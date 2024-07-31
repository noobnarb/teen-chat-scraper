import requests
import json
import time
import os

url = "https://www.teen-chat.org/chat/system/action/chat_log.php"
payload = {
    "token": "Change To Yours",
    "cp": "chat",
    "fload": "1",
    "caction": "113401166",
    "last": "46239241",
    "preload": "0",
    "priv": "6025243",
    "lastp": "57001522",
    "pcount": "1599",
    "room": "1",
    "notify": "14",
    "curset": "201"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.teen-chat.org",
    "Connection": "keep-alive",
    "Referer": "https://www.teen-chat.org/chat/",
    "Cookie": "Change To Yours",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

def scrape_and_save():
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            
            if "check" in data and data["check"] == 99:
                print("No new data retrieved. Response contains 'check': 99")
            else:
                if os.path.exists("chat_log.json"):
                    with open("chat_log.json", "r") as json_file:
                        existing_data = json.load(json_file)
                else:
                    existing_data = {"mlogs": [], "plogs": []}

                combined_logs = {
                    "mlogs": existing_data["mlogs"] + data.get("mlogs", []),
                    "plogs": existing_data["plogs"] + data.get("plogs", [])
                }

                combined_logs["mlogs"] = remove_duplicates(combined_logs["mlogs"])
                combined_logs["plogs"] = remove_duplicates(combined_logs["plogs"])

                with open("chat_log.json", "w") as json_file:
                    json.dump(combined_logs, json_file, indent=4)
                
                print("Updated chat_log.json")
        except json.JSONDecodeError as e:
            print("Failed to decode JSON response.")
            print(f"Error: {e}")
            print(f"Response content: {response.content[:500]}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(f"Response: {response.text}")

def remove_duplicates(logs):
    unique_logs = []
    seen = set()
    
    for log in logs:
        log_tuple = (
            log.get("log_id"),
            log.get("user_name"),
            log.get("user_age"),
            log.get("user_gender"),
            log.get("user_country"),
            log.get("log_content"),
            log.get("log_date")
        )
        
        if log_tuple not in seen:
            seen.add(log_tuple)
            unique_logs.append(log)
    
    return unique_logs

try:
    while True:
        scrape_and_save()
        time.sleep(3)
except KeyboardInterrupt:
    print("I COMMAND YOU TO STOP!")
