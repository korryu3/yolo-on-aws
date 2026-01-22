"""YOLOモデルのロード処理"""
from pathlib import Path
import onnxruntime as ort
from backend.utils.logger import logger


class ModelLoader:
    """YOLOモデルローダー"""
    
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self.session: ort.InferenceSession | None = None
    
    def load(self) -> ort.InferenceSession:
        """モデルをロード"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        try:
            self.session = ort.InferenceSession(str(self.model_path))
            logger.info(f"✓ YOLO model loaded successfully from {self.model_path}")
            return self.session
        except Exception as e:
            logger.error(f"Failed to load ONNX model: {e}")
            raise RuntimeError(f"Failed to load ONNX model: {e}")
    
    def get_session(self) -> ort.InferenceSession:
        """セッションを取得（未ロードの場合は例外）"""
        if self.session is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        return self.session
