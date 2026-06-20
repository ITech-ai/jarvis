import re
import requests

def get_price():
    try:
        res = requests.get("https://www.tgju.org/", timeout=5)
        tag1 = re.findall('<span class="info-price">(.*)</span>', res.text)
        
        data = {
            "gold": tag1[3],
            "coin": tag1[4],
            "dollar": tag1[5]
        }
        return data
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None
