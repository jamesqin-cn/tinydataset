# Tiny DataSet

## What is TinyDataSet?
tinydataset is two dememsional array, which implements with a list of dictionaries, generated by mysql query action generally.
```
table = [
    {'stat_date': '2020-01-01', 'k1':'a', 'k2':1},
    {'stat_date': '2020-01-02', 'k1':'b', 'k2':2},
    {'stat_date': '2020-01-03', 'k1':'c', 'k2':3}
]
```
Generally speaking, you may fetch a list of dictionaries after execute mysql query like this:
```
conn = pymysql.connect(...)
conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute("SELECT stat_date,k1,k2,k3 FROM example_table LIMIT 10")
cursor.fetchall()
cursor.close()
conn.close()
```
This package provides some functions for processing table data structures


## Programming Language
- python 2.7
- python 3.7

## Install
```
pip install tinydataset
```

## Quick Start
```
from tinydataset import *

class Test_TinyDataSet(unittest.TestCase):

    def test_VLookupCol(self):
        table = [
            {'stat_date': '2020-01-01', 'a':'a', 'x':1},
            {'stat_date': '2020-01-02', 'b':'b', 'x':2},
            {'stat_date': '2020-01-03', 'c':'c', 'x':3}
        ]
        self.assertEqual(VLookupCol(table,'a',0,stat_date='2020-01-02'), 0)
        self.assertEqual(VLookupCol(table,'b',0,stat_date='2020-01-02'), 'b')
        self.assertEqual(VLookupCol(table,'b',0,stat_date='2020-01-02',x=2), 'b')
        self.assertEqual(VLookupCol(table,'b',0,stat_date='2020-01-02',x=3), 0)

    def test_TableLeftJoin(self):
        t1 = [
            {'stat_date': '2020-01-01', 'x':1},
            {'stat_date': '2020-01-02', 'x':2},
            {'stat_date': '2020-01-03', 'x':3}
        ]
        t2 = [
            {'stat_date': '2020-01-01', 'y':4},
            {'stat_date': '2020-01-02', 'y':5},
            {'stat_date': '2020-01-03', 'y':6}
        ]
        t3 = [
            {'stat_date': '2020-01-01', 'x':1, 'y':4},
            {'stat_date': '2020-01-02', 'x':2, 'y':5},
            {'stat_date': '2020-01-03', 'x':3, 'y':6}
        ]
        self.assertEqual(TableLeftJoin('stat_date', t1, t2), t3)

    def test_FillTableWithDateRange(self):
        table = [
            {'stat_date': '2020-01-02', 'a': 'a'},
            {'stat_date': '2020-01-03', 'c': 'c'}
        ]
        new_table = FillTableWithDateRange(table, '2020-01-05', '2020-01-01', 'stat_date')
        self.assertEqual(new_table[0]['stat_date'], '2020-01-05')
        self.assertEqual(new_table[0]['a'], 0)
        self.assertEqual(new_table[0]['c'], 0)
        self.assertEqual(new_table[4]['stat_date'], '2020-01-01')
        self.assertEqual(new_table[0]['a'], 0)
        self.assertEqual(new_table[0]['c'], 0)

    def test_MakeDateRangeTable(self):
        expected_table = [
            {'stat_date': '2020-01-01'}, 
            {'stat_date': '2020-01-02'}, 
            {'stat_date': '2020-01-03'}
        ]
        self.assertEqual(MakeDateRangeTable('2020-01-01', '2020-01-03', 'stat_date'), expected_table)

    def test_FillTableMissingColumn(self):
        table = [
            {'stat_date': '2020-01-01', 'a': 'a'},
            {'stat_date': '2020-01-02', 'b': 'b'},
            {'stat_date': '2020-01-03', 'c': 'c'}
        ]
        full_filled_table = [
            {'stat_date': '2020-01-01', 'a':'a', 'b': 0,  'c': 0 },
            {'stat_date': '2020-01-02', 'a': 0,  'b':'b', 'c': 0 },
            {'stat_date': '2020-01-03', 'a': 0,  'b': 0,  'c':'c'},
        ]
        self.assertEqual(FillTableMissingColumn(table),full_filled_table)

    def test_ExtractArrayFromTableByCol(self):
        table = [
            {'stat_date': '2020-01-01', 'a': 'a'},
            {'stat_date': '2020-01-02', 'b': 'b'},
            {'stat_date': '2020-01-03', 'c': 'c'}
        ]
        self.assertEqual(ExtractArrayFromTableByCol(table,'a'), ['a', 0,  0 ])
        self.assertEqual(ExtractArrayFromTableByCol(table,'b'), [ 0, 'b', 0 ])
        self.assertEqual(ExtractArrayFromTableByCol(table,'c'), [ 0,  0, 'c'])

    def test_MaxInTable(self):
        table = [
            {'stat_date': '2020-01-01', 'v': 1, u'中文':9},
            {'stat_date': '2020-01-02', 'v': 2, u'中文':5},
            {'stat_date': '2020-01-03', 'v': 3}
        ]
        self.assertEqual(MaxInTable(table, 'v'), 3)
        self.assertEqual(MaxInTable(table, u'中文'), 9)

    def test_SumInTable(self):
        table = [
            {'stat_date': '2020-01-01', 'v': 1, u'中文':9},
            {'stat_date': '2020-01-02', 'v': 2, u'中文':5},
            {'stat_date': '2020-01-03', 'v': 3}
        ]
        self.assertEqual(SumInTable(table, 'v'), 6)
        self.assertEqual(SumInTable(table, u'中文'), 14)
```

## Function List
- Lookup Tools
    - VLookupCol(table_array, return_col, return_default_val = None, **conditions)
    - VLookupRow(table_array, **conditions):
- Table Tools
    - TableLeftJoin(pri_key, *tables):
    - FillTableWithDateRange(table_array, begin_date, end_date, date_col_name):
    - MakeDateRangeTable(begin_date, end_date, date_col_name):
    - FillTableMissingColumn(table_array, default_val = 0):
    - ExtractArrayFromTableByCol(table_array, col_name, default_val = 0):
    - MaxInTable(table_array, col_name):
    - SumInTable(table_array, col_name):
    - ReverseTable(table):