# coding:utf-8
import urllib.request as ul
import xmltodict
import json
import sys
import io
import os #DBModel 참조위한 절대값 호출 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import datetime
import Model.DBModel as DBModel 


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


global service_key
global organizations
global orgCode_index

service_key = "eSiby8RuStqW%2F%2BpmvbtEVin7gWDGxynbYaouL6DM5y2DOziRI75s5K5nFzfnXpp3Ce3vssdZUPvYD8zPabwWUg%3D%3D"
#service_key = "xez1WwGlvDKKVugWlOG6wl1CFDj3iCGWYp5blEh4wwob4eVe2VptQkJ48NMlozmyTESWEnlz5jgmy60YR00HTA%3D%3D"
#SetDBSet
DB = create_engine('mysql+mysqldb://root:hongskids1!@127.0.0.1/site?charset=utf8', echo=True)
Base = declarative_base()
Base.metadata.create_all(DB)

Session = sessionmaker()
Session.configure(bind=DB)
session = Session()

# api 나)기관분류 코드
# 중앙행정기관 or 시군구
def organization_classify():
    global service_key
    global organizations
    global orgCode_index
    orgCode = [0 for i in range(30)]  # 기관코드를 저장하는 리스트
    
    i = 0
    organizations = [0 for i in range(2)]
    orgCode_index = 0

    url = 'http://api.korea.go.kr/openapi/org/cls/code?serviceKey=' + service_key + '&'
    result = apiconnect(url)

    for res_val in result.values():
        for val_1 in res_val.values():
            if 'orgCls' in val_1:
                for val_2 in val_1.values():
                    for val_3 in val_2:
                        organizations[i] = val_3['orgClsCode']
                        i+=1
                        # organizations[0] : 중앙행정기관
                        # organizations[1] : 시군구

    for val in organizations:
        organization_code(val, orgCode)

    # orgCode : 모든 기관코드 list
    service_list(orgCode)

# 기관 코드
def organization_code(organizations_classified, orgCode):
    global orgCode_index
    url = "http://api.korea.go.kr/openapi/org/code?serviceKey="+service_key+"&orgClsCd="+organizations_classified+"&upOrgCd=&"
    result = apiconnect(url)

    for res_val in result.values():
        print(res_val)
        val_1 = res_val['orgs']
        val_2 = val_1['org']

        for val_3 in val_2:
            orgCode[orgCode_index] = val_3['orgCode']
            orgCode_index += 1



# 서비스 목록
def service_list(orgCode):

    listsize = str(3) # 받아올 서비스 목록 개수

    for val_1 in orgCode:

        url = "http://api.korea.go.kr/openapi/svc/list?serviceKey=" + service_key + "&format=&srhQuery=&sort=DATE&jrsdOrgCd=" + str(val_1) + "&jrsdOrgNm=&lrgAstCd=&mdmAstCd=&smallAstCd=&pageIndex=1&pageSize=" + listsize + "&"
        result = apiconnect(url)

        for res_val in result.values():
            for val_1 in res_val:
                if val_1 == 'svcList':
                    val_2 = res_val[val_1]
                    val_3 = val_2['svc'] # val_3 : 한 기관의 서비스 목록
                    for val_4 in val_3: # val_4 : 각각의 목록
                        #print(val_4)
                        svcId = val_4['svcId'] #id
                        svcNm = val_4['svcNm']
                        jrsdDptAllNm = val_4['jrsdDptAllNm']
                        svcEditDt = val_4['svcEditDt']
                        svcPpo = val_4['svcPpo']
                        sportFr = val_4['sportFr']
                        vwCnt = val_4['vwCnt']
                        svcInfoUrl = val_4['svcInfoUrl']
                        svcInfoKrUrl = val_4['svcInfoKrUrl']

                        """
                        ### site db 채워넣는 코드 ###
                        #data_2 = DBModel.site(jrsdDptAllNm, svcInfoUrl)  # svcNm
                        data_2 = DBModel.site("다 안들어가요", svcInfoUrl) #svcNm
                        session.add(data_2)
                        session.commit()
                        """

                        site_id = findSiteID(svcInfoUrl)
                        
                        more_service_list(svcId, site_id, svcNm, vwCnt)


# 서비스 상세 목록
def more_service_list(svcId, site_id, svcNm, vwCnt):
    url = "http://api.korea.go.kr/openapi/svc?serviceKey=eSiby8RuStqW%2F%2BpmvbtEVin7gWDGxynbYaouL6DM5y2DOziRI75s5K5nFzfnXpp3Ce3vssdZUPvYD8zPabwWUg%3D%3D&format=xml&svcId="+str(svcId)+"&"
    result = apiconnect(url)

    print(result.values())
    for res_val in result.values():
        for val_1 in res_val:
            if val_1 == 'svc':
                val_2 = res_val['svc']
                for val_3 in val_2:
                    svcNm = val_2['svcNm'] #제목
                    jrsdDptAllNm = val_2['jrsdDptAllNm']
                    svcEditDt = val_2['svcEditDt'] #최종수정일
                    slctnStdr = val_2['slctnStdr']
                    dupImprtySvc = val_2['dupImprtySvc']
                    reqstProcessPd = val_2['reqstProcessPd'] #신청기한
                    posesPapers = val_2['posesPapers']
                    onlnReqstSiteUrl = val_2['onlnReqstSiteUrl']
                    rcvOrgNm = val_2['rcvOrgNm']
                    rcvOrgTelNo = val_2['rcvOrgTelNo']
                    svcCts = val_2['svcCts'] # 내용
                    refrncNm = val_2['refrncNm']
                    refrncTelNo = val_2['refrncTelNo']
                    refrncSiteUrl = val_2['refrncSiteUrl']
                    svcInfoUrl = val_2['svcInfoUrl'] #url
                    svcInfoKrUrl = val_2['svcInfoKrUrl']
                    onlnReqstSiteUrl = val_2['onlnReqstSiteUrl']

    state = 1 #임시

    crawl_item_id = insertCrawlItemDB(site_id, svcInfoUrl, svcNm, state ,vwCnt, svcEditDt, reqstProcessPd)
    data = DBModel.ContentDB(crawl_item_id, svcCts)
    session.add(data) #Insert crawl_item DB
    session.commit()

#reqstProcessPd : 신청기한일, 거의 대부분 None 값임
def decideState(reqstProcessPd):
    now = datetime.datetime.now()
    #now 와 reqstProcessPd 비교코드 만들기


def findSiteID(site):
    #Site DB에서 'site'에 해당하는 site_id return
    for id, value in session.query(DBModel.site.site_id, DBModel.site.name).distinct():
        if (site == value):
            return id


def insertCrawlItemDB(site_id, contentUrl, title, state, views, reg_date, deadline):
    #  insert into crawl_item table
    selectData = session.query(DBModel.crawl_item).filter(DBModel.crawl_item.url == contentUrl).all()  # contentUrl을 가진 칼럼 select

    #api 는 공고 마감일이 없음
    if selectData:  # check selectData list empty
        if (selectData[0].url == contentUrl):  # url이 이미 db에 존재하는 경우, 공고 진행상태(state column)만 update
            session.query(DBModel.crawl_item).filter(DBModel.crawl_item.url == contentUrl).update({'state': state});
            session.commit()
            return 1
    else:
        data = DBModel.crawl_item(site_id, contentUrl, title, state,views, reg_date=reg_date, deadline=str(deadline))  # 존재하지 않는 url일 경우 insert
        # 이미지는 api 정보가 없음

        session.add(data) #Insert crawl_item DB
        session.commit()

        return data.crawl_id


def apiconnect(url):
    global orgCode_index

    request = ul.Request(url)
    response = ul.urlopen(request)
    rescode = response.getcode()

    # api 파싱에 성공했을 때
    if rescode == 200:
        responseData = response.read()
        # 요청받은 데이터를 읽음
        rD = xmltodict.parse(responseData)
        rDJ = json.dumps(rD)  #
        rDD = json.loads(rDJ)  # json을 dict 로

    return rDD


organization_classify()

