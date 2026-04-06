import os
import pandas as pd
from vnstock import *
import google.generativeai as genai

# 1. Cấu hình AI
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Lấy dữ liệu thị trường (Ví dụ VNINDEX)
try:
    # Lấy dữ liệu 2 phiên gần nhất để so sánh
    df = stock_historical_data("VNINDEX", "2026-04-01", "2026-04-06", "1D", "index")
    latest_price = df.iloc[-1]['close']
    change = latest_price - df.iloc[-2]['close']
    status = "tăng" if change > 0 else "giảm"
except Exception as e:
    latest_price, change, status = "N/A", "N/A", "N/A"

# 3. Nhờ AI viết nhận định
prompt = f"Chỉ số VN-Index hiện tại là {latest_price}, biến động {change} ({status}). Hãy viết một bản tin ngắn gọn về thị trường chứng khoán Việt Nam hôm nay, giọng văn chuyên nghiệp, súc tích."
response = model.generate_content(prompt)
analysis = response.text

# 4. Tạo giao diện HTML
html_content = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Bản Tin Chứng Khoán DrDStock</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
</head>
<body>
    <h1>Báo Cáo Thị Trường Chứng Khoán</h1>
    <p><i>Cập nhật ngày: {pd.Timestamp.now().strftime('%d/%m/%Y')}</i></p>
    <div style="padding: 20px; border-radius: 10px; background: #f0f0f0; color: #333">
        <h2>VN-Index: {latest_price} ({'+' if status == 'tăng' else ''}{change})</h2>
        <p><strong>Phân tích từ AI:</strong></p>
        <p>{analysis}</p>
    </div>
    <hr>
    <p>Hệ thống cập nhật tự động.</p>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
