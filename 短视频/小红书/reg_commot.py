import json

with open("commot.json", "r", encoding='utf-8') as f:
    comment_data = json.load(f)

"""
有关作者的一些信息
id 发布时间 下一页评论的游标

TODO 游标说明
':authority': 'edith.xiaohongshu.com'
':referer': 'https://www.xiaohongshu.com/'
":path"："/api/sns/web/v2/comment/page"
":param": "note_id=&cursor=&top_comment_id=&image_formats=jpg,webp,avif"
仅一个参数：cursor -> 第一次的接口"cursor"是没有赋值的 
-> 第二次调用该接口(评论区翻页拿到更多的评论)需要赋值给"cursor"
-> 因此将"cursor"赋值 拼接后 重复操作即可
!!! *特别强调* "下一页评论的游标" 与 "展开二级评论游标" 是不一样的 !!!
"""
author_user_id = comment_data["data"]["user_id"] # 作者的用户id
author_release_time = comment_data["data"]["time"] # 作者发布笔记的时间
next_comment_cursor = comment_data["data"]["cursor"] # 下一页评论的游标
note_id = comment_data["data"]["comments"][0]["note_id"] # 作者发布该篇笔记的id

"""
用户在该帖子下面的评论 以及 评论用户的一些信息   ->   这里简称一级评论
"""
#一级评论用户 -> 用户id 用户昵称 用户头像
user_id = comment_data["data"]["comments"][0]["user_info"]["user_id"]
user_nickname = comment_data["data"]["comments"][0]["user_info"]["nickname"]
user_image = comment_data["data"]["comments"][0]["user_info"]["image"]

user_tags = comment_data["data"]["comments"][0]["show_tags"] # 一级评论用户评论时 用户昵称后面的标识 比如：作者在下方评论 标识为 "is_author"
user_comment = comment_data["data"]["comments"][0]["content"] # 一级评论用户的评论
user_comment_count = comment_data["data"]["comments"][0]["sub_comment_count"] # 一级评论用户下方二级评论数
# 这里如果发表了图片 提取到的信息 里面多个链接都指向同一张图
try:
    user_pictures = comment_data["data"]["comments"][0]["pictures"] # 一级评论用户发表的图片链接
    if user_pictures != []:
        user_pictures_link = user_pictures[0]["url_default"]
except Exception as error:
    user_pictures = []
user_time = comment_data["data"]["comments"][0]["create_time"] # 一级评论用户评论的时间
user_ip = comment_data["data"]["comments"][0]["ip_location"] # 一级评论用户的IP
# user_id && nickname   -->   返回的是个字典 可以单独做提取
user_at = comment_data["data"]["comments"][0]["at_users"] # 一级评论用户@其他用户
user_liked = comment_data["data"]["comments"][0]["like_count"] # 一级评论用户的评论 点赞的数量

next_user_cursorId = comment_data["data"]["comments"][0]["id"] # 一级评论用户的游标id
next_user_cursor = comment_data["data"]["comments"][0]["sub_comment_cursor"] # 一级评论用户的游标值

user_sub_comment = comment_data["data"]["comments"][0]["sub_comments"] # 二级评论用户的所有内容

"""
用户在评论下方回复的评论 以及 用户的信息   ->   这里简称二级评论 
"""
# 被回复人信息 -> 用户id 用户昵称 用户头像
sub_usered_id = user_sub_comment[0]["target_comment"]["user_info"]["user_id"]
sub_usered_nickname = user_sub_comment[0]["target_comment"]["user_info"]["nickname"]
sub_usered_image = user_sub_comment[0]["target_comment"]["user_info"]["image"]

# 回复人信息 及 评论
# 回复人信息 -> 用户id 用户昵称 用户头像
sub_user_id = user_sub_comment[0]["user_info"]["user_id"]
sub_user_nickname = user_sub_comment[0]["user_info"]["nickname"]
sub_user_image = user_sub_comment[0]["user_info"]["image"]

# 内容信息同上 这里不再单独注释 过多赘述
sub_user_tags = user_sub_comment[0]["show_tags"]
sub_user_ip = user_sub_comment[0]["ip_location"]
sub_user_time = user_sub_comment[0]["create_time"]
try:
    sub_user_pictures = user_sub_comment[0]["pictures"]
    if sub_user_pictures != []:
        sub_user_pictures_link = sub_user_pictures[0]["url_default"]
except Exception as error:
    sub_user_pictures = []
sub_user_comment = user_sub_comment[0]["content"]
# user_id && nickname
sub_user_at = user_sub_comment[0]["at_users"]
sub_user_liked = user_sub_comment[0]["like_count"]