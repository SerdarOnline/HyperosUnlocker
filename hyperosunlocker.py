import hashlib
import random
import time
import webbrowser
from datetime import datetime, timezone, timedelta
import ntplib
import pytz
import urllib3
import json
from icmplib import ping
from colorama import init, Fore, Style

init(autoreset=True)
col_g = Fore.GREEN 
col_gb = Style.BRIGHT + Fore.GREEN 
col_b = Fore.BLUE 
col_bb = Style.BRIGHT + Fore.BLUE 
col_y = Fore.YELLOW 
col_yb = Style.BRIGHT + Fore.YELLOW 
col_r = Fore.RED 
col_rb = Style.BRIGHT + Fore.RED 

ntp_servers = [
    "ntp0.ntp-servers.net", "ntp1.ntp-servers.net", "ntp2.ntp-servers.net",
    "ntp3.ntp-servers.net", "ntp4.ntp-servers.net", "ntp5.ntp-servers.net",
    "ntp6.ntp-servers.net"
]

mi_account_url = "https://account.xiaomi.com/fe/service/login/password?_locale=en_IN&checkSafePhone=false&sid=18n_bbs_global&qs=%253Fcallback%253Dhttps%25253A%25252F%25252Fsgp-api.buy.mi.com%25252Fbbs%25252Fapi%25252Fglobal%25252Fuser%25252Flogin-back%25253Ffollowup%25253Dhttps%2525253A%2525252F%2525252Fnew-ams.c.mi.com%2525252Fglobal%2525252F%252526sign%25253DM2UyYmIxZjc0MGQxODhkYjg3NWVlNDI4ZGQxNzk3ZmY3MThhYTVmNA%25252C%25252C%2526sid%253D18n_bbs_global%2526_locale%253Den_IN%2526checkSafePhone%253Dfalse&callback=https%3A%2F%2Fsgp-api.buy.mi.com%2Fbbs%2Fapi%2Fglobal%2Fuser%2Flogin-back%3Ffollowup%3Dhttps%253A%252F%252Fnew-ams.c.mi.com%252Fglobal%252F%26sign%3DM2UyYmIxZjc0MGQxODhkYjg3NWVlNDI4ZGQxNzk3ZmY3MThhYTVmNA%2C%2C&_sign=%2BnjnarFZlvmk2A9UJro3U%2BS0lbc%3D&serviceParam=%7B%22checkSafePhone%22%3Afalse%2C%22checkSafeAddress%22%3Afalse%2C%22lsrp_score%22%3A0.0%7D&showActiveX=false&theme=&needTheme=false&bizDeviceType="
webbrowser.open_new(mi_account_url)

print("Insert below the value of cookie [new_bbs_serviceToken]")
token_input = input("new_bbs_serviceToken: ")

print (col_y + f"Checking Account Status" + Fore.RESET)
cookie_value = token_input.strip()
feedtime = float(1400)
feed_time_shift = feedtime
feed_time_shift_1 = feed_time_shift / 1000

def generate_device_id():
    random_data = f"{random.random()}-{time.time()}"
    device_id = hashlib.sha1(random_data.encode('utf-8')).hexdigest().upper()
    return device_id

def get_initial_beijing_time():
    client = ntplib.NTPClient()
    beijing_tz = pytz.timezone("Asia/Shanghai")
    for server in ntp_servers:
        try:
            print(col_y + f"\nGetting Beijing time 🇨🇳" + Fore.RESET)
            response = client.request(server, version=3)
            ntp_time = datetime.fromtimestamp(response.tx_time, timezone.utc)
            beijing_time = ntp_time.astimezone(beijing_tz)
            print(col_g + f"[⏰🇨🇳]: " + Fore.RESET +  f"{beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
            return beijing_time
        except Exception as e:
            print(f"Error to connect {server}: {e}")
    print(f"NTP Server Not Found.")
    return None

def get_synchronized_beijing_time(start_beijing_time, start_timestamp):
    elapsed = time.time() - start_timestamp
    current_time = start_beijing_time + timedelta(seconds=elapsed)
    return current_time

def wait_until_target_time(start_beijing_time, start_timestamp):
    next_day = start_beijing_time + timedelta(days=1)
    print(col_y + f"\nBootloader unlock request" + Fore.RESET)
    print (col_g + f"[Phase Shift Established]: " + Fore.RESET + f"{feed_time_shift:.2f} мс.")
    target_time = next_day.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=feed_time_shift_1)
    print(col_g + f"[Waiting untill ... 🥱]: " + Fore.RESET + f"{target_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
    print(f"Do not exit")
    
    while True:
        current_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
        time_diff = target_time - current_time
        
        if time_diff.total_seconds() > 1:
            time.sleep(min(1.0, time_diff.total_seconds() - 1))
        elif current_time >= target_time:
            print(f"It's tiiime: {current_time.strftime('%Y-%m-%d %H:%M:%S.%f')}. Starting requests")
            break
        else:
            time.sleep(0.0001)

def check_unlock_status(session, cookie_value, device_id):
    try:
        url = "https://sgp-api.buy.mi.com/bbs/api/global/user/bl-switch/state"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }
        
        response = session.make_request('GET', url, headers=headers)
        if response is None:
            print(f"[Error] It was not possible retrieve unlock status.")
            return False

        response_data = json.loads(response.data.decode('utf-8'))
        response.release_conn()

        if response_data.get("code") == 100004:
            print(f"[Error] Expired Cookie ... try again.")
            exit()

        data = response_data.get("data", {})
        is_pass = data.get("is_pass")
        button_state = data.get("button_state")
        deadline_format = data.get("deadline_format", "")

        if is_pass == 4:
            if button_state == 1:
                    print(col_g + f"[Account Status]: " + Fore.RESET + f"the requests will be sent.")
                    return True

            elif button_state == 2:
                print(col_g + f"[Account Satus]: " + Fore.RESET + f"requests blocked untill " f"{deadline_format} (Month/Day).")
                status_2 = (input(f"Continue (" + col_b + f"Yes/No" +Fore.RESET + f")?: ") )
                if (status_2 == 'y' or status_2 == 'Y' or status_2 == 'yes' or status_2 == 'Yes' or status_2 == 'YES'):
                    return True
                else:
                    exit()
            elif button_state == 3:
                print(col_g + f"[Account Status]: " + Fore.RESET + f"Account created date lesser than 30 days")
                status_3 = (input(f"Continue (" + col_b + f"Yes/No" +Fore.RESET + f")?: ") )
                if (status_3 == 'y' or status_3 == 'Y' or status_3 == 'yes' or status_3 == 'Yes' or status_3 == 'YES'):
                    return True
                else:
                    exit()
        elif is_pass == 1:
            print(col_g + f"[Account Status]: " + Fore.RESET + f"Request approved, unblock untill " f"{deadline_format}.")
            input(f"Presione Enter para cerrar...")
            exit()
        else:
            print(col_g + f"[Account Status]: " + Fore.RESET + f"Unknow State.")
            exit()
    except Exception as e:
        print(f"[Error at status checking] {e}")
        return False

class HTTP11Session:
    def __init__(self):
        self.http = urllib3.PoolManager(
            maxsize=10,
            retries=True,
            timeout=urllib3.Timeout(connect=2.0, read=15.0),
            headers={}
        )

    def make_request(self, method, url, headers=None, body=None):
        try:
            request_headers = {}
            if headers:
                request_headers.update(headers)
                request_headers['Content-Type'] = 'application/json; charset=utf-8'
            
            if method == 'POST':
                if body is None:
                    body = '{"is_retry":true}'.encode('utf-8')
                request_headers['Content-Length'] = str(len(body))
                request_headers['Accept-Encoding'] = 'gzip, deflate, br'
                request_headers['User-Agent'] = 'okhttp/4.12.0'
                request_headers['Connection'] = 'keep-alive'
            
            response = self.http.request(
                method,
                url,
                headers=request_headers,
                body=body,
                preload_content=False
            )
            
            return response
        except Exception as e:
            print(f"[Netwrok Error] {e}")
            return None
 
def main():
        
    device_id = generate_device_id()
    session = HTTP11Session()

    if check_unlock_status(session, cookie_value, device_id):
        start_beijing_time = get_initial_beijing_time()
        if start_beijing_time is None:
            print(f"Error to retrieve Beijing time.")
            exit()

        start_timestamp = time.time()
        
        wait_until_target_time(start_beijing_time, start_timestamp)

        url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }

        try:
            while True:
                request_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
                print(col_g + f"[Request]: " + Fore.RESET + f"Request sent at {request_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)")
                
                response = session.make_request('POST', url, headers=headers)
                if response is None:
                    continue

                response_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
                print(col_g + f"[Response]: " + Fore.RESET + f"Received at {response_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)")

                try:
                    response_data = response.data
                    response.release_conn()
                    json_response = json.loads(response_data.decode('utf-8'))
                    code = json_response.get("code")
                    data = json_response.get("data", {})

                    if code == 0:
                        apply_result = data.get("apply_result")
                        if apply_result == 1:
                            print(col_g + f"[Status]: " + Fore.RESET + f"Request approved, checking status")
                            check_unlock_status(session, cookie_value, device_id)
                        elif apply_result == 3:
                            deadline_format = data.get("deadline_format", "Not declared")
                            print(col_g + f"[Status]: " + Fore.RESET + f"Request quota reached. Try again at {deadline_format} (Month/Day).")
                            exit()
                        elif apply_result == 4:
                            deadline_format = data.get("deadline_format", "Not declared")
                            print(col_g + f"[Status]: " + Fore.RESET + f"Account blocked untill {deadline_format} (Month/Day).")
                            exit()
                    elif code == 100001:
                        print(col_g + f"[Status]: " + Fore.RESET + f"Request rejected")
                        print(col_g + f"[Response]: " + Fore.RESET + f"{json_response}")
                    elif code == 100003:
                        print(col_g + f"[Status]: " + Fore.RESET + f"Maybe it was approved, check status")
                        print(col_g + f"[Response]: " + Fore.RESET + f"{json_response}")
                        check_unlock_status(session, cookie_value, device_id)
                    elif code is not None:
                        print(col_g + f"[Status]: " + Fore.RESET + f"Unknow status: {code}")
                        print(col_g + f"[Response]: " + Fore.RESET + f"{json_response}")
                    else:
                        print(col_g + f"[Error]: " + Fore.RESET + f"Response without status code")
                        print(col_g + f"[Response]: " + Fore.RESET + f"{json_response}")

                except json.JSONDecodeError:
                    print(col_g + f"[Error]: " + Fore.RESET + f"JSON decode error")
                    print(col_g + f"[Server Response]: " + Fore.RESET + f"{response_data}")
                except Exception as e:
                    print(col_g + f"[Error response processing]: " + Fore.RESET + f"{e}")
                    continue

        except Exception as e:
            print(col_g + f"[Request Error]: " + Fore.RESET + f"{e}")
            exit()

if __name__ == "__main__":
    main()
