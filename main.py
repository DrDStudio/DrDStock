import os
import requests
import json
from vnstock import *

# 1. Lấy thông tin
api_key = os.environ.get("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

def run_bot():
    try:
        if not api_key:
            return "LỖI: Chưa có API Key."

        # 2. Lấy dữ liệu chứng khoán
        try:
            df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-07", "1D", "index")
            price = df.iloc[-1]['close'] if not df.empty else "N/A"
            prompt = f"Chỉ số VN-Index hiện tại là {price}. Hãy viết 1 câu nhận định ngắn gọn bằng tiếng Việt."
        except:
            prompt = "Chào bạn, AI đã hoạt động. Chúc bạn một ngày tốt lành!"

        # 3. Gọi trực tiếp đến Google API (Ép dùng bản v1)
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()

        if response.status_code == 200:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"LỖI API {response.status_code}: {data.get('error', {}).get('message', 'Không xác định')}"

    except Exception as e:
        return f"LỖI HỆ THỐNG: {str(e)}"

# Ghi kết quả
result = run_bot()
html = f"<html><head><meta charset='utf-8'></head><body style='padding:20px;'><h1>DrDStock</h1><p>{result}</p></body></html>"
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
