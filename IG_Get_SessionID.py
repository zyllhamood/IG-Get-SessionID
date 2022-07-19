import os
try:
    from requests import post
except ImportError:
    os.system('pip install requests')
    from requests import post
import re
import json
def sendCode(url,csrftoken,mid,choice):
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-CSRFToken": csrftoken,
        "X-Instagram-AJAX": "ebe60d79ce7c",
        "X-IG-App-ID": "936619743392459",
        "X-ASBD-ID": "198387",
        "X-IG-WWW-Claim": "0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "8",
        "Origin": "https://www.instagram.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": f"csrftoken={csrftoken}; mid={mid}",
        "Sec-Fetch-Dest": "empty",
    }
    data = f"choice={choice}"
    req = post(url,data=data, headers=Headers)
    response = req.text
    return response

def submit(url,csrftoken,mid,code):
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-CSRFToken": csrftoken,
        "X-Instagram-AJAX": "ebe60d79ce7c",
        "X-IG-App-ID": "936619743392459",
        "X-ASBD-ID": "198387",
        "X-IG-WWW-Claim": "0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "20",
        "Origin": "https://www.instagram.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": f"csrftoken={csrftoken}; mid={mid}",
        "Sec-Fetch-Dest": "empty",
    }
    data = f"security_code={code}"
    req = post(url,data=data, headers=Headers)
    return req

def api(username,password):
    url = 'https://i.instagram.com/api/v1/accounts/login/'
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Instagram 27.0.0.13.98 (iPhone7,2; iOS 12_5_1; en_SA@calendar=gregorian; ar-SA; scale=2.00; gamut=normal; 750x1334) AppleWebKit/420+"
    }
    data = 'signed_body=60db38d4261c23c9ccb814cb3820ed63870f385a30e648659f2ffa9aeb623234.{"reg_login":"0","username":"' + username + '","password":"' + password + '","device_id":"A6ECB176-7695-4893-9185-A478D3B10BFD","login_attempt_count":"0","adid":"ED063999-948C-4B83-A80F-D412E3DB21DA"}&ig_sig_key_version=5'
    resp = post(url, headers=headers, data=data)
    return resp

def account():
    username = input("Enter Username : ")
    password = input("Enter Password : ")
    resp = api(username, password)
    if 'logged_in_user' in resp.text:
        sessionid = resp.cookies['sessionid']
        print(f"Your SessionID : {sessionid}")
        with open('sessions.txt', 'a', encoding='utf-8', errors='ignore') as p:
            p.writelines(sessionid + '\n')

    elif 'challenge' in resp.text:
        secureURL = json.loads(resp.text)['challenge']['url']
        csrftoken = re.findall(r'csrftoken=(\w+)', str(resp.cookies))[0]
        mid = re.findall(r'mid=(\w+)', str(resp.cookies))[0]
        num = input("[0] send code to phone [1]send code to email")
        respSend = sendCode(secureURL, csrftoken, mid, num)
        if '"status":"ok"' in respSend:
            print("Done Send ...")
            code = input("Enter code : ")
            respSubmit = submit(secureURL, csrftoken, mid, code)
            if '"status":"ok"' in respSubmit.text:
                sessionid = re.findall(r'sessionid=(.*) for', str(respSubmit.cookies))[0]
                print(f"Your SessionID : {sessionid}")
            else:
                print("Error Code")
        else:
            print("Error Send")
    else:
        print(resp)

def combo():
    combo_list = open('combo.txt','r', encoding='utf-8').read().splitlines()
    for item in combo_list:
        username = item.split(":")[0]
        password = item.split(":")[1]
        try:

            resp = api(username, password)
            sessionid = resp.cookies['sessionid']
            print(sessionid)
            with open('sessions.txt', 'a', encoding='utf-8', errors='ignore') as p:
                p.writelines(sessionid + '\n')
        except:
            print(f"Error Login : {item}")

    print("Done ...")


choice = input("Enter [1]account || [2]combo(user:pass) : ")
if choice == "1":
    account()
if choice == "2":
    combo()




