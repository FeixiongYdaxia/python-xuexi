import pandas as pd

pe_pb = pd.read_csv('pe_pb.csv')
资产负债表 = pd.read_csv('资产负债表.csv')
利润表 = pd.read_csv('利润表.csv')
股票列表 = pd.read_csv('股票列表.csv')[['ts_code', 'name']]

合并 = pd.merge(pe_pb, 资产负债表, on='ts_code', how='inner')
合并 = pd.merge(合并, 利润表, on='ts_code', how='inner')
合并 = pd.merge(合并, 股票列表, on='ts_code', how='inner')

合并.to_csv('合并表格.csv', index=False)
print(f'合并完成，共 {len(合并)} 只股票')

