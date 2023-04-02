import uuid

from api.core.config import settings
from api.utils.constants import DEPLOY_ENVIRONMENT_LOCAL


def generate_file_name(file_type: str) -> str:
    file_extension = file_type.split("/")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    return file_name


async def upload_file_to_bucket(file_bytes: bytes, file_name: str) -> None:
    if settings.deploy_environment == DEPLOY_ENVIRONMENT_LOCAL:
        with open(f"./uploaded_files/{file_name}", "wb") as f:
            f.write(file_bytes)
    else:
        raise Exception("implement cloud deploy file upload")
