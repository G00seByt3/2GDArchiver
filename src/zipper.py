import shutil
import os.path

from configs.config_reader import cfg


def make_zip_from_folder(path_to_folder: str) -> str:
    """
    Архивирование папки в директорию archives

    :path_to_folder: - путь до искомой папки
    """
    # Отделяем от абсолютного пути папки ее имя
    filename = os.path.split(path_to_folder)[1]

    # Путь созданного архива
    path_to_zip = cfg.path_to_zip + '/' + filename

    # make_archive возвращает имя созданного архива
    return shutil.make_archive(path_to_zip, 'zip', path_to_folder)

