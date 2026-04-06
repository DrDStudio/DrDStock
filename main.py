import os
from google import genai  # Cấu trúc mới của thư viện google-genai
from vnstock import *

# 1. Lấy API Key từ Secrets
api_key = os.environ.get("GEMINI_API_KEY")

def run_bot():
    try:
        if not api_key:
            return "LỖI: Chưa cấu hình GEMINI_API_KEY trong Secrets."
        
        # 2. Khởi tạo Client theo chuẩn mới nhất
        client = genai.Client(api_key=api_key)
        
        # 3. Thử lấy dữ liệu chứng khoán (nếu có)
        try:
            df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-06", "1D", "index")
            current_price = df.iloc[-1]['close'] if not df.empty else "N/A"
            prompt = f"Chỉ số VN-Index hiện tại là {current_price}. Viết 1 câu nhận định ngắn."
        except:
            prompt = "Chào bạn, hãy viết 1 câu chúc mừng trang web chứng khoán đã hoạt động."

        # 4. Gọi AI
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"LỖI HỆ THỐNG: {str(e)}"

# Ghi kết quả ra HTML
result = run_bot()
with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"<html><head><meta charset='utf-8'></head><body><h1>Bản tin chứng khoán</h1><p>{result}</p></body></html>")
