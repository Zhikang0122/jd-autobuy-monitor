import requests
from bs4 import BeautifulSoup

# 商品页面链接（建议用京东 item.jd.com 标准链接）
url = "https://item.jd.com/614833.html"

# Server酱 SendKey
sckey = "SCTxxxxxxxxxxxxxxxxxxxxx"  # 👈 替换成你的 SendKey

def check_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print("❌ 页面请求失败")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.text

    # 判断库存状态
    if "到货通知" in text or "无货" in text:
        print("🚫 当前无货")
    elif "加入购物车" in text:
        print("✅ 检测到补货！正在推送微信提醒...")

        title = "📦 拍立得相纸补货啦！（京东自营）"
        desp = f"[点我立即抢购]({url})"
        push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
        requests.get(push_url)
    else:
        print("⚠️ 状态未知，请手动检查页面")

if __name__ == "__main__":
    check_stock()
