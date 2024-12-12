from database.repos import BaseRepository
from database.models import CameraConfig as CameraConfigModel


class CameraConfigRepository(BaseRepository[CameraConfigModel]):
    MODEL = CameraConfigModel
