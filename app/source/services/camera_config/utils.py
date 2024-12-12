from fastapi import Depends
from .interface import CameraConfigServiceInterface
from .local import LocalCameraConfigService


def get_camera_config_service(service: LocalCameraConfigService = Depends()) -> CameraConfigServiceInterface:
    return service
