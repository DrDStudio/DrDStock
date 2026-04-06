import os
import pandas as pd
from vnstock import *
import google.generativeai as genai
from datetime import datetime, timedelta

# 1. Cấu hình AI
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    analysis = "LỖI: Chưa tìm thấy GEMINI_API_KEY trong mục Secrets của GitHub."
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 2. Lấy dữ liệu
        df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-06", "1D", "index")
        price = df.iloc[-1]['close'] if not df.empty else "N/A"
        
        # 3. Nhờ AI viết
        prompt = f"Chỉ số VN-Index hiện là {price}. Viết 1 đoạn ngắn nhận định thị trường."
        response = model.generate_content(prompt)
        analysis = response.text
    except Exception as e:
        analysis = f"LỖI KỸ THUẬT: {str(e)}"

# 4. Tạo HTML
html_content = f"<html><head><meta charset='utf-8'></head><body><h1>Bản tin chứng khoán</h1><p>{analysis}</p></body></html>"
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
