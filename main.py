import os
from vnstock import *
import google.generativeai as genai

# 1. Kiểm tra API Key có tồn tại không
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    # Nếu không thấy Key, in thông báo này ra file HTML luôn
    result = "LỖI: GitHub chưa nhận được API Key. Hãy kiểm tra lại mục Secrets."
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 2. Thử một câu lệnh đơn giản nhất để test AI
        response = model.generate_content("Chào bạn, hãy viết 1 câu ngắn về chứng khoán.")
        result = response.text
    except Exception as e:
        # Nếu AI từ chối hoặc lỗi Key, in lỗi cụ thể ra đây
        result = f"LỖI TỪ GOOGLE AI: {str(e)}"

# 3. Xuất ra file HTML
html_content = f"<html><head><meta charset='utf-8'></head><body><h1>Kết quả kiểm tra</h1><p>{result}</p></body></html>"
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
