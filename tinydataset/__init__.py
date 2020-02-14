# -*- coding:utf-8 -*-

import math
from datetime import datetime,timedelta

# 实现类似excel表的vlookup功能
def  VLookupCol(table_array, return_col, return_default_val = None, **conditions):
    row = VLookupRow(table_array, **conditions)
    return row[return_col] if row is not None and return_col in row else return_default_val

def  VLookupRow(table_array, **conditions):
    for row in table_array:
        find_it = True
        for (find_col,find_val) in conditions.items():
            if row[find_col] != find_val:
                find_it = False
                break
        if find_it:
            return row

    return None

# 规整MySQL返回的二维矩阵，确保名为 date_col_name 的列存在[begin_date, end_date]的连续取值。该函数一般用于画图时预先补齐不存在的行
def FillTableWithDateRange(table_array, begin_date, end_date, date_col_name):
    date_table_array = MakeDateRangeTable(begin_date, end_date, date_col_name)
    new_table = TableLeftJoin(date_col_name, date_table_array, table_array)
    new_table = FillTableMissingColumn(new_table)
    return new_table

# 生成一个二维矩阵，存在名为 date_col_name 的列，且取值为[begin_date, end_date]的连续区间
def MakeDateRangeTable(begin_date, end_date, date_col_name):
    date_list = GetEveryDay(begin_date, end_date)
    table_array = []
    for date in date_list:
        table_array.append({date_col_name:date})
    return table_array

# 两表在内存中实现类似MySQL的left join功能
def TableLeftJoin(pri_key, *tables):
    if len(tables) == 0:
        raise Exception("At least one table is required")

    if len(tables[0]) == 0:
        raise Exception("At least one row is required")

    if pri_key not in tables[0][0]:
        raise Exception("The first table doesn't have primary key column: " + pri_key)

    new_table = []
    for row in tables[0]:
        v = row[pri_key]
        new_row = row
        for table in tables[1:]:
            conditions = {pri_key:v}
            row = VLookupRow(table, **conditions)
            if row is not None:
                new_row.update(row)
        new_table.append(new_row)
    return new_table

# 将稀疏矩阵转化为完全矩阵
def FillTableMissingColumn(table_array, default_val = 0):
    keys = set()
    for row in table_array:
        keys.update(row.keys())

    new_table = []
    for row in table_array:
        new_row = {}
        for k in keys:
            new_row[k] = row.get(k, default_val)
        new_table.append(new_row)
    return new_table

# 从二维矩阵按某一列抽出一个一维数组
def ExtractArrayFromTableByCol(table_array, col_name, default_val = 0):
    return [row.get(col_name, default_val) for row in table_array]

def MaxInTable(table_array, col_name):
    v = None
    for row in table_array:
        the_one = row.get(col_name, None)
        if the_one is not None:
            if v is not None:
                v = max(v, the_one)
            else:
                v = the_one
    return v

def SumInTable(table_array, col_name):
    s = 0
    for row in table_array:
        s += float(row.get(col_name, 0))
    return s

def ReduceDateArray(arr, step = 5):
    new_arr = []
    for i,val in enumerate(arr):
        if i % step == 0:
            new_val = datetime.strptime(val, '%Y-%m-%d').strftime("%m%d")
            new_arr.append(new_val)
        else:
            new_arr.append('')
    new_arr[-1] = datetime.strptime(arr[-1], '%Y-%m-%d').strftime("%m%d")
    return new_arr

def ReverseTable(table):
    new_table = []
    for row in table:
        new_table.insert(0, row)
    return new_table

def GetEveryDay(begin_date, end_date):
    step = 1 if begin_date <= end_date else -1

    date_list = []
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date,"%Y-%m-%d")
    while True:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        if begin_date == end_date:
            break
        begin_date += timedelta(days=step)
    return date_list

