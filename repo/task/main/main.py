"""
Тестовой задание.

Скрипт выполненого тестового задания по асинхронному скачиванию
файлов из удаленного репозитария и вычисления их хеша.
"""
import asyncio
import hashlib
import os

import aiofiles
import aiohttp


class DownloadRepo:
    """
    Класс для асинхронного скачивания репозиториев.

    get_hash: вычисляет хеши файлов
    download_list_name_file: получает списки файлов репозитория
    download_file: скачивает файлы из репозитория.
    get_list_files: получаем файлы из каталога
    main: метод, объеденяющий всю логику класса.
    """

    def __init__(self, url, url_list_file, directory):
        """Создание экземпляра класса.

        Args:
            url: ссылка на репозиторий
            url_list_file: ссылка на страницу списка с именами файлов хранящимися в репозитории
            directory: временная папка
        """
        self.url = url
        self.url_list_file = url_list_file
        self.directory = directory
        self.SIZE = 2048
        self.NUMBER_OF_TREADS = 12

    def get_hash(self):
        """Вычисление хеша файлов.

        Returns:
            list_hash (list): список вычисленных хешей SHA-256
        """
        list_hash = []
        for path_file in self.get_list_files():
            with open(path_file, 'rb') as path_file:
                sha256_hash = hashlib.sha256()
                while True:
                    data = path_file.read(self.SIZE)
                    if not data:
                        break
                    sha256_hash.update(data)
                list_hash.append(sha256_hash.hexdigest())

        return list_hash

    async def download_list_name_file(self, link):
        """Получение списка файлов репозитория.

        Args:
            link: ссылка на страницу списка с именами файлов
                хранящимися в репозитории

        Returns:
            list_name (list): список имен файлов репозитария
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(link, allow_redirects=True) as response:
                return await response.json()

    async def download_file(self, link, name, sem):
        """Скачивание файлов из репозитария.

        Args:
            link: ссылка для построения полного url файла
            name: имя файла для ссылки
            sem: семафор

        """
        async with aiohttp.ClientSession() as session:
            async with sem, session.get(link) as response:
                data_for_entries = await response.text()
                async with aiofiles.open(self.directory + name, 'w') as file:
                    await file.write(data_for_entries)

    def get_list_files(self):
        """Получение файлов из каталога.

        Returns:
            list_files (list): список файлов
        """
        list_files = []
        for root, _, files in os.walk(self.directory):
            for path_file in files:
                list_files.append(f'{root}/{path_file}')
        return list_files

    async def main(self):
        """
        Функция обьединяющая всю логику модуля.

        Саздание временной директории

        Returns:
            get_hash() (list): список вычисленных хешей
        """
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

        sem = asyncio.BoundedSemaphore(self.NUMBER_OF_TREADS)
        list_name_for_urls = await asyncio.gather(
            asyncio.create_task(self.download_list_name_file(self.url_list_file)),
        )

        list_urls = []
        for name in list_name_for_urls[0]:
            list_urls.append(self.url + name)

        await asyncio.gather(
            *[
                asyncio.create_task(
                    self.download_file(url_file, url_file.split('/')[-1], sem),
                )
                for url_file in list_urls
            ],
        )
        return self.get_hash()


if __name__ == '__main__':
    url = 'https://gitea.radium.group/radium/project-configuration/raw/branch/master/'

    url_list_file = 'https://gitea.radium.group/radium/project-configuration/tree-list/branch/master'

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    directory = f'{BASEDIR}/project-configuration/'
    download = DownloadRepo(url, url_list_file, directory)
    asyncio.run(download.main())
