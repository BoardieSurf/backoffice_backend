from fastapi import HTTPException, UploadFile


def ensure_file_is_image(file: UploadFile) -> None:
    if file.content_type not in ["image/png", "image/jpg", "image/gif", "image/jpeg"]:
        raise HTTPException(
            400,
            detail="Invalid document type, only images are supported (jpeg, jpg, gif, png)",
        )
