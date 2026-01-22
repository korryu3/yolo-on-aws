from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import onnxruntime as ort
import numpy as np
from PIL import Image
import io
from typing import Optional

CLASSES = [
    "weed"
]

# グローバル変数（モデルセッション）
yolo_session: Optional[ort.InferenceSession] = None

def load_yolo_model(model_path: str) -> ort.InferenceSession:
    """YOLOモデルをロードする"""
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        session = ort.InferenceSession(model_path)
        return session
    except Exception as e:
        raise RuntimeError(f"Failed to load ONNX model: {e}")

def get_coco_class_name(class_id: int) -> str:
    """COCOクラスIDからクラス名を取得"""
    if 0 <= class_id < len(CLASSES):
        return CLASSES[class_id]
    return "unknown"

def preprocess_image(image_bytes: bytes) -> tuple[np.ndarray, tuple[int, int]]:
    """
    画像を前処理してYOLO入力形式に変換
    
    Returns:
        tuple[np.ndarray, tuple[int, int]]: (前処理済みテンソル, 元画像サイズ(width, height))
    """
    try:
        # 画像読み込み
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # EXIF情報を考慮して画像を回転（スマホ写真などの対応）
        try:
            from PIL import ImageOps
            image = ImageOps.exif_transpose(image)
        except Exception:
            pass  # EXIF情報がない場合はそのまま
        
        original_size = image.size  # (width, height)
        
        # 640x640にリサイズ（letterbox: アスペクト比維持+パディング）
        target_size = 640
        scale = min(target_size / original_size[0], target_size / original_size[1])
        new_width = int(original_size[0] * scale)
        new_height = int(original_size[1] * scale)
        
        # リサイズ
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # パディング（グレー背景）
        padded_image = Image.new("RGB", (target_size, target_size), (114, 114, 114))
        paste_x = (target_size - new_width) // 2
        paste_y = (target_size - new_height) // 2
        padded_image.paste(resized_image, (paste_x, paste_y))
        
        # numpy配列に変換してCHW形式に変更
        img_array = np.array(padded_image, dtype=np.float32)
        img_array = img_array.transpose(2, 0, 1)  # HWC -> CHW
        
        # 正規化 (0-255 -> 0-1)
        img_array /= 255.0
        
        # バッチ次元追加
        img_array = np.expand_dims(img_array, axis=0)  # (1, 3, 640, 640)
        
        return img_array, original_size
    
    except Exception as e:
        raise ValueError(f"Failed to preprocess image: {e}")

def run_inference(session: ort.InferenceSession, input_tensor: np.ndarray) -> np.ndarray:
    """ONNX Runtimeで推論を実行"""
    try:
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: input_tensor})
        return outputs[0]  # shape: (batch, num_detections, 6)
    except Exception as e:
        raise RuntimeError(f"Inference failed: {e}")

def scale_boxes(
    boxes: np.ndarray,
    original_size: tuple[int, int],
    input_size: tuple[int, int] = (640, 640)
) -> np.ndarray:
    """
    バウンディングボックス座標を元画像サイズにスケール変換
    
    Args:
        boxes: shape=(N, 4) [x1, y1, x2, y2]
        original_size: (width, height)
        input_size: (width, height)
    """
    # スケール計算（letterbox考慮）
    scale = min(input_size[0] / original_size[0], input_size[1] / original_size[1])
    
    # パディング計算
    new_width = int(original_size[0] * scale)
    new_height = int(original_size[1] * scale)
    pad_x = (input_size[0] - new_width) / 2
    pad_y = (input_size[1] - new_height) / 2
    
    # 座標変換
    boxes[:, [0, 2]] = (boxes[:, [0, 2]] - pad_x) / scale  # x1, x2
    boxes[:, [1, 3]] = (boxes[:, [1, 3]] - pad_y) / scale  # y1, y2
    
    # 画像範囲内にクリップ
    boxes[:, [0, 2]] = np.clip(boxes[:, [0, 2]], 0, original_size[0])
    boxes[:, [1, 3]] = np.clip(boxes[:, [1, 3]], 0, original_size[1])
    
    return boxes

def postprocess_detections(
    outputs: np.ndarray,
    original_size: tuple[int, int],
    conf_threshold: float = 0.25
) -> list[dict]:
    """
    推論結果を後処理して検出結果リストに変換（正規化座標）
    
    Args:
        outputs: shape=(batch, num_detections, 6) [x1, y1, x2, y2, conf, class_id]
        original_size: (width, height)
        conf_threshold: 信頼度閾値
    
    Returns:
        検出結果のリスト（座標は0-1に正規化）
    """
    detections = []
    
    # バッチ次元を削除
    outputs = outputs[0]  # shape: (num_detections, 6)
    
    # 信頼度フィルタリング
    mask = outputs[:, 4] >= conf_threshold
    filtered_outputs = outputs[mask]
    
    if len(filtered_outputs) == 0:
        return detections
    
    # 座標スケーリング（元画像サイズ）
    boxes = filtered_outputs[:, :4].copy()
    boxes = scale_boxes(boxes, original_size)
    
    # 正規化（0-1の範囲）
    width, height = original_size
    boxes[:, [0, 2]] /= width   # x座標
    boxes[:, [1, 3]] /= height  # y座標
    
    # 結果をリスト化
    for i, box in enumerate(boxes):
        class_id = int(filtered_outputs[i, 5])
        confidence = float(filtered_outputs[i, 4])
        
        detections.append({
            "class_id": class_id,
            "class_name": get_coco_class_name(class_id),
            "confidence": round(confidence, 3),
            "bbox": {
                "x1": round(float(box[0]), 4),
                "y1": round(float(box[1]), 4),
                "x2": round(float(box[2]), 4),
                "y2": round(float(box[3]), 4)
            }
        })
    
    return detections

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite開発サーバー
        "https://*.vercel.app",   # Vercel本番/プレビュー
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時にモデルをロード"""
    global yolo_session
    model_path = Path(__file__).parent / "YOLOv10n.onnx"
    try:
        yolo_session = load_yolo_model(str(model_path))
        print(f"✓ YOLO model loaded successfully from {model_path}")
    except Exception as e:
        print(f"✗ Failed to load YOLO model: {e}")
        raise

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/api/detect")
async def detect(
    file: UploadFile = File(...),
    conf_threshold: float = Form(0.25)
):
    """
    画像ファイルを受け取り、YOLO物体検出を実行する
    
    Args:
        file: 画像ファイル
        conf_threshold: 信頼度閾値（デフォルト: 0.25）
    """
    global yolo_session
    
    # モデルロード確認
    if yolo_session is None:
        raise HTTPException(status_code=503, detail="YOLO model not loaded")
    
    # ファイル形式検証
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are supported"
        )
    
    try:
        # 画像読み込み
        image_bytes = await file.read()
        
        # 前処理
        input_tensor, original_size = preprocess_image(image_bytes)
        
        # 推論
        outputs = run_inference(yolo_session, input_tensor)
        
        # 後処理
        detections = postprocess_detections(outputs, original_size, conf_threshold)
        
        return {
            "status": "ok",
            "detections": detections,
            "image_size": {
                "width": original_size[0],
                "height": original_size[1]
            },
            "conf_threshold": conf_threshold
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
