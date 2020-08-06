# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:20:33 2020

@author: SUE
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#from bs4 import BeautifulSoup
import json,time,datetime
def Connect_to_web(url):
    Options = webdriver.ChromeOptions()#设置请求头的信息
    Options.add_argument('lang=zh_CN.UTF-8')
    Options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU ""iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
    driver = webdriver.Chrome(r"C:\Users\SUE\AppData\Local\Google\Chrome\Application\chromedriver.exe",chrome_options=Options)#启动谷歌浏览器
    driver.get(url)
    return driver
def del_advertisements_tabs(driver):
          try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ico-close-b")))
            driver.find_element_by_class_name("ico-close-b").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))
            driver.find_element_by_class_name("button").click()
          except:
             return;
          print('',end='')
def read_script(driver):
    driver.set_script_timeout(30)
    fp1=open("script1.js",mode="r")
    script1=fp1.read()
    fp1.close()
    data=driver.execute_async_script(script1)#利用传参机制callback
    script2="window.scrollTo(0,0);"
    driver.execute_script(script2)#翻到顶上:进行下一次查询
    div=data.split("|")
    send="{\"list\":["
    for member in div:
          #print(member)
          send+="\""+member+"\""+","
    send=send[0:-1]+"]}"
    js=json.loads(send)
    return js
def search_city(driver,tag,info):#利用js寻找出发地和到达地
    del_alert_tabs="const callback = arguments[arguments.length -1];var tab=document.getElementsByClassName('button')[0];"
    del_alert_tabs+="if(tab){tab.click();} callback();"
    driver.execute_async_script(del_alert_tabs)
    try:
        driver.find_element_by_id(tag).click()
    except:
        print("找不到input1")
    print("",end="")
    path=driver.find_element_by_class_name("address_hot_abb")
    xpath=path.find_elements_by_tag_name("li")
    status="none"
    script="const callback = arguments[arguments.length -1];"
    script+="target='"+info+"';var list=document.getElementsByClassName('address_hot_adress layoutfix')[0].getElementsByTagName('a');"
    script+="var i;for(i=0;i<list.length;i++){if(list[i].innerHTML==target){list[i].click();callback('ok');}}callback('none');"  
    for i in xpath:
        i.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "address_hot")))#等待加载完成
        status=driver.execute_async_script(script)
        if(status=="ok"):
            break
    return status
def work_and_alter(driver,dcity,acity,date):
    print(search_city(driver,"dcity0",dcity))
    print(search_city(driver,"acity0",acity))
    driver.find_element_by_class_name("btn_search").click()
    js=read_script(driver)
    js['acity']=acity
    js['dcity']=dcity
    js['flight_date']=date
    js['update_date']= datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S')
    insert_data("data.txt", js)
    
def main():
     date="2020-08-14"
     driver=Connect_to_web("https://flights.ctrip.com/itinerary/oneway/ckg-tao?date="+date)
     del_advertisements_tabs(driver)
     work_and_alter(driver,"拉萨","成都",date)
     work_and_alter(driver,"西安","杭州",date)
     work_and_alter(driver,"南京","北京",date)
     work_and_alter(driver,"重庆","太原",date)
     work_and_alter(driver,"呼和浩特","沈阳",date)
    
def makeroom(path):#制作存储容器
    data="{\"data\":["
    for i in range(100):
       data+="\"\","
    data=data[0:-1]
    data+="],\"size\":100,\"length\":0}"
    data=json.loads(data)
    with open(path,mode='w')as fp:
      fp.write(json.dumps(data))
    fp.close()
def insert_data(path,string):#存储信息
    with open(path,mode='r')as fp:
      js=json.loads(fp.read())
      if js['length']==js['size']:
         print("该地址超载:请另换地址:")
         return;
      else:
          js['data'][js['length']]=json.dumps(string)
          js['length']=js['length']+1
          fp.close()
          fp=open(path,mode='w')
          fp.write(json.dumps(js))
          fp.close()
def check_data(path):
    fp=open(path,mode='r',encoding="utf-8")
    js=json.loads(fp.read())
    for i in range(js['length']):
        print(json.loads(js['data'][i]))
    print("length:",js['length'])
makeroom("data.txt")     
main()
check_data("data.txt")