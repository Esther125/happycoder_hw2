import requests
from bs4 import BeautifulSoup
import pandas as pd

stock_num = 2412

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}

# 發出網路請求
resp = requests.get(f'https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID={stock_num}', headers=headers)
# 設定編碼
resp.encoding = 'utf-8'
# 將回傳的網頁內容轉換成 BeautifulSoup 物件
soup = BeautifulSoup(resp.text, 'html.parser')

# 將資料組織成 dict
dividend_data = {
    'datetime': [],
    'dividend': []
}

# 取出近五年資料(n = 5, 6, 7, ...10，注意 range 不含結尾 11)
for n in range(5, 11):
    # table row 第五行開始資料（之前為標頭）
    # td 第一欄為時間
    # f'{變數}' 為 Python 字串格式化，可以將變數在字串中進行替換，簡化寫法。以下將 n 替換成 5, 6, 7...10
    datetime_items = soup.select(f'#divDetail > table > tr:nth-child({n}) > td:nth-child(1)')[0].text
    print('datetime_items', datetime_items)
    # td 第四欄為現金股利總和
    dividend_items = soup.select(f'#divDetail > table > tr:nth-child({n}) > td:nth-child(4)')[0].text
    dividend_data['datetime'].append(datetime_items)
    dividend_data['dividend'].append(dividend_items)

# 印出組織成果
print('dividend_data', dividend_data)

# 將 dict 轉換成 pandas DataFrame 結構
df = pd.DataFrame.from_dict(dividend_data)
# 將 DataFrame 轉成 csv 檔案
df.to_csv(f'dividend_{stock_num}.csv', index=False)