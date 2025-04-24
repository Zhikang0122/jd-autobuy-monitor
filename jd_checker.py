import requests
from bs4 import BeautifulSoup

# ✅ 使用 lite.jd.com 页面，适合脚本静态抓取
url = "https://lite.jd.com/614833.html"

# ✅ 替换为你自己的 Server酱 SendKey（SCT开头）
sckey = "SCT277418TPZW6vZxtP3h6v0eoti0O3yR7"

def check_stock():
    # 模拟真实浏览器访问，防止重定向到移动页面
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
        print(f"❌ 页面请求失败，状态码：{response.status_code}")
        return

    # ✅ 打印页面前1000字做调试
    print("🧾 页面预览（前1000字）：")
    print(response.text[:1000])
    print("-" * 60)

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.text

    # ✅ 检查库存关键词（可根据页面内容自定义更多）
    if "到货通知" in text or "无货" in text:
        print("🚫 当前无货")
    elif "加入购物车" in text or "立即购买" in text or "购买" in text:
        print("✅ 检测到补货！正在推送微信提醒...")

        title = "📦 拍立得相纸补货啦！（京东）"
        desp = f"[点我立即抢购]({url})"
        push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
        requests.get(push_url)
    else:
        print("⚠️ 状态未知，请手动检查页面")

if __name__ == "__main__":
    check_stock()
