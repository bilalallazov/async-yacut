import asyncio

import aiohttp

API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
UPLOAD_LINK_URL = f'{API_BASE_URL}/upload'
DOWNLOAD_LINK_URL = f'{API_BASE_URL}/download'
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)


async def _get_upload_link(session, path, token):
    headers = {'Authorization': f'OAuth {token}'}
    async with session.get(
        UPLOAD_LINK_URL,
        params={'path': path, 'overwrite': 'true'},
        headers=headers,
    ) as response:
        data = await response.json()
        return data['href']


async def _upload_file(session, upload_url, file_data):
    async with session.put(upload_url, data=file_data) as response:
        await response.read()


async def _get_download_link(session, path, token):
    headers = {'Authorization': f'OAuth {token}'}
    async with session.get(
        DOWNLOAD_LINK_URL,
        params={'path': path},
        headers=headers,
    ) as response:
        data = await response.json()
        return data['href']


async def upload_file(session, file_data, filename, token):
    path = f'app:/{filename}'
    upload_url = await _get_upload_link(session, path, token)
    await _upload_file(session, upload_url, file_data)
    return await _get_download_link(session, path, token)


async def upload_files(files_data, token):
    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        tasks = [
            upload_file(session, file_data, filename, token)
            for file_data, filename in files_data
        ]
        return await asyncio.gather(*tasks)
