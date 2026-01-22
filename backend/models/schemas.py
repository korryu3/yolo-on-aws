"""型定義とPydanticスキーマ"""
from typing import TypedDict
from pydantic import BaseModel, Field


class BoundingBox(TypedDict):
    """バウンディングボックス座標（正規化済み: 0-1）"""
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(TypedDict):
    """物体検出結果"""
    class_id: int
    class_name: str
    confidence: float
    bbox: BoundingBox


class ImageSize(BaseModel):
    """画像サイズ"""
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)


class DetectionResponse(BaseModel):
    """検出APIのレスポンス"""
    status: str
    detections: list[dict]
    image_size: ImageSize
    conf_threshold: float
