import requests
from bs4 import BeautifulSoup
import re

# ✅ 商品页面（你要抢的相纸链接）
url = "https://npcitem.jd.hk/10148775088416.html"

# ✅ Server酱 SendKey（自动推送到微信）
sckey = "SCT277418TPZW6vZxtP3h6v0eoti0O3yR7"

# ✅ 设置最高接受价格（单位：元）
max_price = 80

def check_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://item.jd.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("❌ 请求失败：", e)
        return

    if response.status_code != 200:
        print(f"❌ 页面请求失败，状态码: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.text

    # ✅ 提取价格：从 JavaScript 数据中匹配 "price": "xx.xx"
    price_match = re.search(r'"price"\s*:\s*"([\d.]+)"', response.text)
    if price_match:
        price = float(price_match.group(1))
        print(f"🔍 当前商品价格：￥{price}")
    else:
        print("❌ 无法提取商品价格")
        return

    # ✅ 判断是否有货 + 是否为原价
    if ("加入购物车" in text or "立即购买" in text) and price <= max_price:
        print("✅ 有货且价格合适，正在推送提醒...")

        title = f"📦 拍立得相纸补货！￥{price} 元"
        desp = f"[点我抢购]({url})"
        push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
        requests.get(push_url)
    elif price > max_price:
        print(f"⚠️ 有货但价格过高（￥{price} > ￥{max_price}），不推送")
    else:
        print("🚫 当前无货")

if __name__ == "__main__":
    check_stock()
