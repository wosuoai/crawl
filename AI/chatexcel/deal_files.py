import requests

headers = {
    'Origin': 'https://chatexcel.com',
    'Referer': 'https://chatexcel.com/convert',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


# 汇总处理文件的操作
def executed_data(data: str, table_id: str, my_data: str) -> dict:
    try:
        deal_data = {
            'data': data,
            'table_id': table_id,
            'filename': '',
            'my_data': my_data
        }
        query_data = requests.post('https://chatexcel.com/upload_query', headers=headers, data=deal_data).json()
        return query_data
    except Exception as error:
        return {"error": {str(error)}}
