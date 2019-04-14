
import requests
import json
from redis import StrictRedis

url = "http://iphighproxyv2.haoservice.com/devtoolservice/ipagency"
headers = {
    "Authorization": "APPCODE 13b49d3840da4d9795227e6e00d4c14c"
}
params = {
    "foreigntype": 1

}
response = requests.get(url, params=params, headers=headers)
ip_data = response.content.decode()
#json 转字典
ip_dict = json.loads(ip_data)
print(type(ip_dict))
#将字典格式的IP 存储到redis数据库 存入字典格式必须先序列化成字符串json格式


ip_list = ip_dict["result"]
print(ip_list)

# useable_ip_list=[]
redis_connection=StrictRedis(host="127.0.0.1",port=6379,db=8)
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
            # useable_ip_list.append(ip)
            redis_connection.lpush("1",ip)
            print("存储成功")
        else:
            print("IP不可用")
    except:
        print("服务器响应超时")


#将userable_ip_list 存入redis
# print(useable_ip_list)
print(redis_connection.lrange("1" , 0 , -1))

