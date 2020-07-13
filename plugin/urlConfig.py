import requests


def csvToJson(data, header=2):
    p = requests.get(data, verify=False)
    p = p.content.decode('utf-8').strip().replace('\r', '').split('\n')
    header = p[header].split(',')
    d = []
    for i in p[3:len(p)]:
        i = i.split(',')
        if len(i) != len(header):
            print('wtf')
        thisDist = {}
        for j, data in enumerate(i):
            thisDist[header[j]] = data
        d.append(thisDist)
    return d


# 大學JSON
university = {
    'name': '大學資料集',
    'schools': "https://quality.data.gov.tw/dq_download_json.php?nid=6091&md5_url=2e95c3485b2b41a7eec51fa2d629d5fa",
    'libarysInfo': "https://quality.data.gov.tw/dq_download_json.php?nid=6288&md5_url=474d3f017fad0c40628f72d6d9c3fa5c",
    'libarys': "http://stats.moe.gov.tw/files/detail/108/108_library2.csv",
    'downloadData': requests.get("https://quality.data.gov.tw/dq_download_json.php?nid=6091&md5_url=2e95c3485b2b41a7eec51fa2d629d5fa", verify=False)
}
# 高中職JSON
highSchool = {
    'name': '高中職資料集',
    'schools': "https://quality.data.gov.tw/dq_download_json.php?nid=6089&md5_url=58e949f445c4e8fec0ef78ad1be3d771",
    'downloadData': requests.get("https://quality.data.gov.tw/dq_download_json.php?nid=6089&md5_url=58e949f445c4e8fec0ef78ad1be3d771")
}
# 國中
junior = {
    'name': '國中資料集',
    'schools': "http://stats.moe.gov.tw/files/school/108/j1_new.csv",
    'downloadData': csvToJson("http://stats.moe.gov.tw/files/school/108/j1_new.csv")
}
# 國小
elementary = {
    'name': '國小資料集',
    'schools': "https://quality.data.gov.tw/dq_download_json.php?nid=6087&md5_url=5825c099d4c7f424385afafbf2495d2d",
    'downloadData': requests.get("https://quality.data.gov.tw/dq_download_json.php?nid=6087&md5_url=5825c099d4c7f424385afafbf2495d2d")
}
# 資源較不足(國中小)
loseJunior = {
    'name': '資源較不足',
    'schools': "https://quality.data.gov.tw/dq_download_json.php?nid=28582&md5_url=ab863e631deac12a65ec30163c314f53",
    'downloadData': requests.get("https://quality.data.gov.tw/dq_download_json.php?nid=28582&md5_url=ab863e631deac12a65ec30163c314f53")
}
###############
# 各縣市圖書館編列統計
twLibarys = {
    'totalLibary': requests.get('https://www.nlpi.edu.tw/opendata/da08aaaf-7edd-461d-a645-3039f840a1a8', verify=False),
    # 圖書館的編列經費(縣市)
    'info': requests.get("https://quality.data.gov.tw/dq_download_json.php?nid=6425&md5_url=d2df28892756187278095473c973d09b", verify=False),
    # 可以知道圖書館的類型
    'libaryClass': requests.get("https://quality.data.gov.tw/dq_download_json.php?nid=8306&md5_url=3a7adaba0bca31a3d39903357acc8a0c", verify=False),
    # 特色圖書館
    'specialLibary': requests.get('https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=K', verify=False),
}
if __name__ == "__main__":
    pass
