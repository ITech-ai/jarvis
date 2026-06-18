import threading
import time
import webview

from features.ai import ask_jarvis  
from features.G_S_i import get_SI
from features.Global_price import get_price
from features.site_control import run_command
from features.temperature import get_weather
from features.translator import transletor
from listening import listen
from speak import speak as original_speak

jarvis_window = None

# ⚙️ کلاس API برای ایجاد پل ارتباطی بین جاوااسکریپت (فرانت) و پایتون (بک‌اند)
class JarvisAPI:
    def process_text_input(self, text):
        threading.Thread(target=generate_ai_response, args=(text,), daemon=True).start()


# 🧠 موتور پردازش و هماهنگی پاسخ هوش مصنوعی (مشترک برای متن و صوت)
def generate_ai_response(user_text):
    global jarvis_window
    if not user_text.strip():
        return

    # نمایش متن کاربر در بخش چت داشبورد و ترمینال صوتی
    ui_add_message(user_text, 'user')

    try:
        # روشن کردن انیمیشنِ حرکت سریع هسته ۳ بعدی (حالت در حال صحبت)
        if jarvis_window:
            jarvis_window.evaluate_js("setSpeakingState(true);")

        # فراخوانی ماژول هوش مصنوعی مستقل شما و دریافت پاسخ از Groq
        bot_reply = ask_jarvis(user_text)

        if bot_reply:
            # ارسال پاسخ به فرانت‌بند جهت تایپ افکت‌دار روی مانیتورها
            ui_add_message(bot_reply, 'jarvis')
            # خواندن صوتی پاسخ توسط جارویس
            original_speak(bot_reply)

    except Exception as e:
        print(f"AI Execution Error: {e}")
        ui_add_message("System error in processing data stream, sir.", 'jarvis')
    
    finally:
        # برگرداندن انیمیشن هسته ۳ بعدی به حالت عادی (حالت آماده‌به‌کار)
        if jarvis_window:
            jarvis_window.evaluate_js("setSpeakingState(false);")


# 📊 تِرد مدیریت داشبورد: مانیتورینگ منابع سخت‌افزاری و دریافت اطلاعات شبکه
def dashboard_updater():
    global jarvis_window
    # زمان معطلی اولیه برای اینکه مطمئن شویم پوسته و فریم‌ها کاملاً لود شده‌اند
    time.sleep(5)  
    
    counter = 0
    while True:
        if jarvis_window:
            try:
                # دریافت اطلاعات منابع سیستم با استفاده از تابع بهینه‌شده شما
                sys_info = get_SI()
                if sys_info:
                    cpu = sys_info.get("cpu", 0)
                    ram = sys_info.get("ram", 0)
                    disk = sys_info.get("disk", 0)
                    gpu = sys_info.get("gpu", 0)
                    ip = sys_info.get("ip", "Scanning...")
                    
                    # تزریق تله‌متری سیستم به فرانت‌بند
                    jarvis_window.evaluate_js(
                        f"updateSystemStats('{cpu}', '{ram}', '{disk}', '{gpu}', '{ip}');"
                    )

                if counter % 150 == 0:
                    weather_data = get_weather() 
                    if weather_data:
                        city, temp, humidity, condition = weather_data
                        jarvis_window.evaluate_js(f"updateWeather('{city}', '{temp}', '{humidity}', '{condition}');")
                    
                    price_data = get_price() 
                    if price_data:
                        gold = price_data.get("gold", "---")
                        coin = price_data.get("coin", "---")
                        usd = price_data.get("dollar", "---")
                        jarvis_window.evaluate_js(f"updatePrices('{usd}', '{coin}', '{gold}');")
                    
            except Exception as e:
                print(f"Dashboard Telemetry Error: {e}")
                
        counter += 1
        time.sleep(2)  


def ui_add_message(text, sender):
    global jarvis_window
    if jarvis_window:
        safe_text = text.replace("'", "\\'").replace("\n", " ").replace("\r", "")
        jarvis_window.evaluate_js(f"addUserMessage('{safe_text}', '{sender}');")


def speak(text):
    global jarvis_window
    if jarvis_window:
        jarvis_window.evaluate_js("setSpeakingState(true);")
        ui_add_message(text, 'jarvis')
    original_speak(text)
    if jarvis_window:
        jarvis_window.evaluate_js("setSpeakingState(false);")


def jarvis_core_logic():
    global jarvis_window
    time.sleep(1.5)  
    speak("Systems online. Jarvis mainframe initialized, sir.")

    while True:
        order = listen()
        if order is not None:
            print(f"Voice Command: {order}")
            if order =="سلام":
                ui_add_message(order, 'user')
                speak("hi sir, how can i help you today")
               
            if "باز" in order:
                ui_add_message(order, 'user')
                run_command(order)
            elif "ترجمه" in order:
                ui_add_message(order, 'user')
                pass
            elif order == "پایان":
                speak("thank you sir, shuting down")
                break


    if jarvis_window:
        jarvis_window.destroy()  


if __name__ == "__main__":
    api = JarvisAPI()
    
    jarvis_window = webview.create_window(
        title="JARVIS AI Core",
        url="UI/UI_v2/main.html",  
        js_api=api,  
        width=1500,
        height=900,
        resizable=True,
        fullscreen=True, 
        background_color="#000000",
    )


    threading.Thread(target=jarvis_core_logic, daemon=True).start()
    threading.Thread(target=dashboard_updater, daemon=True).start()
    webview.start()