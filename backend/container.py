"""依存性注入コンテナ"""

from config import Settings
from dependency_injector import containers, providers
from services.class_mapper import ClassMapper
from services.image_processing import ImageProcessor
from services.inference import InferenceService
from services.model_loader import ModelLoader
from services.postprocessor import YOLOPostprocessor
from services.preprocessor import YOLOPreprocessor
from utils.constants import CLASSES


class Container(containers.DeclarativeContainer):
    """アプリケーション全体のDIコンテナ"""

    # 設定
    config = providers.Singleton(Settings)

    # ClassMapper（シングルトン）
    class_mapper = providers.Singleton(ClassMapper, class_names=CLASSES)

    # ModelLoader（シングルトン）
    model_loader = providers.Singleton(
        ModelLoader, model_path=config.provided.model_path
    )

    # ModelLoaderの初期化（load()を呼び出し）
    model_session = providers.Resource(
        lambda loader: loader.load(), loader=model_loader
    )

    # InferenceService（シングルトン）
    inference_service = providers.Singleton(InferenceService, session=model_session)

    # YOLOPreprocessor（シングルトン）
    preprocessor = providers.Singleton(
        YOLOPreprocessor, input_size=config.provided.input_size
    )

    # YOLOPostprocessor（シングルトン）
    postprocessor = providers.Singleton(
        YOLOPostprocessor,
        class_mapper=class_mapper,
        input_size=config.provided.input_size,
    )

    # ImageProcessor（コーディネーター・シングルトン）
    image_processor = providers.Singleton(
        ImageProcessor, preprocessor=preprocessor, postprocessor=postprocessor
    )
