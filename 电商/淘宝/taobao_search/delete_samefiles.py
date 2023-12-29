import os
import shutil

folder_path = r'E:\shop_imgs\老钱风'
folder_path1 = r'E:\test1'

# 获取所有子文件夹
subfolders = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
subfolders1 = [os.path.join(folder_path, d.split("-")[0]) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

print(f"删除前的文件夹总量是{len(subfolders1)}")

first_occurrence = {} #记录没有重复的文件夹
duplicates_indices = [] #存放重复文件夹的索引
# 判断subfolders1列表中是否有重复的元素
if len(subfolders1) != len(set(subfolders1)):
    for index, name in enumerate(subfolders1):
        if name in first_occurrence:
            duplicates_indices.append(index)
        else:
            first_occurrence[name] = index

#删除重复文件夹
for del_index in duplicates_indices:
    shutil.rmtree(subfolders[del_index])
    subfolders = subfolders[:]

    # shutil.move(subfolders[del_index],folder_path1)
    # subfolders = subfolders[:]

# 删除后剩余的文件夹数量
now_subfolders = [os.path.join(folder_path, d) for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
print(f"删除后的文件夹总量是{len(now_subfolders)}")

#删除不包含关键词的商品
# import os
# import shutil
#
# folder_path = r"E:\keyword\国风大衣"  # 父文件夹路径
#
# # 遍历父文件夹下的所有子文件夹和文件
# for root, dirs, files in os.walk(folder_path):
#     for dir in dirs:
#         dir_path = os.path.join(root, dir)  # 获取文件夹的完整路径
#         if not any(keyword in dir for keyword in ["国风", "新中式"]):  # 如果文件夹名不包含关键词
#             shutil.rmtree(dir_path)  # 删除该文件夹