import requests
from bs4 import BeautifulSoup
import re

# ✅ 商品信息
url = "https://npcitem.jd.hk/10148775088416.html"
sku_id = "10148775088416"
max_price = 80.0  # 接受的最高价格

# ✅ 你的 Server酱 SendKey
sckey = "SCT277418TPZW6vZxtP3h6v0eoti0O3yR7"

def check_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://item.jd.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    # ✅ 第一步：获取商品页面文本（用来判断是否有货）
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("❌ 页面请求失败：", e)
        return

    if response.status_code != 200:
        print(f"❌ 页面状态码异常：{response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.text

    # ✅ 第二步：调用京东价格接口获取当前价格
    price_api = f"https://p.3.cn/prices/mgets?skuIds=J_{sku_id}"
    try:
        price_response = requests.get(price_api, timeout=5)
        price_json = price_response.json()
        price = float(price_json[0]['p'])
        print(f"💰 当前价格：￥{price}")
    except Exception as e:
        print("❌ 获取价格失败：", e)
        return

    # ✅ 第三步：判断是否有货 + 价格是否符合
    if ("加入购物车" in text or "立即购买" in text) and price <= max_price:
        print("✅ 有货且价格合适，准备推送提醒...")

        title = f"📦 拍立得相纸补货！￥{price} 元"
        desp = f"[点我抢购 >>]({url})"
        push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
        requests.get(push_url)
    elif price > max_price:
        print(f"⚠️ 有货但价格￥{price} 超过阈值￥{max_price}，不提醒")
    else:
        print("🚫 当前无货")

if __name__ == "__main__":
    check_stock()
