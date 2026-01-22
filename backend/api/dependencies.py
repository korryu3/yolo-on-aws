"""FastAPI依存性注入"""
from fastapi import HTTPException
from services.model_loader import ModelLoader
from services.inference import InferenceService
from services.image_processing import ImageProcessor


# グローバルインスタンス（アプリケーション起動時に初期化）
model_loader: ModelLoader | None = None
image_processor: ImageProcessor | None = None


def get_inference_service() -> InferenceService:
    """推論サービスを取得"""
    if model_loader is None:
        raise HTTPException(status_code=503, detail="Model loader not initialized")
    
    try:
        session = model_loader.get_session()
        return InferenceService(session)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


def get_image_processor() -> ImageProcessor:
    """画像処理サービスを取得"""
    if image_processor is None:
        raise HTTPException(status_code=503, detail="Image processor not initialized")
    return image_processor
