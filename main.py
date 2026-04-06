import os
from google import genai
from vnstock import *

# 1. Lấy API Key
api_key = os.environ.get("GEMINI_API_KEY")

def run_bot():
    try:
        if not api_key:
            return "LỖI: Chưa cấu hình GEMINI_API_KEY."
        
        # 2. Khởi tạo Client và ép sử dụng phiên bản API v1 ổn định
        client = genai.Client(
            api_key=api_key,
            http_options={'api_version': 'v1'}
        )
        
        # 3. Lấy dữ liệu VN-Index
        try:
            # Lấy dữ liệu gần nhất (thay đổi ngày theo thời gian thực nếu cần)
            df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-06", "1D", "index")
            price = df.iloc[-1]['close'] if not df.empty else "N/A"
            prompt = f"Chỉ số VN-Index hiện tại là {price}. Hãy viết 1 câu nhận định thị trường ngắn gọn."
        except:
            prompt = "Chào bạn, AI đã sẵn sàng phân tích chứng khoán cho bạn."

        # 4. Gọi AI
        response = client.models.generate_content(
            model="gemini-1.5-flash",
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
<body style='font-family: sans-serif; padding: 20px; line-height: 1.6;'>
    <h1 style='color: #1a73e8;'>Bản tin chứng khoán</h1>
    <div style='background: #f8f9fa; padding: 20px; border-left: 5px solid #1a73e8; border-radius: 4px;'>
        {result}
    </div>
    <p style='color: #666; font-size: 0.8em; margin-top: 20px;'>Cập nhật tự động bởi DrDStock Bot</p>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
