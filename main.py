import re
import urllib.request
import urllib.error
import json
import pandas as pd
import openpyxl

if __name__ == '__main__':
    #hsr_cache 其中有抽卡记录网址（需要打开记录页面）
    file_path = 'D:/starRail/Star Rail/Game/StarRail_Data/webCaches/2.27.0.0/Cache/Cache_Data/data_2'
    # 使用rb进行二进制阅读
    with open(file_path, 'rb') as fp:
        cache_file = fp.read()
    # 使用正则找到其中的网址
    regex = re.compile(b'(https://public-operation-hkrpg.mihoyo.com/common/gacha_record/api/getGachaLog.+?)\0')
    matches = regex.findall(cache_file)
    #得到抽卡信息的网址
    warp_url = matches[0].decode('utf-8')
    end_id = ''
    #将size替换为20
    url = re.sub(r'(size=)\d+', r'\g<1>20', warp_url)

    # 创造excel workbook
    workbook = openpyxl.Workbook()
    file_name = '抽卡记录.xlsx'
    workbook.save(file_name)
    is_first_loop = True
    try:
        for j in range(2):
            f = urllib.request.urlopen(url)
            #获得二进制的页面信息
            pull = f.read()#.decode('utf-8')
            data = json.loads(pull)
            if is_first_loop:
                df = pd.json_normalize(data['data']['list'])
                is_first_loop = False
            else:
                df = df.append(pd.json_normalize(data['data']['list']))
            for i in data['data']['list']:
                #需要修改为：i加入excel表格
                #print(i)
                #将i放进sheet中
                end_id = i['id']
            url = re.sub(r'(end_id=)\d+', fr'\g<1>{end_id}', url)
        #print(df)
        df.to_excel(file_name, index=False)


    except urllib.error.URLError as e:
        print(e)
