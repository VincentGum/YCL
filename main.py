import json
import os
import time
import sys

import requests
from bs4 import BeautifulSoup

urlRoot = "http://shop.tfent.cn/GoodsCategory"
category = {
    "TNT": "stationery",
}

def getProductList():
    # 请求网页
    try:
        currentRoot = os.path.join(urlRoot, category["TNT"])
        rsp = requests.get(currentRoot)
    except:
        print("===== ❌ 请 求 失 败 ❌ =====")
        sys.exit("===== ⚠️ 终 止 运 行 ⚠️ =====")

    if rsp.status_code != 200:
        print("===== ❌ 请 求 失 败 ❌ =====")
        sys.exit("===== ⚠️ 终 止 运 行 ⚠️ =====")

    # 解析html内容
    try:
        soup = BeautifulSoup(rsp.content, 'html.parser')
        listBox = soup.find_all("div", {"class": "floor floor2"})
        productList = listBox[0].find_all("li")

        # 解析产品url及id
        productURL = []
        for product in productList:
            a = product.find("a", href=True)
            productURL.append(a["href"].split("id=")[1])

        return productURL
    except:
        print("===== ❌ 解 析 错 误 ❌ =====")
        sys.exit("===== ⚠️ 终 止 运 行 ⚠️ =====")


if __name__ == "__main__":

    print("===== 🐞 开 始 进 行 爬 取 🐞 =====")

    firstProducts = getProductList()
    historyP = [item for item in firstProducts]
    print("进行了第 1 次爬取，当前的产品ID为：{}".format(",".join(historyP)))

    count = 1
    while True:
        time.sleep(60)
        count += 1

        print("===== 🐞 进 行 第 {} 次 爬 取 🐞 =====".format(count))
        newProducts = getProductList()

        for newP in newProducts:
            if newP not in historyP:
                print("☎️发现新产品：{}".format(newP))
                # SendMessage() 进行通知，待实现
                historyP.append(newP)
                historyP = historyP.sort()
        print("进行了第 {} 次爬取，当前的产品ID为：{}".format(count, ",".join(historyP)))
        # if count == 3:
        #     break

