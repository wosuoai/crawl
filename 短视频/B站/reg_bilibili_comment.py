import json

with open("bilibili_comment.json", "r", encoding='utf-8') as f:
    comment_data = json.load(f)

for reply in comment_data["data"]["replies"]:
    reply_time = reply["ctime"]  # 用户评论时间

    user_id = reply["member"]["mid"]  # 评论用户的id
    user_name = reply["member"]["uname"]  # 评论用户的昵称
    user_sex = reply["member"]["sex"]  # 评论用户的性别
    user_sign = reply["member"]["sign"]  # 评论用户的个性签名
    user_avatar = reply["member"]["avatar"]  # 评论用户的头像链接

    user_vip_level = reply["member"]["level_info"]["current_level"]  # 评论用户的会员等级

    user_content = reply["content"]["message"]  # 用户的评论


    replies = reply["replies"]  # 二级用户评论
    if len(replies) != 0:
        for any_reply in replies:
            any_reply_time = any_reply["ctime"]

            any_user_id = any_reply["member"]["mid"]  # 评论用户的id
            any_user_name = any_reply["member"]["uname"]  # 评论用户的昵称
            any_user_sex = any_reply["member"]["sex"]  # 评论用户的性别
            any_user_sign = any_reply["member"]["sign"]  # 评论用户的个性签名
            any_user_avatar = any_reply["member"]["avatar"]  # 评论用户的头像链接

            any_user_vip_level = any_reply["member"]["level_info"]["current_level"]  # 评论用户的会员等级

            any_user_content = any_reply["content"]["message"]  # 用户的评论

            print(any_user_content.split(" :")[-1])