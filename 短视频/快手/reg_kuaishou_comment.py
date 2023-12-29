import json

with open("kuaishou_comment.json", "r", encoding='utf-8') as f:
    comment_data = json.load(f)

count = comment_data["data"]["visionCommentList"]["commentCount"]  # 该视频的获赞数
pcursor = comment_data["data"]["visionCommentList"]["pcursor"]  # 下一页评论的游标

for comment in comment_data["data"]["visionCommentList"]["rootComments"]:
    user_id = comment["authorId"]  # 评论用户的id
    user_name = comment["authorName"]  # 评论用户的昵称
    user_headUrl = comment["headurl"]  # 评论用户的头像链接

    user_content = comment["content"]  # 用户评论
    content_time = comment["timestamp"]  # 用户评论的时间
    content_likedCount = comment["likedCount"]  # 用户评论的获赞数

    # 二级用户评论的游标
    try:
        subCommentsPcursor = comment["subCommentsPcursor"]
        if subCommentsPcursor == "no_more":
            subCommentsPcursor = ""
    except Exception as error:
        subCommentsPcursor = ""

    subComments = comment["subComments"]  # 二级用户评论
    if len(subComments) != 0:
        for subComment in subComments:
            sub_user_id = subComment["authorId"]
            sub_user_name = subComment["authorName"]
            sub_user_headUrl = subComment["headurl"]

            sub_user_content = subComment["content"]
            sub_content_time = subComment["timestamp"]
            sub_content_likedCount = subComment["likedCount"]

            reply_user_name = subComment["replyToUserName"]  # 该评论的回复对象昵称
            reply_user_id = subComment["replyTo"]  # 该评论的回复对象id