import os
import pandas as pd
from vnstock import *
import google.generativeai as genai
from datetime import datetime, timedelta

# 1. Cấu hình AI
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    print("Lỗi cấu hình API Key")

# 2. Lấy dữ liệu (Tự động lấy ngày gần nhất)
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')

try:
    df = stock_historical_data("VNINDEX", start_date, end_date, "1D", "index")
    if not df.empty:
        latest_price = df.iloc[-1]['close']
        change = latest_price - df.iloc[-2]['close']
        content_for_ai = f"VN-Index hiện tại: {latest_price}, biến động: {change}"
    else:
        content_for_ai = "Thị trường hôm nay chưa có dữ liệu mới."
except:
    content_for_ai = "Không thể kết nối dữ liệu chứng khoán."

# 3. Nhờ AI viết nhận định
try:
    prompt = f"{content_for_ai}. Viết 1 bản tin ngắn, súc tích về chứng khoán VN."
    response = model.generate_content(prompt)
    analysis = response.text
except:
    analysis = "AI đang bận, vui lòng quay lại sau."

# 4. Tạo giao diện HTML
html_content = f"<html><head><meta charset='utf-8'></head><body><h1>Bản tin chứng khoán</h1><p>{analysis}</p></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
