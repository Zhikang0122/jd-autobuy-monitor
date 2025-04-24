import requests
from bs4 import BeautifulSoup
import re

# 商品页面
url = "https://npcitem.jd.hk/10148775088416.html"

# Server酱 SendKey
sckey = "SCT277418TPZW6vZxtP3h6v0eoti0O3yR7"  # ← 替换成你的 SendKey

# 设置价格阈值（单位：元）
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

    # 用正则从页面提取价格（适配京东页面的 ￥xx.xx）
    price_match = re.search(r'￥\s*([\d.]+)', text)
    if price_match:
        price = float(price_match.group(1))
        print(f"🔍 当前商品价格：￥{price}")
    else:
        print("❗ 无法提取商品价格")
        return

    # 判断库存关键词 + 价格
    if ("加入购物车" in text or "立即购买" in text) and price <= max_price:
        print("✅ 有货且原价合理，正在推送提醒...")

        title = f"📦 拍立得相纸补货！仅售￥{price}元"
        desp = f"[点击抢购链接]({url})"
        push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
        requests.get(push_url)
    elif price > max_price:
        print(f"⚠️ 有货但价格过高（￥{price}），不提醒")
    else:
        print("🚫 当前无货")

if __name__ == "__main__":
    check_stock()
