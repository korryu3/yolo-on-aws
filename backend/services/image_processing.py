"""画像処理コーディネーター"""

import numpy as np
from models.schemas import Detection
from services.base import (
    ImageProcessorBase,
    PostprocessorBase,
    PreprocessorBase,
)
from utils.logger import logger


class ImageProcessor(ImageProcessorBase):
    """画像処理のコーディネーター（前処理と後処理を組み合わせる）"""

    def __init__(
        self, preprocessor: PreprocessorBase, postprocessor: PostprocessorBase
    ):
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor
        logger.info("ImageProcessor initialized with preprocessor and postprocessor")

    def preprocess(self, image_bytes: bytes) -> tuple[np.ndarray, tuple[int, int]]:
        """
        画像を前処理（preprocessorに委譲）

        Args:
            image_bytes: 画像のバイトデータ

        Returns:
            tuple[np.ndarray, tuple[int, int]]: (前処理済みテンソル, 元画像サイズ)
        """
        return self.preprocessor.preprocess(image_bytes)

    def postprocess(
        self,
        outputs: np.ndarray,
        original_size: tuple[int, int],
        conf_threshold: float,
    ) -> list[Detection]:
        """
        推論結果を後処理（postprocessorに委譲）

        Args:
            outputs: 推論結果の配列
            original_size: 元画像サイズ (width, height)
            conf_threshold: 信頼度閾値

        Returns:
            検出結果のリスト
        """
        return self.postprocessor.postprocess(outputs, original_size, conf_threshold)
