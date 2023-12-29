from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def get_items():
    # 连接数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='wosuoai8279', database='taobao_tmall')
    cursor = conn.cursor()

    # 查询所有数据并存入shop_list列表中
    sql = "SELECT shop_id FROM crawled_shops"
    cursor.execute(sql)
    results = cursor.fetchall()
    shop_list = [result[0] for result in results]

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return shop_list

@app.route('/api/shops', methods=['GET'])
def get_shops():
    shop_list = get_items()
    return jsonify(shop_list)

@app.route('/api/check_shopid', methods=['POST'])
def check_shopid():
    shopid=request.form.get('shopid')
    shop_list=get_items() #每次check调用一次数据库
    if int(shopid) in shop_list:
        return jsonify({'exist': True})
    else:
        return jsonify({'exist': False})

if __name__ == '__main__':
    app.run(debug=True, port=7001)