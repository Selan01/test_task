import os

from main.main import DownloadRepo
import pytest

url = 'https://gitea.radium.group/radium/project-configuration/raw/branch/master/'

url_list_file = 'https://gitea.radium.group/radium/project-configuration/tree-list/branch/master'

BASEDIR = os.path.abspath(os.path.dirname(__file__))
directory = f'{BASEDIR}/project-configuration/'
download = DownloadRepo(url, url_list_file, directory)

@pytest.mark.asyncio
async def test_download_list_name_file():
    assert len(await download.download_list_name_file(url_list_file)) == 17


@pytest.mark.asyncio
async def test_main():
    assert len(await download.main()) == 16


def test_get_hash():
    assert len(download.get_hash()) == 16