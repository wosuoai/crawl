import os

folder_path = r"E:\新建文件夹"

# 遍历父文件夹下的所有子文件夹和文件
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".mp4"):
            file_path = os.path.join(root, file)  # 获取文件的完整路径
            os.remove(file_path)