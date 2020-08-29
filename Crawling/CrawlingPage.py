# -*- coding: utf-8 -*-
'''복지로 Page Crawling'''
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append("/root/RGRG")
import Model.DBModel as DBModel


mainUrl = 'http://www.bokjiro.go.kr' #main url

#Set ChromeDriver Option
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')

now = datetime.now() #get current datetime(format: YYYY-MM-DD TIME)

#SetDBSet
DB = create_engine('mysql+mysqldb://root:hongskids1!@127.0.0.1/site?charset=utf8', echo=True)
Base = declarative_base()
Base.metadata.create_all(DB)

Session = sessionmaker()
Session.configure(bind=DB)
session = Session()

def getMainPage(soup):
    #민간 복지서비스 조회 페이지에서 제목, 사업기간, 사업상태(진행중, 마감)을 크롤링하는 함수
    datas = soup.select('table > tbody > tr > td')

    title = '' #공지사항 제목
    site = '' #기관명
    reg_date = None
    deadline = None
    state = 1

    i = 1

    if not datas: #빈 페이지일 경우, return
        return -1

    for data in datas:
        title, site, reg_date, deadline, state
        if i == 2: #공지사항 제목
            title = data.text

        if i == 3: #기관명
            site = data.text

        if i == 4:
            splitMark = data.text.find('~')
            reg_date = datetime.strptime(data.text[:splitMark-1].replace('/', '-'), "%Y-%m-%d")
            deadline = datetime.strptime(data.text[splitMark+2:].replace('/', '-'), "%Y-%m-%d")

        if i == 5: #진행여부
            if(data.find('a').text != '진행중'): #진행중이 아닐 시, return
                state = 0
                break
                return 0
            else:
                contentUrl = mainUrl + data.find('a')['href']
                site_id = findSiteID('복지로')
                crawl_item_id = insertCrawlItemDB(site_id, contentUrl, title, reg_date, deadline, state)
                if crawl_item_id != 1:
                    getContent(crawl_item_id, contentUrl)


        i += 1
        if i == 6:
            i = 1

def getContent(crawl_item_id, contentUrl):
    #공지사항 게시물 하나의 url을 인자로 받아 게시물 내용을 크롤링하는 함수
    content = ""
    postDriver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', chrome_options=options)
    postDriver.get(contentUrl)
    postHtml = postDriver.page_source
    postSoup = BeautifulSoup(postHtml, "html.parser")

    datas = postSoup.find_all('div', {"class": "shareServiceCont"})

    for data in datas:
        for i in data.find_all('li'):
            for j in i.contents:
                if j != '\n':
                    content = content + j.text.strip() + "\n"

    insertContentDB(crawl_item_id, content)
    postDriver.close()

def insertCrawlItemDB(site_id, contentUrl, title, reg_date, deadline, state):
    #  insert into crawl_item table
    selectData = session.query(DBModel.crawl_item).filter(DBModel.crawl_item.url == contentUrl).all()  # contentUrl을 가진 칼럼 select

    if selectData:  # check selectData list empty
        if (selectData[0].url == contentUrl):  # url이 이미 db에 존재하는 경우, 공고 진행상태(state column)만 update
            session.query(DBModel.crawl_item).filter(DBModel.crawl_item.url == contentUrl).update({'state': state});
            session.commit()
            return 1
    else:
        data = DBModel.crawl_item(site_id, contentUrl, title, state, reg_date=reg_date, deadline=deadline)  # 존재하지 않는 url일 경우 insert

        session.add(data) #Insert crawl_item DB
        session.commit()

        return data.crawl_id

def insertContentDB(crawl_item_id, content):
    #insert into content table
    data = DBModel.content(crawl_item_id, content)

    session.add(data)
    session.commit()

def findSiteID(site):
    #Site DB에서 'site'에 해당하는 site_id return
    for id, value in session.query(DBModel.site.site_id, DBModel.site.name).distinct():
        if (site == value):
            return id


pageNo = 1
while(1):
    url = "http://www.bokjiro.go.kr/nwel/helpus/welsha/selectWelShaInfoBbrdMngList.do?searchCondition=&searchKeyword=&srchDuration=&stDate=&endDate=&pageUnit=10&endSvrEsc=0&intClIdStr=&orderCol=MODDATE&orderBy=DESC&recordCountPerPage=10&viewEndService=&pageIndex=" + str(pageNo)
    driver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', chrome_options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    result = getMainPage(soup)
    driver.close()
    pageNo += 1 #pagenation 증가
    if result == -1: #빈페이지 일 경우, 반복문 종료
        break


        #contents > div.listTbl > table > tbody
