"""画像前処理サービス"""

import io

import numpy as np
from PIL import Image, ImageOps
from services.base import PreprocessorBase
from utils.constants import INPUT_SIZE, PADDING_COLOR
from utils.logger import logger


class YOLOPreprocessor(PreprocessorBase):
    """YOLO用の画像前処理クラス"""

    def __init__(
        self,
        input_size: int = INPUT_SIZE,
        padding_color: tuple[int, int, int] = PADDING_COLOR,
    ):
        self.input_size = input_size
        self.padding_color = padding_color

    def preprocess(self, image_bytes: bytes) -> tuple[np.ndarray, tuple[int, int]]:
        """
        画像を前処理してYOLO入力形式に変換

        Args:
            image_bytes: 画像のバイトデータ

        Returns:
            tuple[np.ndarray, tuple[int, int]]: (前処理済みテンソル, 元画像サイズ(width, height))
        """
        try:
            # 画像読み込み
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

            # EXIF情報を考慮して画像を回転（スマホ写真などの対応）
            try:
                image = ImageOps.exif_transpose(image)
            except Exception:
                pass  # EXIF情報がない場合はそのまま

            original_size = image.size  # (width, height)

            # letterbox処理（アスペクト比維持+パディング）
            scale = min(
                self.input_size / original_size[0], self.input_size / original_size[1]
            )
            new_width = int(original_size[0] * scale)
            new_height = int(original_size[1] * scale)

            # リサイズ
            resized_image = image.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )

            # パディング
            padded_image = Image.new(
                "RGB", (self.input_size, self.input_size), self.padding_color
            )
            paste_x = (self.input_size - new_width) // 2
            paste_y = (self.input_size - new_height) // 2
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
            logger.error(f"Failed to preprocess image: {e}")
            raise ValueError(f"Failed to preprocess image: {e}")
