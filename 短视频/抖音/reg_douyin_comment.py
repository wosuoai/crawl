import json

with open("douyin_comment.json", "r", encoding='utf-8') as f:
    comment_data = json.load(f)

for comment in comment_data["comments"]:
    user_cid = comment["cid"]
    user_comment = comment["text"]
    user_aweme_id = comment["aweme_id"]
    user_create_time = comment["create_time"]
    user_count = comment["digg_count"]

    user_uid = comment["user"]["uid"]
    user_short_id = comment["user"]["short_id"]
    user_nickname = comment["user"]["nickname"]
    user_signature = comment["user"]["signature"]
    user_uri = comment["user"]["avatar_larger"]["uri"]
    user_background = comment["user"]["avatar_larger"]["url_list"][0]

    print(user_background)

comment_cursor = comment_data["cursor"]  # 下一页评论的游标
comment_total = comment_data["total"]  # 共计有多少条评论
print(comment_cursor,comment_total)