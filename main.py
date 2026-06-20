import threading
import time
import json 
import webview
from features.daily_schedule import read_schedule, write_schedule
from features.ai import ask_jarvis  
from features.G_S_i import get_SI
from features.Global_price import get_price
from features.site_control import run_command
from features.temperature import get_weather
from features.translator import transletor
from listening import listen
from speak import speak as original_speak

jarvis_window = None

class JarvisAPI:
    def process_text_input(self, text):
        threading.Thread(target=generate_ai_response, args=(text,), daemon=True).start()

def generate_ai_response(user_text):

    global jarvis_window
    if not user_text.strip():
        return

    ui_add_message(user_text, 'user')

    try:
        if jarvis_window:
            jarvis_window.evaluate_js("setSpeakingState(true);")

        bot_reply = ask_jarvis(user_text)

        if bot_reply:
            ui_add_message(bot_reply, 'jarvis')
            original_speak(bot_reply)

    except Exception as e:
        print(f"AI Execution Error: {e}")
        ui_add_message("System error in processing data stream, sir.", 'jarvis')
    
    finally:
        if jarvis_window:
            jarvis_window.evaluate_js("setSpeakingState(false);")

def dashboard_updater():
    global jarvis_window
    counter = 0
    while True:
    
        if jarvis_window:
            try:
                if counter % 50 == 0:
                    sys_info = get_SI()
                    if sys_info:
                        cpu = sys_info.get("cpu", 0)
                        ram = sys_info.get("ram", 0)
                        disk = sys_info.get("disk", 0)
                        gpu = sys_info.get("gpu", 0)
                        ip = sys_info.get("ip", "Scanning...")
                        jarvis_window.evaluate_js(
                            f"updateSystemStats('{cpu}', '{ram}', '{disk}', '{gpu}', '{ip}');"
                        )
                    weather_data = get_weather() 
                    if weather_data:
                        city = weather_data.get("city" , "---")
                        temp = weather_data.get("temp" , "---")
                        humidity = weather_data.get("humidity" , "---")
                        condition = weather_data.get("condition" , "---")
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

def ui_add_message(text, sender):
    global jarvis_window
    if jarvis_window:
        safe_text = json.dumps(text)[1:-1]
        jarvis_window.evaluate_js(f"addUserMessage('{safe_text}', '{sender}');")

def speak(text):
    global jarvis_window
    if jarvis_window:
        jarvis_window.evaluate_js("setSpeakingState(true);")
        ui_add_message(text, 'jarvis')
    original_speak(text)
    if jarvis_window:
        jarvis_window.evaluate_js("setSpeakingState(false);")

def schedule():
    speak("what do you want to do, sir")
    option = listen()
    print(option)
    if not option:
        return
    if "خروج" in option:
        pass
    elif "ببینم" in option:
        while True:
        
            speak("say day, sir") 
            myday = listen()      
            if myday is not None:
                day = transletor(myday)
                speak(transletor(myday))
                speak(read_schedule(day))
                
                break
    elif "تغییر" in option:
        pass
    elif "حذف" in option:
        pass

def jarvis_core_logic():
    global jarvis_window
    speak("Systems online. Daruish mainframe initialized, sir.")
    
    while True:
        order = listen()
        print(order)
        if order is not None:
            print(f"Voice Command: {order}")
            if "سلام" in order:
                ui_add_message(order, 'user')
                speak("hi sir, how can i help you today")
               
            elif "باز" in order: 
                ui_add_message(order, 'user')
                run_command(order)
            
            elif "ترجمه" in order:
                print("translator mode")
                ui_add_message(order, 'user')
                while True:
                    speak("ok sir say your sentence")
                    trans = listen()
                    if trans == "خروج":
                        speak("exit translator mode")
                        break
                    elif trans:
                        ui_add_message(trans, 'user')
                        translated_text = transletor(trans)
                        speak(translated_text)
                        speak("finish the translate")
                        break
            
            elif "برنامه" in order:
                ui_add_message(order, 'user')
                schedule()
                        
            elif order == "پایان":
                ui_add_message(order, 'user')
                speak("thank you sir, shutting down")
                break
            else:
                ui_add_message(order, 'user')

    if jarvis_window:
        jarvis_window.destroy()  

if __name__ == "__main__":
    api = JarvisAPI()
    
    jarvis_window = webview.create_window(
        title="Dariush",
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