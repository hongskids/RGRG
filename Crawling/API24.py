
import urllib.request as ul
import xmltodict
import json
import sys
import io
import Model.DBModel as DBModel 
global service_key
global organizations
global orgCode_index

service_key = "eSiby8RuStqW%2F%2BpmvbtEVin7gWDGxynbYaouL6DM5y2DOziRI75s5K5nFzfnXpp3Ce3vssdZUPvYD8zPabwWUg%3D%3D"


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

                        more_service_list(svcId, svcNm, vwCnt)


# 서비스 상세 목록
def more_service_list(svcId, svcNm, vwCnt):
    print("~~~~~~~~~~~~~~~~")
    url = "http://api.korea.go.kr/openapi/svc?serviceKey=eSiby8RuStqW%2F%2BpmvbtEVin7gWDGxynbYaouL6DM5y2DOziRI75s5K5nFzfnXpp3Ce3vssdZUPvYD8zPabwWUg%3D%3D&format=xml&svcId="+str(svcId)+"&"
    result = apiconnect(url)
    print("~~~~~~~~~~~~~~~~")

    for res_val in result.values():
        for val_1 in res_val:
            if val_1 == 'svc':
                val_2 = res_val['svc']
                #print(val_2)
                for val_3 in val_2:
                    svcNm = val_2['svcNm']
                    jrsdDptAllNm = val_2['jrsdDptAllNm']
                    svcEditDt = val_2['svcEditDt']
                    slctnStdr = val_2['slctnStdr']
                    dupImprtySvc = val_2['dupImprtySvc']
                    reqstProcessPd = val_2['reqstProcessPd']
                    posesPapers = val_2['posesPapers']
                    onlnReqstSiteUrl = val_2['onlnReqstSiteUrl']
                    rcvOrgNm = val_2['rcvOrgNm']
                    rcvOrgTelNo = val_2['rcvOrgTelNo']
                    svcCts = val_2['svcCts'] # 내용
                    refrncNm = val_2['refrncNm']
                    refrncTelNo = val_2['refrncTelNo']
                    refrncSiteUrl = val_2['refrncSiteUrl']
                    svcInfoUrl = val_2['svcInfoUrl']
                    svcInfoKrUrl = val_2['svcInfoKrUrl']
                    onlnReqstSiteUrl = val_2['onlnReqstSiteUrl']
		    
    #DBModel.crawl_item(svcId, svcInfoUrl, svcNm, reqstProcessPd, views = vwCnt, reg_date = svcEditDt, deadline = None, attribute = None)
    #이미지는 api 정보가 없기때문에 None 으로 둠
    DBModel.content(svcId, svcCts)
    DBModel.site(svcNm, svcInfoUrl)

    print("아이디 : "+svcId)
    print("조회수 : "+vwCnt)
    print(" url  : "+svcInfoUrl)
    print("이름  : "+svcNm)
          

		



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

