"""YOLO推論サービス"""
import numpy as np
import onnxruntime as ort
from backend.utils.logger import logger


class InferenceService:
    """推論実行サービス"""
    
    def __init__(self, session: ort.InferenceSession):
        self.session = session
    
    def run(self, input_tensor: np.ndarray) -> np.ndarray:
        """
        ONNX Runtimeで推論を実行
        
        Args:
            input_tensor: shape=(1, 3, 640, 640)
        
        Returns:
            outputs: shape=(1, num_detections, 6) [x1, y1, x2, y2, conf, class_id]
        """
        try:
            input_name = self.session.get_inputs()[0].name
            outputs = self.session.run(None, {input_name: input_tensor})
            return outputs[0]
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise RuntimeError(f"Inference failed: {e}")
