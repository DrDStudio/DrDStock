import os
from google import genai
from vnstock import *

# 1. Lấy API Key
api_key = os.environ.get("GEMINI_API_KEY")

try:
    if not api_key:
        result = "LỖI: Chưa cấu hình GEMINI_API_KEY trong Settings/Secrets."
    else:
        # 2. Cấu hình Client mới theo chuẩn Google 2026
        client = genai.Client(api_key=api_key)
        
        # 3. Gửi yêu cầu (Sử dụng model gemini-2.0-flash hoặc 1.5)
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Chào bạn, AI đã hoạt động rồi!"
        )
        result = response.text
except Exception as e:
    result = f"LỖI KỸ THUẬT MỚI: {str(e)}"

# 4. Ghi file HTML
with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"<html><head><meta charset='utf-8'></head><body><p>{result}</p></body></html>")
