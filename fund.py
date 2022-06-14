from cmath import isnan
import requests
import json
import pandas as pd
import os
import time
import sys
import config
import math



# 获取基金的净值
def get_nav(code, start_date, end_date, token):
    url = 'http://api.waizaowang.com/doc/getFundNav?code={code}&startDate={startDate}&endDate={endDate}&fields=code,tdate,nav&export=1&token={token}'
    url = url.format(code=code, startDate=start_date, endDate=end_date, token=token)
    resp = requests.get(url)
    if resp:
        obj = json.loads(resp.text)
        if obj['code'] == 200:
            return obj['data']
    return ''

# 获取基金的市值
def get_price(code, start_date, end_date, token):
    url = 'http://api.waizaowang.com/doc/getCnFundDailyMarket?code={code}&startDate={startDate}&endDate={endDate}&fields=code,tdate,name,price&export=1&token={token}'
    url = url.format(code=code, startDate=start_date, endDate=end_date, token=token)
    resp = requests.get(url)
    if resp:
        obj = json.loads(resp.text)
        if obj['code'] == 200:
            return obj['data']
    return ''



def gen_one(code, start_date, end_date, out_csv):
    data1 = get_nav(code, start_date, end_date, config.waizao_token)
    df1 = pd.DataFrame(data=data1)
    # print(df1)

    data2 = get_price(code, start_date, end_date, config.waizao_token)
    df2 = pd.DataFrame(data=data2)
    # print(df2)

    df = df1.merge(df2, how='right', on='tdate')
    df['nav'] = df['nav'].astype('float')
    df['rate'] = '' 
    for index, row in df.iterrows():
        if math.isnan(row['nav']):
            continue
        rate = (row['price'] - row['nav']) / row['nav'] * 100
        df.loc[index, 'rate'] = str(round(rate, 2)) + '%' 

    df = df[['code_x', 'name', 'tdate', 'nav', 'price', 'rate']]
    df.rename(columns={'code_x':'代码', 'name':'基金名称', 'tdate':'日期', 'nav':'净值', 'price':'市价', 'rate':'溢价率'}, inplace = True)
    df.to_csv(out_csv)


def work(code_list, start_date, end_date, out_dir):
    for one in code_list:
        gen_one(one, start_date, end_date, out_dir + '/' + one + '.csv')
        print(one + ' finish')


def main():
    list =['513050', '513030', '513360', '513100', '159605', '159941', '159607'] 
    work(list, '2021-01-01', '2023-01-01', './work_dir')


if __name__ == "__main__":
    main()
