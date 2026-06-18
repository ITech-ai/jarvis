from groq import Groq

# راه‌اندازی کلاینت با کلید شما
client = Groq(api_key="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")

# حافظه موقت و تاریخچه پیام‌ها برای حفظ روند گفت‌وگو
messages_history = [
    {
        "role": "system", 
        "content": "You are Jarvis, a highly intelligent, witty, and helpful AI assistant. Keep your answers concise, professional, and powerful. you sed just a very shor ansowr im from iran"
    }
]

def ask_jarvis(user_input):

    global messages_history
    
    if not user_input or not user_input.strip():
        return None
        
    # اضافه کردن پیام کاربر به هیستوری
    messages_history.append({"role": "user", "content": user_input})

    try:
        # ارسال درخواست به ال‌ال‌ام
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=messages_history
        )
        
        bot_reply = response.choices[0].message.content
        
        # اضافه کردن پاسخ بات به هیستوری برای دفعات بعدی
        messages_history.append({"role": "assistant", "content": bot_reply})
        
        return bot_reply

    except Exception as e:
        print(f"Error in Groq API: {e}")
        return "System error in processing data stream, sir."
