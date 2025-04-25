import requests

# ✅ 腾讯云代理的 API 地址（代理了京东 p.3.cn 接口）
proxy_api_url = "http://1356392297-2qzwoew2rb.ap-guangzhou.tencentscf.com/jd-price?sku=10148775088416"

# ✅ 原商品详情页（用于 Server酱推送里的跳转链接）
jd_url = "https://npcitem.jd.hk/10148775088416.html"

# ✅ Server酱 SendKey（推送到你微信）
sckey = "SCT277418TPZW6vZxtP3h6v0eoti0O3yR7"

# ✅ 接受的最高价格
max_price = 80.0

def check_stock():
    try:
        response = requests.get(proxy_api_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ 获取价格失败，状态码：{response.status_code}")
            return

        data = response.json()
        price = float(data.get("p", -1))  # 获取价格字段

        print(f"💰 当前价格：￥{price}")

        # ✅ 判断价格
        if 0 < price <= max_price:
            print("✅ 补货原价命中！准备推送微信提醒...")

            title = f"📦 拍立得相纸补货！￥{price} 元"
            desp = f"[👉 点我立即抢购]({jd_url})"
            push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
            push_res = requests.get(push_url)
            print("📬 推送结果：", push_res.text)
        elif price > max_price:
            print(f"⚠️ 当前价格 ￥{price} 超过原价 ￥{max_price}，不提醒")
        else:
            print("🚫 暂时无货或未能成功获取价格")

    except Exception as e:
        print("❌ 脚本异常：", e)

if __name__ == "__main__":
    check_stock()
