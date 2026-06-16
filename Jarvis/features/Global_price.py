import re
import requests
from tkinter import *
from PIL import Image,ImageTk
res=requests.get("https://www.tgju.org/")
def get_price():
   
    tag1=re.findall('<span class="info-price">(.*)</span>',res.text)
 
    print(f"gold : {tag1[3]}")
    print(f"coin : {tag1[4]}")
    print(f"dolor : {tag1[5]}")

