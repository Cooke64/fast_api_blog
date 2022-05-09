import shutil

from fastapi import UploadFile, HTTPException


IMG_TYPES = ['image/jpeg', 'image/png']
VIDEO_TYPES = ['video/mp4']


def save_item(file_name: str, file: UploadFile):
    """Сохраняет изображение."""
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


def get_file_name(file_type, tasks, item):
    """Получаем file_type и согласно него получаем file_name."""
    if file_type in IMG_TYPES:
        file_name = f'media/img/{item.filename}'
        tasks.add_task(save_item, file_name, item)
    elif file_type in VIDEO_TYPES:
        file_name = f'media/video/{item.filename}'
        tasks.add_task(save_item, file_name, item)
    else:
        raise HTTPException(status_code=418, detail='Загружай только картинки')
    return file_name
