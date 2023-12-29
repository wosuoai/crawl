import pygame
import pyautogui
import time
import re
import json
import asyncio
import websockets
import queue
# 导入线程池
from concurrent.futures import ThreadPoolExecutor

def process_message(message:str):
    try:
       message=json.loads(message)
       t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
       nickname = re.search(r'"Nickname":"(.*?)"', str(message)).group(1)
       HeadImgUrl = re.search(r'"HeadImgUrl":"(.*?)"', str(message)).group(1)
       content = re.search(r'"Content":"(.*?)"', str(message)).group(1)
       if '来了' in content:
           content = content.replace(nickname, '').replace('来了', '进入了直播间')
       else:
           content = '发表评论：' + content
       room_id = re.search(r'"RoomId":(\d+)', str(message)).group(1)

       print(f'{t}  当前直播间RoomId：{room_id}  用户：{nickname}   用户头像链接：{HeadImgUrl}  {content}')
    except Exception as error:
        print(error)


async def web_socket_main():
    print("接受到websocket消息")
    url = "ws://127.0.0.1:8888"
    websocket = await websockets.connect(url)
    while True:
        # print("接受到websocket消息一次")
        try:
            message = await websocket.recv()
            process_message(message)
        except Exception as error:
            #websocket.close()
            websocket = await websockets.connect(url)
            print(type(error))
if __name__ == "__main__":
    asyncio.run(web_socket_main())