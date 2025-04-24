import requests
from bs4 import BeautifulSoup

# 商品页面链接（标准 JD 商品页）
url = "https://item.jd.com/614833.html"

# Server酱 SendKey（请替换为你的真实 key）
sckey = "SCTxxxxxxxxxxxxxxxxxxxxx"

def check_stock():
    # 使用更强的浏览器模拟 headers，避免被跳转到移动端
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://item.jd.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print("❌ 页面请求失败")
        return

    # 打印页面前1000字符用于调试
    print("🧾 页面预览（前1000字）：")
    print(response.text[:1000])
    print("-" * 60)

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.text

    # 判断关键词
    if "到货通知" in text or "无货" in text:
        print("🚫 当前无货")
    elif "加入购物车" in text or "立即购买" in text or "购买" in text:
        print("✅ 检测到补货！正在推送微信提醒...")

        title = "📦 拍立得相纸补货啦！（京东自营）"
        desp = f"[点我立即抢购]({url})"
        push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
        requests.get(push_url)
    else:
        print("⚠️ 状态未知，请手动检查页面")

if __name__ == "__main__":
    check_stock()
