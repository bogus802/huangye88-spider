import  requests
import random
from headers_list import USER_AGENT_LIST
# from ip_filter import useable_ip_list
from redis import StrictRedis
from lxml import etree
import time,json

class Get_Ip(object):
    def get_ip(self,):
        redis_connection=StrictRedis(host="127.0.0.1",port=6379,db=8,decode_responses=True)
        useable_ip_list=redis_connection.lrange("1",0,-1)
        ip_list=useable_ip_list
        ip=random.choice(ip_list)
        print(ip)
        key_ip = ip[0:4]
        value_ip = ip[7:]
        dict_ip = {key_ip: value_ip}
        proxy = dict_ip
        # print(proxy)
        return proxy
class Get_User_Agent(object):
     def get_user_agent(self, ):
        user_agent = random.choice(USER_AGENT_LIST)
        # print(user_agent)
        headers = {"User-Agent": user_agent}
        # print(headers)
        return headers


class hangye88(object):
    def __init__(self,proxy,user_agent):
        self.page=0
        self.proxy=proxy
        self.headers=user_agent

    def get_first_url(self,):
        self.page+=1
        base_url = "http://b2b.huangye88.com/beijing/jiaoyu/pn{}".format(self.page)
        response = requests.get(base_url, headers=self.headers, proxies=self.proxy)
        print(response.status_code)

        data = response.content
        parse_data = etree.HTML(data)
        parse_url = parse_data.xpath('//div[@class="mach_list2"]//h4/a/@href')
        print(self.page)
        return parse_url
    def get_target_data(self,parse_url):
        for url in parse_url:
            time.sleep(0.1)
            two_response = requests.get(url, headers=self.proxy, proxies=self.headers)
            print(two_response.status_code)
            try:
                print(two_response.status_code)
                two_data = two_response.content
                two_parse_data = etree.HTML(two_data)
                try:
                    com_name = two_parse_data.xpath('/html/body/div[4]/div[1]/div[1]/div[2]/ul[1]/li/text()')
                    # print(com_name)

                    com_product = two_parse_data.xpath('/html/body/div[4]/div[1]/div[1]/div[2]/ul[2]/li[2]/text()')
                    # print(com_product)
                    com_address = two_parse_data.xpath('/html/body/div[4]/div[1]/div[1]/div[2]/ul[2]/li[3]/text()')
                    # print(com_address)
                    com_introduce = two_parse_data.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/p/text()')
                    com_people = two_parse_data.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/ul/li[1]/a/text()')
                    phone_number = two_parse_data.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/ul/li[4]/text()')
                    # print(phone_number)
                    com_dict = {}
                    com_dict["com_name"] = com_name[0]
                    com_dict["com_product"] = com_product[0]
                    com_dict["com_address"] = com_address[0]
                    com_dict["com_people"] = com_people[0]
                    com_dict["com_phone_number"] = phone_number[0]
                    com_dict["com_introduce"] = com_introduce[0]
                    com_json = json.dumps(com_dict, ensure_ascii=False) + "," + "\n"
                    with open("1com_data.json", "a") as f:
                        f.write(com_json)
                except Exception:
                    print("获取数据失败")
            except:
                print("请求超时")
proxy=Get_Ip().get_ip()
user_agent=Get_User_Agent().get_user_agent()
print(proxy)
print(user_agent)
one=hangye88(proxy,user_agent)
for i in range(1,350):
    parse_url = one.get_first_url()
    one.get_target_data(parse_url)
