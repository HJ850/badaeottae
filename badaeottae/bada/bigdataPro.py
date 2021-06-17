'''
Created on 2021. 3. 22

@author: lyh77
'''
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import os
from badaeottae.settings import STATIC_DIR
from sqlalchemy import create_engine
import pandas as pd
#import seaborn as sns

def beach(data):
    key="SztTDw8obijvNv2nSJA3Gbbz3oO5rLOI%2Fe4Cn4n9quoxAk9q7G0AdrvohZRerogZxaEyA8p2FdmMGkDUELpFSQ%3D%3D"
    url="http://apis.data.go.kr/1192000/service/OceansBeachInfoService1/getOceansBeachInfo1?serviceKey="+key+"&pageNo=1&numOfRows=10&SIDO_NM=%EB%B6%80%EC%82%B0&resultType=json"
    resp = requests.get(url)
    
    jsonData=resp.json()
    items=jsonData['getOceansBeachInfo']['item']
    
    for i in range(0,7):
        beach=items[i]['sta_nm']
        link_addr=items[i]['link_addr']
        link_tel=items[i]['link_tel']
        lat=items[i]['lat']
        lon=items[i]['lon']
        data.append([beach,link_addr,link_tel,lat,lon])
        
def beach_scoring(water_temp,air_temp,windspd,wavehigh):
    sum=0
    result=0
    
    #배점
    best=5
    good=3
    normal=1
    bad=-1
    worst=-3
    
    #가중치
    if water_temp > 16:
        weight_wavehigh=2.2
        weight_windspd=1.2
        weight_water_temp=0.4
        weight_air_temp=0.2
    else:
        weight_wavehigh=1.8
        weight_windspd=1.0
        weight_water_temp=1.0
        weight_air_temp=0.2
    
    #수온
    if water_temp >= 22:
        score_water_temp=best
    elif 22 > water_temp >=20:
        score_water_temp=good
    elif 20 > water_temp >=20:
        score_water_temp=normal
    elif 18 > water_temp >=14:
        score_water_temp=bad
    else:
        score_water_temp=worst
    sum+=score_water_temp*weight_water_temp
    
    #유의 파고
    if wavehigh <= 0.5:
        score_wavehigh=best
    elif 1 > wavehigh >=0.5:
        score_wavehigh=good
    elif 1.5 > wavehigh >=1:
        score_wavehigh=normal
    elif 2 > wavehigh >=1.5:
        score_wavehigh=bad
    else:
        score_wavehigh=worst
    sum+=score_wavehigh*weight_wavehigh
    
    #풍속
    if windspd <= 2:
        score_windspd=best
    elif 5 > windspd >=2:
        score_windspd=good
    elif 8 > windspd >=5:
        score_windspd=normal
    elif 10 > windspd >=8:
        score_windspd=bad
    else:
        score_windspd=worst
    sum+=score_windspd*weight_windspd
    
    #기온
    if air_temp >= 27:
        score_air_temp=best
    elif 27 > air_temp >=24:
        score_air_temp=good
    elif 24 > air_temp >=22:
        score_air_temp=normal
    elif 22 > air_temp >=20:
        score_air_temp=bad
    else:
        score_air_temp=worst
    sum+=score_air_temp*weight_air_temp
    
    score=score_water_temp*weight_water_temp+score_wavehigh*weight_wavehigh+score_windspd*weight_windspd+score_air_temp*weight_air_temp
    
    if score>=12:
        result="좋음"
    elif 12>score>-4:
        result="보통"
    else:
        result="나쁨"
        
    return result

def weather_search(data):
    #부산앞바다 날씨
    weather_url = 'http://www.weather.go.kr/mini/marine/marine_daily.jsp?topArea=12B20000&midArea=12B20100&btmArea=12B20103'
    weather_html=urlopen(weather_url)
    weather_bs=BeautifulSoup(weather_html,'html.parser')
    weather=weather_bs.select('tbody > tr:nth-of-type(1) > td:nth-of-type(4) > img')[0].attrs['alt']
    
    #임랑
    im_url='http://www.khoa.go.kr/oceangrid/koofs/kor/observation/obs_real_detail.do?tsType=2&tsId=IMRANG&obsItem=ALL&obsSubItem='
    #송정
    song_url='http://www.khoa.go.kr/oceangrid/koofs/kor/observation/obs_real_detail.do?tsType=2&tsId=SONGJUNG&obsItem=&obsSubItem=S_'
    #해운대
    hae_url='http://www.khoa.go.kr/oceangrid/koofs/kor/observation/obs_real_detail.do?tsType=2&tsId=HAE&obsItem=ALL&obsSubItem='
    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    
    driver=webdriver.Chrome('D:/LHJ/src/python/chromedriver',options=options)
    driver.implicitly_wait(3)
    
    #임랑
    driver.get(im_url)
    water_temp=driver.find_element_by_css_selector('#subPage > div.rig_box7 > div:nth-child(1) > ul > li:nth-child(3)').text
    air_temp = driver.find_element_by_css_selector("#subPage > div.rig_box7 > div:nth-child(2) > ul > li:nth-child(3)").text
    windspd = driver.find_element_by_css_selector("#subPage > div.rig_box7 > div:nth-child(4) > ul > li:nth-of-type(3) > span.box8_font10").text
    wavehigh = driver.find_elements_by_css_selector("#subPage > div:nth-child(3) > table > tbody > tr:nth-child(4) > td:nth-child(2) > font")[0].text
    
    im_water_temp=float(water_temp.replace("℃",""))
    im_air_temp=float(air_temp.replace("℃",""))
    im_windspd=float(windspd.replace("동","").replace("서","").replace("남","").replace("북",""))
    im_wavehigh=float(wavehigh)
    
    #송정
    driver.get(song_url)
    water_temp=driver.find_element_by_css_selector('#subPage > div.rig_box7 > div:nth-child(1) > ul > li:nth-child(3)').text
    air_temp = driver.find_element_by_css_selector("#subPage > div.rig_box7 > div:nth-child(2) > ul > li:nth-child(3)").text
    windspd = driver.find_element_by_css_selector("#subPage > div.rig_box7 > div:nth-child(4) > ul > li:nth-of-type(3) > span.box8_font10").text
    wavehigh = driver.find_elements_by_css_selector("#subPage > div:nth-child(3) > table > tbody > tr:nth-child(4) > td:nth-child(2) > font")[0].text
    
    song_water_temp=float(water_temp.replace("℃",""))
    song_air_temp=float(air_temp.replace("℃",""))
    song_windspd=float(windspd.replace("동","").replace("서","").replace("남","").replace("북",""))
    song_wavehigh=float(wavehigh)
    
    #해운대
    driver.get(hae_url)
    water_temp=driver.find_element_by_css_selector('#subPage > div.rig_box7 > div:nth-child(1) > ul > li:nth-child(3)').text
    air_temp = driver.find_element_by_css_selector("#subPage > div.rig_box7 > div:nth-child(2) > ul > li:nth-child(3)").text
    windspd = driver.find_element_by_css_selector("#subPage > div.rig_box7 > div:nth-child(4) > ul > li:nth-of-type(3) > span.box8_font10").text
    wavehigh = driver.find_elements_by_css_selector("#subPage > div:nth-child(3) > table > tbody > tr:nth-child(4) > td:nth-child(2) > font")[0].text
    
    hae_water_temp=float(water_temp.replace("℃",""))
    hae_air_temp=float(air_temp.replace("℃",""))
    hae_windspd=float(windspd.replace("동","").replace("서","").replace("남","").replace("북",""))
    hae_wavehigh=float(wavehigh)
    
    data.append([im_water_temp,im_air_temp,im_windspd,im_wavehigh,song_water_temp,song_air_temp,song_windspd,song_wavehigh,hae_water_temp,hae_air_temp,hae_windspd,hae_wavehigh,weather])
    
    return data

def weather_heatmap():
    font_location = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)
    
    engine=create_engine('mysql+pymysql://lhj:1234@localhost/badaeottae_db',convert_unicode=True)
    conn=engine.connect()
    df=pd.read_sql_table('bada__weather',conn)
    
    corr=df.corr()
    
    plt.figure(figsize=(12, 12))
    plt.title("기상 데이터 간의 상관관계", y = 1.05, size = 20)
    sns.heatmap(corr, linewidths = 0.1, vmax = 1.0, square = True,
                cmap = 'Blues', linecolor = "white", annot = True,
                annot_kws = {"size" : 15})
    #plt.savefig(os.path.join(STATIC_DIR,'weather_heatmap.png'))
            
def jf_clustering():
    font_location = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)
    
    engine=create_engine('mysql+pymysql://lhj:1234@localhost/badaeottae_db',convert_unicode=True)
    conn=engine.connect()
    df=pd.read_sql_table('bada__weather',conn)
    
    plt.figure(figsize=(8,4))
    for i in range(0,205):
        if(df.true[i]==1):
            plt.scatter(df.wt[i],df.ratio[i],color='blue',vmin=0,vmax=30)
            plt.xlabel('수온', fontsize=14)
            plt.ylabel('발견율', fontsize=14)
    plt.title('수온별 해파리 발견율', fontsize=20)
    plt.xlim(0, 30)
    plt.ylim(0, 70)
    plt.grid()
    #plt.savefig(os.path.join(STATIC_DIR,'graph/jf_clustering.png'))
    
def plankton_heatmap():
    font_location = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)
    
    engine=create_engine('mysql+pymysql://lhj:1234@localhost/badaeottae_db',convert_unicode=True)
    conn=engine.connect()
    df=pd.read_sql_table('bada__plankton',conn)
    
    corr=df.corr()
    
    plt.figure(figsize=(16, 16))
    plt.title("플랑크톤 데이터 간의 상관관계", y = 1.05, size = 20)
    sns.heatmap(corr, linewidths = 0.1, vmax = 1.0, square = True,
                cmap = 'Blues', linecolor = "white", annot = True,
                annot_kws = {"size" : 15})
    #plt.savefig(os.path.join(STATIC_DIR,'plankton_heatmap.png'))
    
def moak_nomura():
    font_location = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)
    
    engine=create_engine('mysql+pymysql://lhj:1234@localhost/badaeottae_db',convert_unicode=True)
    conn=engine.connect()
    df=pd.read_sql_table('bada__plankton',conn)
    
    x=pd.DataFrame(df, columns=['tos'])
    y=pd.DataFrame(df, columns=['wt','ratio','moak'])
    true=df.true
    
    plt.figure(figsize=(24,5))
    plt.title('모악류와 노무라',y=1.05,fontsize=20)
    plt.plot(x['tos'],y['wt'],color='red',label='watertemper')
    plt.plot(x['tos'],y['ratio'],color='blue',label='jf_ratio')
    plt.plot(x['tos'],y['moak'],color='green',label='moak')
    plt.legend()
    plt.xlim('2015-10-22', '2019-12-12')
    plt.ylim(0, 180)
    plt.grid()
    #plt.savefig(os.path.join(STATIC_DIR,'moak_nomura.png'))
    
def chucksek_nomura():
    engine=create_engine('mysql+pymysql://lhj:1234@localhost/badaeottae_db',convert_unicode=True)
    conn=engine.connect()
    df=pd.read_sql_table('bada__plankton',conn)
    
    x=pd.DataFrame(df, columns=['tos'])
    y=pd.DataFrame(df, columns=['wt','ratio','chuck'])
    true=df.true
    
    plt.figure(figsize=(24,5))
    plt.title('적색류와 노무라',y=1.05,fontsize=20)
    plt.plot(x['tos'],y['wt'],color='red',label='watertemper')
    plt.plot(x['tos'],y['jratio'],color='blue',label='jf_ratio')
    plt.plot(x['tos'],y['chuck'],color='green',label='chucksek')
    plt.legend()
    plt.xlim('2015-10-22', '2019-12-12')
    plt.ylim(0, 180)
    plt.grid()
    #plt.savefig(os.path.join(STATIC_DIR,'chucksek_nomura.png'))