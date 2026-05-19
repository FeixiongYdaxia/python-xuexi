import pandas as pd
from datetime import datetime
from tabulate import tabulate

# 在你的04_数据分析_2.py里，找一下这几行
利润表 = pd.read_csv('利润表.csv')
资产负债表 = pd.read_csv('资产负债表.csv')

# ==================== 权重配置 ====================
权重 = {
    '总资产增长率': 0.10,
    '资产负债率': 0.10,
    '短期还款能力': 0.05,
    '行业地位': 0.10,
    '产品竞争力': 0.10,
    '暴雷风险': 0.00,
    '资产类型': 0.05,
    '企业专注力': 0.05,
    '毛利率': 0.10,
    '净利率': 0.10,
    '营收增长率': 0.05,
    'pe': 0.10,
    'pb': 0.10
}
# =================================================

# 读取数据
合并表格 = pd.read_csv('合并表格.csv')
print(f'已读取 {len(合并表格)} 只股票的信息')

# ==================== 资产负债表分析函数 ====================
def 计算总资产增长率(行):
    total_assets_2025 = 行.get('total_assets_2025', 0)
    total_assets_2024 = 行.get('total_assets_2024', 0)
    if total_assets_2024 > 0:
        return round((total_assets_2025 - total_assets_2024) / total_assets_2024 * 100, 2)
    return 0

def 计算资产负债率(行):
    total_liab = 行.get('total_liab_2025', 0)
    total_assets = 行.get('total_assets_2025', 0)
    if total_assets > 0:
        return round(total_liab / total_assets * 100, 2)
    return 0

def 计算短期还款能力(行):
    short_loan = 行.get('short_loan_2025', 0)
    long_loan = 行.get('long_loan_2025', 0)
    bond_payable = 行.get('bond_payable_2025', 0)
    有息负债 = short_loan + long_loan + bond_payable
    money_cap = 行.get('money_cap_2025', 0)
    trad_fin_asset = 行.get('trad_fin_asset_2025', 0)
    现金 = money_cap + trad_fin_asset
    inventory = 行.get('inventory_2025', 0)
    缺口 = 有息负债 - 现金 - inventory
    return '充足' if 缺口 <= 0 else '紧张'

def 计算行业地位(行):
    acct_payable = 行.get('acct_payable_2025', 0)
    notes_payable = 行.get('notes_payable_2025', 0)
    contract_liab = 行.get('contract_liab_2025', 0)
    应付 = acct_payable + notes_payable + contract_liab
    accounts_receivable = 行.get('accounts_receivable_2025', 0)
    notes_receivable = 行.get('notes_receivable_2025', 0)
    pre_payment = 行.get('pre_payment_2025', 0)
    contract_assets = 行.get('contract_assets_2025', 0)
    应收 = accounts_receivable + notes_receivable + pre_payment + contract_assets
    return round(应付 - 应收, 2)

def 计算产品竞争力(行):
    accounts_receivable = 行.get('accounts_receivable_2025', 0)
    contract_assets = 行.get('contract_assets_2025', 0)
    应收合计 = accounts_receivable + contract_assets
    fixed_assets = 行.get('fixed_assets_2025', 0)
    if fixed_assets <= 0:
        return '无固定资产'
    比率 = 应收合计 / fixed_assets
    if 比率 > 0.15:
        return '弱'
    elif 比率 < 0.01:
        return '非常优秀'
    elif 比率 < 0.03:
        return '较好'
    else:
        return '一般'

def 计算暴雷风险(行):
    total_assets = 行.get('total_assets_2025', 0)
    if total_assets <= 0:
        return '数据不足'
    accounts_receivable = 行.get('accounts_receivable_2025', 0)
    inventory = 行.get('inventory_2025', 0)
    goodwill = 行.get('goodwill_2025', 0)
    应收占比 = accounts_receivable / total_assets
    存货占比 = inventory / total_assets
    商誉占比 = goodwill / total_assets
    if (应收占比 > 0.05 and 存货占比 > 0.15) or 商誉占比 > 0.10:
        return '存在风险'
    return '可控'

def 计算资产类型(行):
    fixed_assets = 行.get('fixed_assets_2025', 0)
    const_in_prog = 行.get('const_in_prog_2025', 0)
    eng_material = 行.get('eng_material_2025', 0)
    重资产 = fixed_assets + const_in_prog + eng_material
    total_assets = 行.get('total_assets_2025', 0)
    if total_assets <= 0:
        return '数据不足'
    return '重资产' if 重资产 / total_assets > 0.4 else '轻资产'

def 计算企业专注力(行):
    fin_assets_fvpl = 行.get('fin_assets_fvpl_2025', 0)
    available_for_sale = 行.get('available_for_sale_fin_assets_2025', 0)
    long_term_equity = 行.get('long_term_equity_invest_2025', 0)
    金融资产 = fin_assets_fvpl + available_for_sale + long_term_equity
    total_assets = 行.get('total_assets_2025', 0)
    if total_assets <= 0:
        return '数据不足'
    return '专注力不足' if 金融资产 / total_assets > 0.10 else '专注力良好'

# ==================== 利润表分析函数 ====================
def 计算毛利率(行):
    revenue = 行.get('revenue_2025', 0)
    oper_cost = 行.get('oper_cost_2025', 0)
    if revenue > 0:
        return round((revenue - oper_cost) / revenue * 100, 2)
    return 0

def 计算净利率(行):
    n_income = 行.get('n_income_2025', 0)
    revenue = 行.get('revenue_2025', 0)
    if revenue > 0:
        return round(n_income / revenue * 100, 2)
    return 0

def 计算营收增长率(行):
    revenue_2025 = 行.get('revenue_2025', 0)
    revenue_2024 = 行.get('revenue_2024', 0)
    if revenue_2024 > 0:
        return round((revenue_2025 - revenue_2024) / revenue_2024 * 100, 2)
    return 0

# ==================== 应用所有分析 ====================
合并表格['总资产增长率'] = 合并表格.apply(计算总资产增长率, axis=1)
合并表格['资产负债率'] = 合并表格.apply(计算资产负债率, axis=1)
合并表格['短期还款能力'] = 合并表格.apply(计算短期还款能力, axis=1)
合并表格['行业地位'] = 合并表格.apply(计算行业地位, axis=1)
合并表格['产品竞争力'] = 合并表格.apply(计算产品竞争力, axis=1)
合并表格['暴雷风险'] = 合并表格.apply(计算暴雷风险, axis=1)
合并表格['资产类型'] = 合并表格.apply(计算资产类型, axis=1)
合并表格['企业专注力'] = 合并表格.apply(计算企业专注力, axis=1)
合并表格['毛利率'] = 合并表格.apply(计算毛利率, axis=1)
合并表格['净利率'] = 合并表格.apply(计算净利率, axis=1)
合并表格['营收增长率'] = 合并表格.apply(计算营收增长率, axis=1)

# 过滤暴雷风险
合并表格 = 合并表格[合并表格['暴雷风险'] != '存在风险']
print(f'过滤暴雷风险后剩余 {len(合并表格)} 只股票')

# ==================== 分位数打分 ====================
# 越高越好的指标
for col in ['总资产增长率', '行业地位', '毛利率', '净利率', '营收增长率']:
    合并表格[f'{col}_得分'] = 合并表格[col].rank(pct=True)

# 越低越好的指标
for col in ['资产负债率']:
    合并表格[f'{col}_得分'] = 1 - 合并表格[col].rank(pct=True)

# 定性指标得分
定性得分 = {
    '短期还款能力': {'充足': 1.0, '紧张': 0.0},
    '产品竞争力': {'非常优秀': 1.0, '较好': 0.8, '一般': 0.5, '弱': 0.2, '无固定资产': 0.0},
    '资产类型': {'轻资产': 1.0, '重资产': 0.5, '数据不足': 0.0},
    '企业专注力': {'专注力良好': 1.0, '专注力不足': 0.3, '数据不足': 0.0}
}

for col, 映射 in 定性得分.items():
    合并表格[f'{col}_得分'] = 合并表格[col].map(映射).fillna(0)

# 估值指标
合并表格['pe_得分'] = 1 - 合并表格['pe'].rank(pct=True)
合并表格['pb_得分'] = 1 - 合并表格['pb'].rank(pct=True)

# ==================== 计算综合得分 ====================
def 计算得分(行):
    得分 = 0
    得分 += 行['总资产增长率_得分'] * 权重['总资产增长率']
    得分 += 行['资产负债率_得分'] * 权重['资产负债率']
    得分 += 行['短期还款能力_得分'] * 权重['短期还款能力']
    得分 += 行['行业地位_得分'] * 权重['行业地位']
    得分 += 行['产品竞争力_得分'] * 权重['产品竞争力']
    得分 += 行['资产类型_得分'] * 权重['资产类型']
    得分 += 行['企业专注力_得分'] * 权重['企业专注力']
    得分 += 行['毛利率_得分'] * 权重['毛利率']
    得分 += 行['净利率_得分'] * 权重['净利率']
    得分 += 行['营收增长率_得分'] * 权重['营收增长率']
    得分 += 行['pe_得分'] * 权重['pe']
    得分 += 行['pb_得分'] * 权重['pb']
    return round(得分, 2)

合并表格['综合得分'] = 合并表格.apply(计算得分, axis=1)

# 取前10
筛选结果 = 合并表格.sort_values('综合得分', ascending=False).head(10)
筛选结果 = 筛选结果.rename(columns={'ts_code': '股票代码'})

# 打印结果
print('\n' + '=' * 100)
print('财报分析筛选结果 TOP 10')
print('=' * 100)
print(tabulate(筛选结果[['股票代码', 'name', 'pe', 'pb',
                         '总资产增长率', '资产负债率', '短期还款能力',
                         '行业地位', '产品竞争力', '暴雷风险',
                         '资产类型', '企业专注力',
                         '毛利率', '净利率', '营收增长率', '综合得分']],
               headers='keys', tablefmt='simple', showindex=False, floatfmt='.2f'))
print('=' * 100)

# 保存Excel
今日日期 = datetime.today().strftime('%Y%m%d')
文件名 = f'财报分析结果_{今日日期}.xlsx'
筛选结果.to_excel(文件名, index=False)
print(f'文件已保存到 {文件名}')

