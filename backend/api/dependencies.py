"""FastAPI依存性注入"""

from container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from services.base import ImageProcessorBase, InferenceServiceBase


@inject
def get_inference_service(
    service: InferenceServiceBase = Depends(Provide[Container.inference_service]),
) -> InferenceServiceBase:
    """推論サービスを取得"""
    return service


@inject
def get_image_processor(
    processor: ImageProcessorBase = Depends(Provide[Container.image_processor]),
) -> ImageProcessorBase:
    """画像処理サービスを取得"""
    return processor
