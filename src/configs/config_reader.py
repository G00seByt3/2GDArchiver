import pathlib

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Адрес папки в GoogleDrive
    gd_obsidian_path: SecretStr 
    # Путь до файла с данными сервисного аккаунта 
    service_account_file: SecretStr

    scopes: list = ['https://www.googleapis.com/auth/drive']
    # Папка с созданными архивами  
    path_to_zip: str = 'src/archives/'


    model_config = SettingsConfigDict(env_file=f"{pathlib.Path(__file__).resolve().parent}/config.env",
                                      env_file_encoding='utf-8')


cfg = Settings()