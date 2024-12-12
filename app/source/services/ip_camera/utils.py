from fastapi import Depends
from .interface import IPCameraServiceInterface
from .local import LocalIPCameraService


def get_ip_camera_service(service: LocalIPCameraService = Depends()) -> IPCameraServiceInterface:
    return service
