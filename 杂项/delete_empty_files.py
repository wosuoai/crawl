import os

def delete_empty_images(root_dir):
    #父文件夹下的所有店铺的文件夹
    for shop_dir in os.listdir(root_dir):
        shop_path = os.path.join(root_dir, shop_dir)
        #判断店铺的文件夹是否为True
        if os.path.isdir(shop_path):
            #每个店铺文件夹下面所有的商品文件夹
            for product_dir in os.listdir(shop_path):
                product_path = os.path.join(shop_path, product_dir)
                #判断商品文件夹是否为True
                if os.path.isdir(product_path):
                    #所有图片的完整路径
                    for image_file in os.listdir(product_path):
                        image_path = os.path.join(product_path, image_file)
                        '''
                        try except
                        为了避免边下载边删除 从而导致的异常情况
                        '''
                        try: #删除大小为0的图片
                            if os.path.isfile(image_path) and os.path.getsize(image_path) == 0:
                                os.remove(image_path)
                                print(f"删除图片： {image_path}")
                        except Exception as error:
                            pass

root_dir = r"E:\shop_imgs"
delete_empty_images(root_dir)
