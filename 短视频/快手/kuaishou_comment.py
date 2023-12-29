import requests
from kuaishou_data import get_photoId
from fake_useragent import UserAgent

share_url = "https://www.kuaishou.com/f/X-6ew1IHeJ6gJ1fl"
cookies = {'did': 'web_50a6d089a9d08c2e42ed768f997af787'}

def ks_comment_referer(share_url: str) -> str:
    """
    给快手评论接口提供参数
    :param share_url:
    :return:
    """
    headers = {'User-Agent': UserAgent().random}

    html = requests.get(share_url, cookies=cookies, headers=headers).text.replace("\n","").replace(" ","").replace("\\u002F","/")
    referer = "https://www.kuaishou.com/short-video/{}".format(get_photoId(html))
    return referer

def ks_comment_details() -> dict:
    """
    快手评论接口数据
    :return:
    """
    headers = {
        'Origin': 'https://www.kuaishou.com',
        'Referer': ks_comment_referer(share_url),
        'User-Agent': UserAgent().random,
    }

    json_data = {
        'operationName': 'commentListQuery',
        'variables': {
            'photoId': ks_comment_referer(share_url).split("video/")[-1],
            'pcursor': '',
        },
        'query': 'query commentListQuery($photoId: String, $pcursor: String) {\n  visionCommentList(photoId: $photoId, pcursor: $pcursor) {\n    commentCount\n    pcursor\n    rootComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      authorLiked\n      subCommentCount\n      subCommentsPcursor\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        likedCount\n        realLikedCount\n        liked\n        status\n        authorLiked\n        replyToUserName\n        replyTo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
    }

    ks_comment = requests.post('https://www.kuaishou.com/graphql', cookies=cookies, headers=headers, json=json_data).json()
    return ks_comment