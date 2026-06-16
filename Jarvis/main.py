
from features.site_control import run_command
from features.temperature import get_weather
from listening import listen
from speak import speak
from features.Global_price import get_price

speak("hi")
while True :
    order = listen()
    if order != None:
        print(order)
        if "باز" in order:
            run_command(order)
        if "قیمت" in order :
            print("قیمت ها")
            get_price()
        elif order == "پایان":
            break
        

        
   
speak("bedrud")
