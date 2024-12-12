from database.repos import BaseRepository
from database.models import IPCamera as IPCameraModel


class IPCameraRepository(BaseRepository[IPCameraModel]):
    MODEL = IPCameraModel
