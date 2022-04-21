from xml.dom.minidom import Element
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
from pytest import Item
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pdb
from pymongo import MongoClient
import psycopg2
con = psycopg2.connect(host='localhost',dbname="onjiuvur", user="onjiuvur", password="DW_pu23aYvbJVc1Z70sBaGjzobEs3tw2",port=5432)

cur = con.cursor()






def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver
driver = set_chrome_driver()







def PageUrl(pageNum):
  url_1 = 'https://www.musinsa.com/category/001001?d_cat_cd=001001&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page='
  url_2 = '&display_cnt=90&sale_goods=&group_sale=&kids=N&ex_soldout=&color=1&price1=&price2=&exclusive_yn=&shoeSizeOption=&tags=&campaign_id=&timesale_yn=&q=&includeKeywords=&measure='
  url = url_1+str(pageNum)+url_2
  return url
pageurl = PageUrl(1)
driver.get(pageurl)
totalPageNum = driver.find_element_by_css_selector(".totalPagingNum").text
print("Total Page" , str(totalPageNum))

for i in range(int(totalPageNum)):

    pageurl = PageUrl(i+1)
    driver.get(pageurl)
    time.sleep(2)
    item_infos = driver.find_elements_by_css_selector('#searchList > li > div.li_inner > div.article_info')
    item_ls = driver.find_elements_by_css_selector(".img-block")


    for i in range(len(item_infos)):
            #time.sleep(0.5)
            price_h = []
            brand_all = []
            title_all = []
            price_all = []
            cunt_all =[]
            love_all =[]
            link_all =[]
            color = []
            price_h = []
            product_all = []
  
            brand = item_infos[i].find_element_by_class_name("item_title")
            brand_ = brand.text
            product_all.append(brand_)
            title = item_infos[i].find_element_by_class_name("list_info")
            title_ = title.text
            if '배송' in title_:
              titlex = title_.split('배송')
              product_all.append(titlex[1])
            else:
              product_all.append(title_)

            price= item_infos[i].find_element_by_class_name("price")
            price_h = price.text.split()
            
            if len(price_h) == 1:
              product_all.append(price_h[0])
              #price_all.replace(' ','')
            elif len(price_h) ==2:
              product_all.append(price_h[1])
            
            #price_all = list(filter(None, price_all))
            
            #price_all.append(price_h[1])
            #price_all = price_all.replace(' ','')
                      
            try:
              cunt = item_infos[i].find_element_by_class_name('count')
              product_all.append(cunt.text.replace(' ',''))
              #cunt_all = cunt_all
            except:
              cunt = None
              product_all.append('0')
              #cunt_all = cunt_all.replace(' ','')
            try:
              love = item_infos[i].find_element_by_class_name('txt_cnt_like')
              product_all.append(love.text.replace(' ',''))
              #love_all = love_all
            except:
              love = None
              product_all.append('0')

            link = item_ls[i].get_attribute("href")
            product_all.append(link)
            product_all.append('White')
            
            print(product_all)
#(brand,title,price,riview,wishlist,link,color) VALUES(
            #print((brand_all))
            #print(title_all)
            #print(price_all)
            #print(cunt_all)
            #print(love_all)
            #print(link_all)
            #print(brand_all)
            sql = "INSERT INTO musinsa_table (brand, title, price, riview, wishlist, link, color) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, product_all)
            con.commit()
driver.close()