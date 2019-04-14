#爬虫主逻辑  配合User-Agent 文件使用
import random
import requests
import json
from lxml import etree
import time
from headers_list import USER_AGENT_LIST




for i in range(1,364):
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
    # print(ip_list)
    ip = random.choice(ip_list)
    # print(type(ip))
    # print(ip)
    key_ip = ip[0:4]
    value_ip = ip[7:]

    dict_ip = {key_ip: value_ip}
    print(dict_ip)
    page=1
    page+=1

    base_url="http://b2b.huangye88.com/beijing/jiaoyu/pn{}".format(page)
    # base_url="https://www.baidu.com"
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
    headers ={"User-Agent":random.choice(USER_AGENT_LIST)}

    proxy=dict_ip
    response=requests.get(base_url,headers=headers,proxies=proxy)
    # print(response.url)
    # print(response.headers)
    print(response.status_code)
    data=response.content
        # with  open("1.html","w") as f:
        #     f.write(data.decode())
    parse_data=etree.HTML(data)
    #解析URL 20个
    parse_url=parse_data.xpath('//div[@class="mach_list2"]//h4/a/@href')

        #解析地址和主营业务
        # com_main_business=parse_data.xpaht('//form[@id="jubao"]//dd/strong[1]/text()')

        #地址解析 只有七个
        # com_address=parse_url.xpath('//f//form[@id="jubao"]//dd/strong[2]/text()')
    print(parse_url)
    for url in parse_url:
        time.sleep(0.1)
        two_response=requests.get(url,headers=headers,proxies=proxy)
        print(response.status_code)
        two_data=two_response.content
        two_parse_data=etree.HTML(two_data)
        try:
            com_name=two_parse_data.xpath('/html/body/div[4]/div[1]/div[1]/div[2]/ul[1]/li/text()')
            # print(com_name)

            com_product=two_parse_data.xpath('/html/body/div[4]/div[1]/div[1]/div[2]/ul[2]/li[2]/text()')
            # print(com_product)
            com_address=two_parse_data.xpath('/html/body/div[4]/div[1]/div[1]/div[2]/ul[2]/li[3]/text()')
            # print(com_address)
            com_introduce=two_parse_data.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/p/text()')
            com_people=two_parse_data.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/ul/li[1]/a/text()')
            phone_number=two_parse_data.xpath('/html/body/div[4]/div[1]/div[2]/div[2]/ul/li[4]/text()')
            # print(phone_number)
            com_dict = {}
            com_dict["com_name"]=com_name[0]
            com_dict["com_product"]=com_product[0]
            com_dict["com_address"]=com_address[0]
            com_dict["com_people"]=com_people[0]
            com_dict["com_phone_number"]=phone_number[0]
            com_dict["com_introduce"]=com_introduce[0]
            com_json=json.dumps(com_dict,ensure_ascii=False)+","+"\n"
            with open("7com_data.json","a") as f:
                f.write(com_json)

        except Exception:
            print("error")


