import tushare as ts
import pandas as pd
import os
import time
import shutil

shutil.rmtree('balance_cache')
shutil.rmtree('profit_cache')

ts.set_token('183e070ce2f6459c5af70e4354f01f3e4e1913ef1f60a366fb1f77cb')
pro = ts.pro_api()

# 获取股票列表（需要 name 字段用于过滤 ST）
股票列表 = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
股票列表.to_csv('股票列表.csv', index=False)

# 过滤 ST 股（需要 name 列）
股票列表 = 股票列表[~股票列表['name'].str.contains('ST')]
缓存目录 = 'profit_cache'
os.makedirs(缓存目录, exist_ok=True)
年份 = [2021, 2022, 2023, 2024, 2025]
结果 = []



for 序号, 股票 in 股票列表.iterrows():
    代码 = 股票['ts_code']
    if 序号 % 10 == 0:
        print(f'利润表进度：{序号}/{len(股票列表)}')

    行数据 = {'ts_code': 代码}
    for y in 年份:
        缓存文件 = f'{缓存目录}/{代码}_{y}.csv'
        if os.path.exists(缓存文件):
            df = pd.read_csv(缓存文件)
            if not df.empty:
                d = df.iloc[0]
            else:
                continue
        else:
            try:
                df = pro.income(
                    ts_code=代码, start_date=f'{y}0101', end_date=f'{y}1231',
                    fields='ts_code,revenue,oper_cost'
                )
                if df.empty:
                    continue
                d = df.iloc[0]
                df.to_csv(缓存文件, index=False)
                time.sleep(0.35)
            except:
                continue
        行数据[f'revenue_{y}'] = d.get('revenue', 0)
        行数据[f'oper_cost_{y}'] = d.get('oper_cost', 0)
    结果.append(行数据)
    time.sleep(0.35)

利润表 = pd.DataFrame(结果)
利润表.to_csv('利润表.csv', index=False)
print('利润表获取完成')