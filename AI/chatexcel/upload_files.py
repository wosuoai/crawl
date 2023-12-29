import requests
from fake_useragent import UserAgent

headers = {
    'Origin': 'https://chatexcel.com',
    'Referer': 'https://chatexcel.com/convert',
    'User-Agent': UserAgent().random,
}

# 用户上传文件后返回的数据
async def upload_excel_data(file):
    try:
        binary_data = await file.read()
        filename = file.filename

        data = {
            "avatar": (filename, binary_data)
        }
        excel_data = requests.post(headers=headers, files=data, url="https://chatexcel.com/upload_excel").json()
        return excel_data
    except Exception as error:
        return str(error)