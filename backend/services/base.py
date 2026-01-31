"""サービス層の抽象基底クラス定義"""

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from models.schemas import Detection


class ModelSessionBase(ABC):
    """モデルセッションの抽象基底クラス"""

    @abstractmethod
    def get_inputs(self) -> list[Any]:
        """モデルの入力情報を取得"""
        pass

    @abstractmethod
    def run(
        self, output_names: list[str] | None, input_feed: dict[str, np.ndarray]
    ) -> list[np.ndarray]:
        """推論を実行"""
        pass


class ModelLoaderBase(ABC):
    """モデルローダーの抽象基底クラス"""

    @abstractmethod
    def load(self) -> ModelSessionBase:
        """モデルをロードしてセッションを返す"""
        pass

    @abstractmethod
    def get_session(self) -> ModelSessionBase:
        """ロード済みのセッションを取得"""
        pass


class InferenceServiceBase(ABC):
    """推論サービスの抽象基底クラス"""

    @abstractmethod
    def run(self, input_tensor: np.ndarray) -> np.ndarray:
        """
        推論を実行

        Args:
            input_tensor: 入力テンソル

        Returns:
            推論結果の配列
        """
        pass


class ClassMapperBase(ABC):
    """クラス名マッピングの抽象基底クラス"""

    @abstractmethod
    def get_class_name(self, class_id: int) -> str:
        """
        クラスIDからクラス名を取得

        Args:
            class_id: クラスID

        Returns:
            クラス名
        """
        pass


class PreprocessorBase(ABC):
    """画像前処理の抽象基底クラス"""

    @abstractmethod
    def preprocess(self, image_bytes: bytes) -> tuple[np.ndarray, tuple[int, int]]:
        """
        画像を前処理

        Args:
            image_bytes: 画像のバイトデータ

        Returns:
            tuple[np.ndarray, tuple[int, int]]: (前処理済みテンソル, 元画像サイズ)
        """
        pass


class PostprocessorBase(ABC):
    """推論結果後処理の抽象基底クラス"""

    @abstractmethod
    def postprocess(
        self,
        outputs: np.ndarray,
        original_size: tuple[int, int],
        conf_threshold: float,
    ) -> list[Detection]:
        """
        推論結果を後処理

        Args:
            outputs: 推論結果の配列
            original_size: 元画像サイズ (width, height)
            conf_threshold: 信頼度閾値

        Returns:
            検出結果のリスト
        """
        pass


class ImageProcessorBase(ABC):
    """画像処理のコーディネーター抽象基底クラス"""

    @abstractmethod
    def preprocess(self, image_bytes: bytes) -> tuple[np.ndarray, tuple[int, int]]:
        """
        画像を前処理

        Args:
            image_bytes: 画像のバイトデータ

        Returns:
            tuple[np.ndarray, tuple[int, int]]: (前処理済みテンソル, 元画像サイズ)
        """
        pass

    @abstractmethod
    def postprocess(
        self, outputs: np.ndarray, original_size: tuple[int, int], conf_threshold: float
    ) -> list[Detection]:
        """
        推論結果を後処理

        Args:
            outputs: 推論結果の配列
            original_size: 元画像サイズ (width, height)
            conf_threshold: 信頼度閾値

        Returns:
            検出結果のリスト
        """
        pass
