import requests
import json
import pandas as pd
import execjs
import os
import time
import sys

def gen_hexinv():
    with open('./aes.min.js', 'r') as f:
        jscontent = f.read()
    context = execjs.compile(jscontent)
    hexinv = context.call("v")
    return hexinv

def gen_header():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,ru;q=0.8,ja;q=0.7',
        'Cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        #'Cookie': 'other_uid=Ths_iwencai_Xuangu_3p4g5xi8tag6om0non8helyrcykqvpne; ta_random_userid=xlcblzk71e; cid=84c9f5bda5a7f8b8163e182baa4719251649577284; iwencaisearchquery=%E7%91%9E%E5%BA%86%E6%97%B6%E4%BB%A3%E6%96%B0%E8%83%BD%E6%BA%90%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8; PHPSESSID=29186cb1e086080d27498be805afe0e5; cid=84c9f5bda5a7f8b8163e182baa4719251649577284; ComputerID=84c9f5bda5a7f8b8163e182baa4719251649577284; WafStatus=0; v=A_7wSd9OEPo8g0TeYvqPEW6kTx9FP8K5VAN2nagHasE8S5CBEM8SySSTxqt7',
        'Cookie': 'ta_random_userid=dih5nrpzja; WafStatus=0; cid=dd9d77e11730754a9d2088ac1cee3eba1650380878; ComputerID=dd9d77e11730754a9d2088ac1cee3eba1650380878; other_uid=Ths_iwencai_Xuangu_7p4mrj2pxia7vn3crq020dl3q83re9in; user=MDpteF82MjAyMTk1OTQ6Ok5vbmU6NTAwOjYzMDIxOTU5NDo4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxMDAwMDAwMDEwLDI4OzcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzEwMiwxLDQwOjE2Ojo6NjIwMjE5NTk0OjE2NTAzODEwMTg6OjoxNjQ0MTk5NTAwOjIyOTc4MjowOjFhN2JkYWExZjk1MzdmOWNmNWI1M2U0ZWI5N2JjYjZhMDpkZWZhdWx0XzQ6MA%3D%3D; userid=620219594; u_name=mx_620219594; escapename=mx_620219594; ticket=b729a0d521c1125c067fdc65f4b61fe7; user_status=0; utk=0a8cea6728cc9ec6fc20d16123360516; wencai_pc_version=0; PHPSESSID=e9782960bbf6b6111f756caabc1a262f; v=AzGFJzjt9_eLR1u0kUOObqjrRrbOHq6CT8ZNTRNGLC0WPl8oW261YN_iWVCg',
        'Origin': 'http://www.iwencai.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.iwencai.com/unifiedwap/result?w=%E9%92%B1%E6%B1%9F%E6%91%A9%E6%89%98%20%E5%AD%90%E5%85%AC%E5%8F%B8&querytype=stock',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'hexin-v': gen_hexinv()
    }
    return headers

def gen_payload(word, block_list='', page=1, perpage=10):
    payload = json.dumps({
        "question":word,
        "secondary_intent":"stock",
        "perpage":perpage,
        "page":page,
        "sort_key":"???????????????",
        "sort_order":"desc",
        "fund_class":"",
        "show_indexes":"[\"?????????\",\"???????????????\",\"90%????????????\",\"90%????????????\",\"????????????\",\"?????????70\",\"?????????90\",\"????????????\"]",
        "source":"Ths_iwencai_Xuangu",
        "version":"2.0",
        "query_area":"",
        "block_list":block_list, # ????????????
        "add_info":"{\"urp\":{\"scene\":1,\"company\":1,\"business\":1},\"contentType\":\"json\"}"
    })
    return payload

def wc_block_list():
    url = "http://www.iwencai.com/unifiedwap/self-stock/plate/list?stocks=0&ths=0"
    headers = gen_header()
    resp = requests.request("POST", url, headers=headers)
    if resp.status_code != 200:
        print('Error: status_code=' + str(resp.status_code))
        return
    return resp.text

def wc_search(word, block_list='', page=1, perpage=10):
    url = "http://www.iwencai.com/customized/chart/get-robot-data"
    headers = gen_header()
    payload = gen_payload(word=word, block_list=block_list, page=page, perpage=perpage)
    resp = requests.request("POST", url, headers=headers, data=payload)
    if resp.status_code != 200:
        print('Error: status_code=' + str(resp.status_code))
        return

    try:
        b = json.loads(resp.text)
        a = b['data']['answer'][0]['txt'][0]['content']['components'][0]['data']['datas']
        return a
    except Exception:
        import traceback
        traceback.print_exc()
    return None

#
#           {
#              "code":"600519",
#              "????????????":"600519.SH",
#              "????????????":"????????????",
#              "market_code":"17",

#              "?????????":"1797.00",
#              "???????????????":"0.374",
#              "?????????:?????????[20220420]":"1820",
#              "?????????:?????????[20220420]":"1768.68",

#              "????????????[20220420]":38.289,
#              "????????????[20220420]":1832.07,

#              "90%????????????[20220420]":2127.9,
#              "90%????????????[20220420]":1655.61,

#              "?????????90[20220420]":12.483,
#              "?????????70[20220420]":8.391,

#              "????????????????????????(roe)?????????[20231231]":27.2224,
#              "??????????????????roe(??????,?????????)[20211231]":29.9,
#              "????????????????????????(roe)?????????[20241231]":26.7322,
#              "?????????[20220420]":2257387446600,
#              "????????????????????????(roe)?????????[20221231]":27.6364
#              "???????????????????????????????????????[20211231]":52460144378.16,
#              "a?????????(???????????????)[20220420]":"2257387400000.000",

#              "??????????????????":"20010827",
#              "????????????[20220420]":7542,
#              "??????????????????[20211231]":196957506705.34,
#              "?????????????????????":"????????????-????????????-??????",
#          },
#

def gen_out_filename():
    return 'out.csv'

def gen_date_str():
    return get_latest_trade_date().replace('-', '')

# ?????????????????????????????????
def get_latest_trade_date():
    url = 'http://api.waizaowang.com/doc/getTradeDate?mtype=1&startDate={startDate}&endDate={endDate}&fields=all&export=1&token=fae13bef7f59af97a52352d34ea6336f'
    s = time.strftime("%Y-%m-%d", time.localtime())
    url = url.format(startDate=s, endDate=s)
    resp = requests.get(url)
    print('get_latest_trade_date=' + resp.text)
    if resp:
        obj = json.loads(resp.text)['data'][0]
        if obj['isopen'] == 2:
            return obj['lastdate']
        else:
            return obj['tdate']
    return s

def gen_email_body(bodyfile):
    body = 'Error'
    with open(bodyfile, 'rb') as f:
        body = f.read().decode()
    return body

def gen_email_subject():
    s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return s + ' ?????????????????????'

def send_email(merge_csv):
    import config
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart()
    message['From'] = config.user
    message['To'] = ','.join(config.receivers)
    message['subject'] = gen_email_subject()
    body = MIMEText(gen_email_body('./email_body.html'), 'html', 'utf-8')
    message.attach(body)

    filename = merge_csv.split('/')[1]
    att = MIMEText(open(merge_csv, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="'+ filename + '"'
    message.attach(att)
    
    try:
        smtp = smtplib.SMTP()
        smtp.connect(config.smtpserver)
        smtp.login(config.user, config.password)
        smtp.sendmail(config.user, config.receivers, message.as_string())
        smtp.quit()
        print("??????????????????")
    except smtplib.SMTPException:
        print("Error: ??????????????????")


def get_base_filter_list(out_csv, send_email=False):
    if os.path.exists(out_csv):
        os.remove(out_csv)

    date_str = gen_date_str()
    word = 'st????????????????????????50??????roe>0???688??????????????????????????????????????????5?????????????????????101%??????????????????????????????????????????????????????'
    columns=[
        '????????????',
        '????????????',
        '????????????' + '[' + date_str + ']', 
        '?????????:?????????' + '[' + date_str + ']',
        '?????????:?????????' + '[' + date_str + ']',
        '?????????', 
        '90%????????????' + '[' + date_str + ']',
        '?????????90' + '[' + date_str + ']',
        '???????????????',
    ]
    res = pd.DataFrame(columns=columns, data=[])
    count = 0
    for i in range(1, 10):
        data = wc_search(word, page=i, perpage=100)
        df = pd.DataFrame(columns=columns, data=data)
        res = pd.concat([res, df], ignore_index=True)
        size = len(data)
        count = count + size
        if size<100:
            break
    
    long_col = '????????????' + '[' + date_str + ']'
    res[long_col] = res[long_col].map('{}%'.format, na_action='ignore')
    res['???????????????'] = res['???????????????'].map('{}%'.format, na_action='ignore')
    res.to_csv(out_csv)
    print('total:' + str(count))

    if send_email:
        send_email(out_csv)

    return out_csv

# ??????????????????????????????
def get_block_data(sn, out_csv=None):
    if not sn:
        print('Error: get_block_data() sn is none')
        return

    data = wc_search('?????????????????????????????????????????????????????????', block_list=sn, page=1, perpage=100)
    
    
    if out_csv and os.path.exists(out_csv):
        os.remove(out_csv)
    date_str = gen_date_str()
    limit90_col_name = '90%????????????' + '[' + date_str + ']' 
    columns=[
        '????????????', 
        '????????????', 
        limit90_col_name,
        '??????????????????5%',
        '?????????', 
        '???????????????',
        '?????????:?????????' + '[' + date_str + ']',
        '?????????:?????????' + '[' + date_str + ']'
        ]
    for one in data:
        if limit90_col_name not in one:
            continue
        limit90 = one[limit90_col_name]

        if '?????????' not in one:
            continue
        price = float(one['?????????'])

        one['??????????????????5%'] = round(limit90 * 0.95, 3)
        one['???????????????'] = round((limit90-price)/limit90*100, 2)

    df = pd.DataFrame(columns=columns, data=data)
    df = df.sort_values(by=['???????????????'], ascending=[False])
    df['???????????????'] = df['???????????????'].map('{}%'.format, na_action='ignore')
    if out_csv:
        df.to_csv(out_csv)
    print('Sucess to csv data count' + str(len(data)))
    return df


def gen_base_filter_name():
    s = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    out_csv = WORK_DIR + '/stock_' + s + '.csv'
    return out_csv


def gen_block_file_name(sn):
    s = time.strftime("%Y_%m_%d", time.localtime())
    out_csv = WORK_DIR + '/block_' + sn + '_' + s + '.csv'
    return out_csv


WORK_DIR = './work_dir'

def main():
    if len(sys.argv) < 2:
        print('Error: ????????????')
        return
    
    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)

    opt = sys.argv[1]
    if '-base' == opt:
        get_base_filter_list(gen_base_filter_name())
        return

    if '-sn' == opt:
        sn = sys.argv[2]
        get_block_data(sn, gen_block_file_name(sn))
        return
    
    if '-allsn' == opt:
        obj = json.loads(wc_block_list())
        for one in obj['data']:
            sn = one['sn']
            get_block_data(sn, gen_block_file_name(sn))
        return
    
    print('Error: unknow argv ' + str(sys.argv))


if __name__ == "__main__":
    main()
