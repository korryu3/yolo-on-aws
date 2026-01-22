"""画像の前処理・後処理"""
from PIL import Image, ImageOps
import numpy as np
import io
from backend.utils.constants import INPUT_SIZE, PADDING_COLOR, CLASSES
from backend.models.schemas import Detection
from backend.utils.logger import logger


class ImageProcessor:
    """画像処理クラス"""
    
    def __init__(self, input_size: int = INPUT_SIZE):
        self.input_size = input_size
    
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
            scale = min(self.input_size / original_size[0], self.input_size / original_size[1])
            new_width = int(original_size[0] * scale)
            new_height = int(original_size[1] * scale)
            
            # リサイズ
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # パディング
            padded_image = Image.new("RGB", (self.input_size, self.input_size), PADDING_COLOR)
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
    
    def scale_boxes(
        self,
        boxes: np.ndarray,
        original_size: tuple[int, int]
    ) -> np.ndarray:
        """
        バウンディングボックス座標を元画像サイズにスケール変換
        
        Args:
            boxes: shape=(N, 4) [x1, y1, x2, y2]
            original_size: (width, height)
        """
        # スケール計算（letterbox考慮）
        scale = min(self.input_size / original_size[0], self.input_size / original_size[1])
        
        # パディング計算
        new_width = int(original_size[0] * scale)
        new_height = int(original_size[1] * scale)
        pad_x = (self.input_size - new_width) / 2
        pad_y = (self.input_size - new_height) / 2
        
        # 座標変換
        boxes[:, [0, 2]] = (boxes[:, [0, 2]] - pad_x) / scale  # x1, x2
        boxes[:, [1, 3]] = (boxes[:, [1, 3]] - pad_y) / scale  # y1, y2
        
        # 画像範囲内にクリップ
        boxes[:, [0, 2]] = np.clip(boxes[:, [0, 2]], 0, original_size[0])
        boxes[:, [1, 3]] = np.clip(boxes[:, [1, 3]], 0, original_size[1])
        
        return boxes
    
    def postprocess(
        self,
        outputs: np.ndarray,
        original_size: tuple[int, int],
        conf_threshold: float
    ) -> list[Detection]:
        """
        推論結果を後処理して検出結果リストに変換（正規化座標）
        
        Args:
            outputs: shape=(batch, num_detections, 6) [x1, y1, x2, y2, conf, class_id]
            original_size: (width, height)
            conf_threshold: 信頼度閾値
        
        Returns:
            検出結果のリスト（座標は0-1に正規化）
        """
        detections: list[Detection] = []
        
        # バッチ次元を削除
        outputs = outputs[0]  # shape: (num_detections, 6)
        
        # 信頼度フィルタリング
        mask = outputs[:, 4] >= conf_threshold
        filtered_outputs = outputs[mask]
        
        if len(filtered_outputs) == 0:
            return detections
        
        # 座標スケーリング（元画像サイズ）
        boxes = filtered_outputs[:, :4].copy()
        boxes = self.scale_boxes(boxes, original_size)
        
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
                "class_name": self._get_class_name(class_id),
                "confidence": round(confidence, 3),
                "bbox": {
                    "x1": round(float(box[0]), 4),
                    "y1": round(float(box[1]), 4),
                    "x2": round(float(box[2]), 4),
                    "y2": round(float(box[3]), 4)
                }
            })
        
        return detections
    
    @staticmethod
    def _get_class_name(class_id: int) -> str:
        """クラスIDからクラス名を取得"""
        if 0 <= class_id < len(CLASSES):
            return CLASSES[class_id]
        return "unknown"
