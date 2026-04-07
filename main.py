import os
import google.generativeai as genai
from vnstock import *

# 1. Lấy API Key
api_key = os.environ.get("GEMINI_API_KEY")

def run_analysis():
    try:
        if not api_key:
            return "LỖI: Thiếu API Key trong GitHub Secrets."
            
        # 2. Cấu hình và ÉP sử dụng phiên bản v1 ổn định
        # Đây là chìa khóa để hết lỗi 404 v1beta trong ảnh của bạn
        genai.configure(api_key=api_key, transport='rest')
        
        # 3. Khởi tạo model với tên đầy đủ
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash'
        )
        
        # 4. Chuẩn bị nội dung
        try:
            df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-07", "1D", "index")
            price = df.iloc[-1]['close'] if not df.empty else "N/A"
            prompt = f"Chỉ số VN-Index là {price}. Nhận định ngắn 1 câu."
        except:
            prompt = "Chào bạn, AI đã sẵn sàng!"

        # 5. Gọi AI (Sử dụng tham số hỗ trợ bản v1)
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"LỖI TẠI BẢN V1: {str(e)}"

# Ghi file HTML
content = run_analysis()
html = f"<html><body style='font-family:sans-serif;padding:30px;'><h1>Bản tin DrDStock</h1><p>{content}</p></body></html>"
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
