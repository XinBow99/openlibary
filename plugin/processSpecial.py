from plugin import urlConfig
import requests
import re
import json
# from plugin


def allCombine(debug=False):
    pass


def universityLibary(debug=False):
    university = urlConfig.university['libarys']
    university = urlConfig.csvToJson(university, 0)
    return university


def libaryCombie(debug=False):
    # 全台公共圖書館
    totalLibary = urlConfig.twLibarys['totalLibary']
    # 圖書館資訊(縣市)
    keyInfo = urlConfig.twLibarys['info']
    # 基礎分類的圖書館
    libaryClass = urlConfig.twLibarys['libaryClass']
    # 特別分類的
    specialLibary = urlConfig.twLibarys['specialLibary']

    libarys = [
        totalLibary,
        keyInfo,
        libaryClass,
        specialLibary
    ]

    # debug
    if debug:
        for i in libarys:
            print('-----------------------------------------------------------------')
            print(i.json()[0])

    # row
    for testCode in libarys:
        if testCode.status_code != 200:
            return {
                'msg': 'not 200'
            }
    # 進行最終合併

    publicLibary = totalLibary.json()
    specialLibary = specialLibary.json()
    #allLibary = libaryClass.json()

    newKeyInfo = []
    for info in keyInfo.json():
        info.update(
            {
                'publicLibary': [],  # putTotalLibary(Public)
                'specialLibary': [],  # putSpecial
                'allLibary': []  # putAllLibary
            }
        )
        newKeyInfo.append(info)

    def putLib(pLibary, putKey, cityKey):
        for lib in pLibary:
            for i, area in enumerate(newKeyInfo):
                checkCity = area['縣市別']
                if lib[cityKey].split(' ')[0] in checkCity:
                    #print(lib[cityKey].split(' ')[0])
                    newKeyInfo[i][putKey].append(lib)
                if checkCity == "2019-全國":
                    newKeyInfo[i]['allLibary'].append(lib)
    putLib(publicLibary, 'publicLibary', '所屬縣市')
    putLib(specialLibary, 'specialLibary', 'cityName')
    #putLib(allLibary, 'allLibary', '所屬縣市')

    print("全國書館合併完成")
    return newKeyInfo


def getConvertJson():
    o = open('jsonFiles/convertSchool.json', 'r', encoding='utf8')

    return json.loads(o.read())


def schoolCombine(debug=False):

    university = urlConfig.university
    highSchool = urlConfig.highSchool
    junior = urlConfig.junior
    elementary = urlConfig.elementary
    losejuniorandelementary = urlConfig.loseJunior
    # debug
    if debug:
        testData = [
            university,
            highSchool,
            junior,
            elementary,
            losejuniorandelementary
        ]
        for test in testData:
            print(test['name'])
            if test['name'] == "國中資料集":
                print(len(test['downloadData']))
                print(test['downloadData'][0])
                continue
            print(len(test['downloadData'].json()))
            print(test['downloadData'].json()[0])
    # debug end
    # next step
    # fi lost
    lostDist = {}
    for i in losejuniorandelementary['downloadData'].json():
        sName = i['本校名稱']
        del i['本校名稱']
        del i['公/私立']
        lostDist[sName] = i
    # combie all school
    schoolsData = [
        university,
        highSchool,
        junior,
        elementary
    ]
    schools = []  # save all school
    for data in schoolsData:
        print(data['name'], "合併中")
        if data['name'] == "國中資料集":
            for s in data['downloadData']:
                if s['學校名稱'] in lostDist:
                    if lostDist[s['學校名稱']]['本校代碼'] == s['代碼']:
                        del lostDist[s['學校名稱']]['本校代碼']
                        s.update(
                            lostDist[s['學校名稱']]
                        )
                schools.append(s)
            continue
        if str(data['downloadData'].status_code) == "200":
            for s in data['downloadData'].json():
                flag = False
                if data['name'] == "國小資料集":
                    if s['學校名稱'] in lostDist:
                        if '本校代碼' in lostDist[s['學校名稱']]:
                            if lostDist[s['學校名稱']]['本校代碼'] == s['代碼']:
                                flag = True
                                del lostDist[s['學校名稱']]['本校代碼']
                                s.update(
                                    lostDist[s['學校名稱']]
                                )
                        else:
                            if lostDist[s['學校名稱']]['縣市名稱'] == s['縣市名稱']:
                                flag = True
                                s.update(
                                    lostDist[s['學校名稱']]
                                )
                s.update(
                    {'isLoseResource': flag}
                )
                schools.append(s)
    o = open('convert.json', 'w', encoding='utf8')
    jsons = open('jsonFiles/schoolsNumber1.json', 'r',
                 encoding="utf8").read().split('\n')
    for i, school in enumerate(schools):
        school['地址'] = {
            'simple': school['地址'],
            'advance': json.loads(jsons[i])
        }
        # print(school['地址'])

    o.write(
        json.dumps(
            schools,
            ensure_ascii=False
        )
    )
    return schools


if __name__ == "__main__":
    schoolCombine()
    # outPutNewJson("新北市石碇區北宜路五段坑內巷1號")
