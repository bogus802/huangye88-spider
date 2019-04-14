#代理IP有一部分是不可用或者速度过慢，此文件主要是过滤掉不可用的IP和速度过慢的IP
import requests
import json

url = "http://iphighproxyv2.haoservice.com/devtoolservice/ipagency"
headers = {
    "Authorization": "APPCODE 13b49d3840da4d9795227e6e00d4c14c"
}
params = {
    "foreigntype": 1

}
response = requests.get(url, params=params, headers=headers)
ip_data = response.content.decode()
ip_dict = json.loads(ip_data)
# print(type(ip_dict))
ip_list = ip_dict["result"]
print(ip_list)

useable_ip_list=[]
for ip in ip_list:
    key_ip = ip[0:4]
    value_ip = ip[7:]
    dict_ip = {key_ip: value_ip}
    proxy=dict_ip
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
    # base_url="http://www.baidu.com"
    base_url="http://b2b.huangye88.com/beijing/jiaoyu"
    try:
        response=requests.get(base_url,headers=headers,proxies=proxy,timeout=3)
        print(response.status_code)
        if response.status_code==200:
            useable_ip_list.append(ip)


        else:
            print("IP不可用")
    except:
        print("服务器响应超时")



print(useable_ip_list)

