"""型定義とPydanticスキーマ"""

from pydantic import BaseModel, Field, field_validator


class BoundingBox(BaseModel):
    """バウンディングボックス座標（正規化済み: 0-1）"""

    x1: float = Field(..., ge=0.0, le=1.0, description="左上のx座標（正規化済み）")
    y1: float = Field(..., ge=0.0, le=1.0, description="左上のy座標（正規化済み）")
    x2: float = Field(..., ge=0.0, le=1.0, description="右下のx座標（正規化済み）")
    y2: float = Field(..., ge=0.0, le=1.0, description="右下のy座標（正規化済み）")

    @field_validator("x2")
    @classmethod
    def validate_x2(cls, v: float, info) -> float:
        """x2がx1より大きいことを検証"""
        if "x1" in info.data and v <= info.data["x1"]:
            raise ValueError("x2はx1より大きい必要があります")
        return v

    @field_validator("y2")
    @classmethod
    def validate_y2(cls, v: float, info) -> float:
        """y2がy1より大きいことを検証"""
        if "y1" in info.data and v <= info.data["y1"]:
            raise ValueError("y2はy1より大きい必要があります")
        return v


class Detection(BaseModel):
    """物体検出結果"""

    class_id: int = Field(..., ge=0, description="クラスID")
    class_name: str = Field(..., min_length=1, description="クラス名")
    confidence: float = Field(..., ge=0.0, le=1.0, description="信頼度スコア")
    bbox: BoundingBox = Field(..., description="バウンディングボックス")


class ImageSize(BaseModel):
    """画像サイズ"""

    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)


class DetectionResponse(BaseModel):
    """検出APIのレスポンス"""

    status: str
    detections: list[Detection]  # BaseModelに変更
    image_size: ImageSize
    conf_threshold: float = Field(..., ge=0.0, le=1.0)
