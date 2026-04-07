import os
import google.generativeai as genai
from vnstock import *

# 1. Lấy API Key từ Secrets
api_key = os.environ.get("GEMINI_API_KEY")

def run_bot():
    try:
        if not api_key:
            return "LỖI: Chưa cấu hình GEMINI_API_KEY."
        
        # 2. Cấu hình cực kỳ chặt chẽ: Dùng REST thay vì gRPC để tránh lỗi 404 v1beta
        genai.configure(api_key=api_key, transport='rest')
        
        # 3. Khởi tạo model với tên đầy đủ
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 4. Lấy dữ liệu VN-Index (thử nghiệm với ngày gần nhất)
        try:
            df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-07", "1D", "index")
            price = df.iloc[-1]['close'] if not df.empty else "N/A"
            prompt = f"Chỉ số VN-Index hiện tại là {price}. Hãy viết 1 câu nhận định ngắn gọn."
        except:
            prompt = "Chào bạn, AI đã sẵn sàng hoạt động!"

        # 5. Gọi AI
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LỖI HỆ THỐNG MỚI: {str(e)}"

# Ghi ra file HTML để hiển thị lên Web
result = run_bot()
html_content = f"""
<html><head><meta charset='utf-8'></head>
<body style='font-family: sans-serif; padding: 20px;'>
    <h1>Bản tin chứng khoán DrDStock</h1>
    <div style='background: #f0f0f0; padding: 15px; border-radius: 5px;'>{result}</div>
</body></html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
