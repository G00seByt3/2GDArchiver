import os.path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from zipper import make_zip_from_folder
from configs.config_reader import cfg


class GoogleDrive:
    """
    Взаимодействие с API GoogleDrive

    Коды ошибок:
    0 - нормальное завершение работы 
    -1 - некорректный файл для архивации
    -2 - ошибка во время отправки в GoogleDrive
    """
    credentials: service_account.Credentials

    def __init__(self) -> None:
        self.set_credentials()


    def set_credentials(self) -> None:
        """Получение данных сервисного аккаунта"""
        self.credentials = service_account.Credentials.from_service_account_file(
            filename=cfg.service_account_file.get_secret_value(),
            scopes=cfg.scopes
        )


    def upload_file(self, file_path: str, mime_type="application/zip") -> int:
        """Загрузка архива"""

        try:
            file_path = make_zip_from_folder(file_path)

        except FileNotFoundError: 
            return -1
        
        file_metadata = {
            "name": os.path.split(file_path)[1],
            "parents": [cfg.gd_obsidian_path.get_secret_value()],
        }

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=False)

        try:
            with build('drive', 'v3', credentials=self.credentials) as service:
                service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
            return 0
        
        except HttpError:
            return -2


gdrive = GoogleDrive()
