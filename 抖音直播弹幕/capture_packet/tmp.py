import re
import time

a = """{'Type': 1, 'ProcessName': 'msedge', 'Data': '{"MsgId":7301885484794450954,"User":{"FollowingCount":27,"Id":98693256907,"ShortId":952066878,"DisplayId":"952066878","Nickname":"义乌严选云仓","Level":0,"PayLevel":0,"Gender":2,"HeadImgUrl":"https://p6.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-avt-0015_725d2f8dd76ecdd695640a12072eb97b.jpeg?from=3067671334","SecUid":"MS4wLjABAAAAdPYZvupL-PCtbfzfvr9OJig5vb8Rgtf4bUbmsDc2OC4","FansClub":{"ClubName":"","Level":0},"FollowerCount":1496,"FollowStatus":0},"Content":"厂家直发, 亏米送浮力,多功能理发器,拍下只需 要29.9米","RoomId":7301805904905669413,"WebRoomId":-1}'}"""

nickname = re.search(r'"Nickname":"(.*?)"', a).group(1)
HeadImgUrl = re.search(r'"HeadImgUrl":"(.*?)"', a).group(1)
content = re.search(r'"Content":"(.*?)"', a).group(1)
if '来了' in content:
    content = content.replace(nickname,'').replace('来了','进入了直播间')
else:
    content = '发表评论：' + content
room_id = re.search(r'"RoomId":(\d+)', a).group(1)

t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f'{t}  当前直播间RoomId：{room_id}  用户：{nickname}   用户头像链接：{HeadImgUrl}  {content}')
# print("Nickname:", nickname)
# print("Content:", content)
# print("RoomId:", room_id)