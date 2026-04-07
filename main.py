import os
import google.generativeai as genai
from vnstock import *

# 1. Cấu hình API
api_key = os.environ.get("GEMINI_API_KEY")

def run_analysis():
    try:
        if not api_key:
            return "LỖI: Thiếu API Key trong GitHub Secrets."
            
        genai.configure(api_key=api_key)
        
        # 2. Ép sử dụng model chuẩn nhất
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. Lấy dữ liệu chứng khoán
        try:
            df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-07", "1D", "index")
            price = df.iloc[-1]['close'] if not df.empty else "N/A"
            msg = f"Chỉ số VN-Index hiện tại là {price}. Viết 1 câu nhận định ngắn."
        except:
            msg = "Chào bạn, AI đã kết nối thành công và sẵn sàng phân tích."

        # 4. Gửi yêu cầu cho AI
        response = model.generate_content(msg)
        return response.text
        
    except Exception as e:
        # Nếu vẫn lỗi 404, in ra chi tiết để xử lý
        return f"LỖI TỪ GOOGLE: {str(e)}"

# Ghi file HTML
content = run_analysis()
html = f"""
<html><head><meta charset='utf-8'></head>
<body style='font-family:sans-serif; padding:30px;'>
    <h1 style='color:#1a73e8;'>Bản tin DrDStock</h1>
    <div style='padding:20px; border-left:5px solid #1a73e8; background:#f8f9fa;'>
        {content}
    </div>
</body></html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
