"""クラス名マッピングサービス"""

from services.base import ClassMapperBase
from utils.logger import logger


class ClassMapper(ClassMapperBase):
    """クラスIDとクラス名のマッピングを管理"""

    def __init__(self, class_names: list[str]):
        """
        Args:
            class_names: クラス名のリスト（インデックスがクラスID）
        """
        self.class_names = class_names
        logger.info(f"ClassMapper initialized with {len(class_names)} classes")

    def get_class_name(self, class_id: int) -> str:
        """
        クラスIDからクラス名を取得

        Args:
            class_id: クラスID

        Returns:
            クラス名（範囲外の場合は "unknown"）
        """
        if 0 <= class_id < len(self.class_names):
            return self.class_names[class_id]
        logger.warning(f"Invalid class_id: {class_id}")
        return "unknown"
