import os
import pandas as pd
from vnstock import *
import google.generativeai as genai

# Cấu hình Gemini AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Lấy dữ liệu VNINDEX
try:
    df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-06", "1D", "index")
    price = df.iloc[-1]['close']
    change = price - df.iloc[-2]['close']
except:
    price, change = "Không có dữ liệu", 0

# Nhờ AI viết nhận định
prompt = f"Chỉ số VN-Index hiện tại là {price}, biến động {change}. Viết 1 đoạn nhận định ngắn bằng tiếng Việt."
response = model.generate_content(prompt)
analysis = response.text

# Tạo file HTML để hiển thị lên web
html = f"<html><body><h1>Bản tin chứng khoán</h1><p>{analysis}</p></body></html>"
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
