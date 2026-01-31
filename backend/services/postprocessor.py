"""推論結果後処理サービス"""

import numpy as np
from models.schemas import Detection
from services.base import ClassMapperBase, PostprocessorBase
from utils.constants import INPUT_SIZE


class YOLOPostprocessor(PostprocessorBase):
    """YOLO用の推論結果後処理クラス"""

    def __init__(self, class_mapper: ClassMapperBase, input_size: int = INPUT_SIZE):
        self.class_mapper = class_mapper
        self.input_size = input_size

    def scale_boxes(
        self, boxes: np.ndarray, original_size: tuple[int, int]
    ) -> np.ndarray:
        """
        バウンディングボックス座標を元画像サイズにスケール変換

        Args:
            boxes: shape=(N, 4) [x1, y1, x2, y2]
            original_size: (width, height)
        """
        # スケール計算（letterbox考慮）
        scale = min(
            self.input_size / original_size[0], self.input_size / original_size[1]
        )

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
        conf_threshold: float,
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
        boxes[:, [0, 2]] /= width  # x座標
        boxes[:, [1, 3]] /= height  # y座標

        # 結果をリスト化
        for i, box in enumerate(boxes):
            class_id = int(filtered_outputs[i, 5])
            confidence = float(filtered_outputs[i, 4])

            detections.append(
                {
                    "class_id": class_id,
                    "class_name": self.class_mapper.get_class_name(class_id),
                    "confidence": round(confidence, 3),
                    "bbox": {
                        "x1": round(float(box[0]), 4),
                        "y1": round(float(box[1]), 4),
                        "x2": round(float(box[2]), 4),
                        "y2": round(float(box[3]), 4),
                    },
                }
            )

        return detections
