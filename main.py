import os
import google.generativeai as genai  # Quay lại dùng thư viện này nhưng cấu hình kỹ hơn

# 1. Lấy API Key
api_key = os.environ.get("GEMINI_API_KEY")

def run_bot():
    try:
        if not api_key:
            return "LỖI: Chưa có API Key trong Secrets."
        
        # 2. Cấu hình trực tiếp
        genai.configure(api_key=api_key)
        
        # 3. Chọn đúng model bằng tên chuẩn
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 4. Gửi tin nhắn đơn giản nhất
        response = model.generate_content("Chào bạn, hãy viết 1 câu chúc ngày mới tốt lành.")
        return response.text
    except Exception as e:
        return f"LỖI THỰC TẾ: {str(e)}"

# Ghi ra HTML
result = run_bot()
with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"<html><head><meta charset='utf-8'></head><body><h1>Kết quả:</h1><p>{result}</p></body></html>")
