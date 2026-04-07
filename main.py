import os
from google import genai
from vnstock import *

# 1. Lấy API Key
api_key = os.environ.get("GEMINI_API_KEY")

def run_bot():
    try:
        if not api_key:
            return "LỖI: Chưa cấu hình GEMINI_API_KEY."
        
        # 2. Khởi tạo Client
        client = genai.Client(api_key=api_key)
        
        # 3. Lấy dữ liệu VN-Index
        try:
            df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-07", "1D", "index")
            price = df.iloc[-1]['close'] if not df.empty else "N/A"
            prompt = f"Chỉ số VN-Index hiện tại là {price}. Hãy viết 1 câu nhận định thị trường ngắn gọn."
        except:
            prompt = "Chào bạn, bot chứng khoán đã sẵn sàng phân tích!"

        # 4. Gọi AI với "Tên đầy đủ" để tránh lỗi 404
        # Chúng ta dùng cấu trúc 'models/gemini-1.5-flash' thay vì chỉ tên
        response = client.models.generate_content(
            model="models/gemini-1.5-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        # Nếu vẫn lỗi, thử dùng model dự phòng cực thấp
        return f"LỖI HỆ THỐNG: {str(e)}"

# Ghi ra file HTML (Giữ nguyên giao diện đẹp tối qua)
result = run_bot()
html_content = f"""
<html>
<head><meta charset='utf-8'><title>DrDStock</title></head>
<body style='font-family: sans-serif; padding: 30px; line-height: 1.6; max-width: 800px; margin: auto;'>
    <h1 style='color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px;'>Bản tin chứng khoán</h1>
    <div style='background: #f8f9fa; padding: 20px; border-left: 5px solid #1a73e8; border-radius: 4px; font-size: 1.2em;'>
        {result}
    </div>
    <p style='color: #666; font-size: 0.8em; margin-top: 30px;'>Cập nhật tự động bởi hệ thống DrDStock</p>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
