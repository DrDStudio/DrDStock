import os
from google import genai
from vnstock import *

# 1. Lấy API Key
api_key = os.environ.get("GEMINI_API_KEY")

def run_bot():
    try:
        if not api_key:
            return "LỖI: Chưa cấu hình GEMINI_API_KEY."
        
        # 2. Khởi tạo Client (Sử dụng model mặc định ổn định)
        client = genai.Client(api_key=api_key)
        
        # 3. Lấy dữ liệu VN-Index (Dùng try-except để tránh lỗi ngày nghỉ)
        try:
            df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-06", "1D", "index")
            price = df.iloc[-1]['close'] if not df.empty else "N/A"
            prompt = f"Chỉ số VN-Index hiện tại là {price}. Hãy viết 1 câu nhận định thị trường ngắn gọn."
        except:
            prompt = "Chào bạn, AI đã sẵn sàng phân tích chứng khoán cho bạn."

        # 4. Gọi AI với cấu hình model chuẩn
        response = client.models.generate_content(
            model="gemini-1.5-flash", # Hoặc bạn có thể thử "gemini-2.0-flash"
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"LỖI HỆ THỐNG: {str(e)}"

# Ghi ra file HTML
result = run_bot()
html_content = f"""
<html>
<head><meta charset='utf-8'><title>DrDStock</title></head>
<body style='font-family: sans-serif; padding: 20px;'>
    <h1>Bản tin chứng khoán</h1>
    <div style='background: #f4f4f4; padding: 15px; border-radius: 5px;'>
        {result}
    </div>
    <p style='color: gray; font-size: 0.8em;'>Cập nhật lúc: 2026-04-06</p>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
