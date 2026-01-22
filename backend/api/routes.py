"""APIエンドポイント定義"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from models.schemas import DetectionResponse, ImageSize
from services.inference import InferenceService
from services.image_processing import ImageProcessor
from api.dependencies import get_inference_service, get_image_processor
from config import settings
from utils.logger import logger

router = APIRouter()


@router.get("/healthz")
def healthz():
    """ヘルスチェック"""
    return {"ok": True}


@router.post("/api/detect", response_model=DetectionResponse)
async def detect(
    file: UploadFile = File(...),
    conf_threshold: float = Form(settings.default_confidence_threshold),
    inference_service: InferenceService = Depends(get_inference_service),
    image_processor: ImageProcessor = Depends(get_image_processor)
):
    """
    画像ファイルを受け取り、YOLO物体検出を実行する
    
    Args:
        file: 画像ファイル
        conf_threshold: 信頼度閾値
        inference_service: 推論サービス（依存性注入）
        image_processor: 画像処理サービス（依存性注入）
    """
    # ファイル形式検証
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are supported"
        )
    
    try:
        # 画像読み込み
        image_bytes = await file.read()
        logger.info(f"Processing image: {file.filename}, size: {len(image_bytes)} bytes")
        
        # 前処理
        input_tensor, original_size = image_processor.preprocess(image_bytes)
        
        # 推論
        outputs = inference_service.run(input_tensor)
        
        # 後処理
        detections = image_processor.postprocess(outputs, original_size, conf_threshold)
        
        logger.info(f"Detected {len(detections)} objects with conf_threshold={conf_threshold}")
        
        return DetectionResponse(
            status="ok",
            detections=detections,
            image_size=ImageSize(width=original_size[0], height=original_size[1]),
            conf_threshold=conf_threshold
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
