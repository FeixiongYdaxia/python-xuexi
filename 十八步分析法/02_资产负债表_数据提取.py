import tushare as ts
import pandas as pd
import os
import time
from datetime import datetime, timedelta
import shutil

# shutil.rmtree('balance_cache')
# shutil.rmtree('profit_cache')


ts.set_token('183e070ce2f6459c5af70e4354f01f3e4e1913ef1f60a366fb1f77cb')
pro = ts.pro_api()

股票列表 = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,industry')
股票列表 = 股票列表[~股票列表['name'].str.contains('ST')]

# 获取PE/PB
尝试日期 = [(datetime.today() - timedelta(days=i)).strftime('%Y%m%d') for i in range(7)]
for 日期 in 尝试日期:
    pe_pb = pro.daily_basic(trade_date=日期)
    if not pe_pb.empty:
        print(f'已获取 PE/PB，日期：{日期}')
        break
pe_pb = pe_pb.dropna(subset=['pe', 'pb'])
pe_pb.to_csv('pe_pb.csv', index=False)

缓存目录 = 'balance_cache'
os.makedirs(缓存目录, exist_ok=True)
年份 = [2021, 2022, 2023, 2024, 2025]
结果 = []

for 序号, 股票 in 股票列表.iterrows():
    代码 = 股票['ts_code']
    if 序号 % 10 == 0:
        print(f'资产负债表进度：{序号}/{len(股票列表)}')

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
                df = pro.balancesheet(
                    ts_code=代码, start_date=f'{y}0101', end_date=f'{y}1231',
                    fields='ts_code,total_assets,total_liab,accounts_receivable,inventory,goodwill,fixed_assets'
                )
                if df.empty:
                    continue
                d = df.iloc[0]
                df.to_csv(缓存文件, index=False)
                time.sleep(0.35)
            except:
                continue
        行数据[f'total_assets_{y}'] = d.get('total_assets', 0)
        行数据[f'total_liab_{y}'] = d.get('total_liab', 0)
        行数据[f'accounts_receivable_{y}'] = d.get('accounts_receivable', 0)
        行数据[f'inventory_{y}'] = d.get('inventory', 0)
        行数据[f'goodwill_{y}'] = d.get('goodwill', 0)
        行数据[f'fixed_assets_{y}'] = d.get('fixed_assets', 0)
    结果.append(行数据)
    time.sleep(0.35)

资产负债表 = pd.DataFrame(结果)
资产负债表.to_csv('资产负债表.csv', index=False)
print('资产负债表获取完成')
