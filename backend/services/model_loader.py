"""YOLOモデルのロード処理"""

from pathlib import Path

import onnxruntime as ort
from services.base import ModelLoaderBase, ModelSessionBase
from utils.logger import logger


class ONNXModelSession(ModelSessionBase):
    """ONNX Runtime セッションのラッパー"""

    def __init__(self, session: ort.InferenceSession):
        self._session = session

    def get_inputs(self):
        return self._session.get_inputs()

    def run(self, output_names, input_feed):
        return self._session.run(output_names, input_feed)


class ModelLoader(ModelLoaderBase):
    """YOLOモデルローダー"""

    def __init__(self, model_path: Path):
        self.model_path = model_path
        self.session: ModelSessionBase | None = None

    def load(self) -> ModelSessionBase:
        """モデルをロード"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        try:
            ort_session = ort.InferenceSession(str(self.model_path))
            self.session = ONNXModelSession(ort_session)
            logger.info(f"✓ YOLO model loaded successfully from {self.model_path}")
            return self.session
        except Exception as e:
            logger.error(f"Failed to load ONNX model: {e}")
            raise RuntimeError(f"Failed to load ONNX model: {e}")

    def get_session(self) -> ModelSessionBase:
        """セッションを取得（未ロードの場合は例外）"""
        if self.session is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        return self.session
