import requests
from bs4 import BeautifulSoup

# ✅ 使用京东国际商品页面
url = "https://npcitem.jd.hk/10148775088416.html"

# ✅ 替换为你的真实 Server酱 SendKey（SCT 开头）
sckey = "SCT277418TPZW6vZxtP3h6v0eoti0O3yR7"

def check_stock():
    # ✅ 模拟 PC 浏览器访问，避免跳转
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

    # ✅ 页面调试预览（前 1000 字符）
    print("🧾 页面预览（前1000字）：")
    print(response.text[:1000])
    print("-" * 60)

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.text

    # ✅ 判断关键词（适配海外购）
    if "到货通知" in text or "无货" in text:
        print("🚫 当前无货")
    elif ("加入购物车" in text or "立即购买" in text or 
          "去结算" in text or "购物车" in text):
        print("✅ 检测到补货！正在推送微信提醒...")

        title = "📦 拍立得国际版相纸补货啦！"
        desp = f"[点我立即抢购]({url})"
        push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
        requests.get(push_url)
    else:
        print("⚠️ 状态未知，请手动检查页面")

if __name__ == "__main__":
    check_stock()
