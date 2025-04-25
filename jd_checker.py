import requests
import time

# ✅ 中转 API 地址（腾讯云函数）
proxy_api = "http://1356392297-2qzwoew2rb.ap-guangzhou.tencentscf.com/jd-price"
sku_id = "10148775088416"
max_price = 80.0
sckey = "SCT277418TPZW6vZxtP3h6v0eoti0O3yR7"

def check_price():
    try:
        res = requests.get(f"{proxy_api}?sku={sku_id}", timeout=10)
        if res.status_code != 200:
            print(f"❌ 获取价格失败，状态码：{res.status_code}")
            return

        data = res.json()
        price_str = data.get("price")

        if not price_str:
            print("❌ 响应中未找到价格字段")
            return

        price = float(price_str)
        print(f"💰 当前价格：￥{price}")

        if price <= max_price:
            print("✅ 价格满足条件，准备推送微信提醒...")

            title = f"📦 拍立得相纸到货啦！￥{price}"
            desp = f"[点我立即抢购 >>](https://npcitem.jd.hk/{sku_id}.html)"
            push_url = f"https://sctapi.ftqq.com/{sckey}.send?title={title}&desp={desp}"
            requests.get(push_url)
        else:
            print(f"⚠️ 当前价格￥{price} 超出设置的阈值￥{max_price}，不提醒")

    except Exception as e:
        print("❌ 出现异常：", e)

if __name__ == "__main__":
    check_price()
