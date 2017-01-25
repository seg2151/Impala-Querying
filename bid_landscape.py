# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 11:44:07 2016

@author: sgarcia
"""
filename = '.xlsx'
from bid_landscape_sql_scripts import scripts
import pandas as pd
from impala.dbapi import connect
from impala.util import as_pandas
print('Connecting to host...')
conn = connect(host = '', port = 21050)
cursor = conn.cursor()
df_list = []
for script in scripts:
    print('Executing script...')
    cursor.execute(script)
    print('SQL script exectued')
    df_list.append(as_pandas(cursor))
print('Merging dataframes')
df = df_list[0].merge(df_list[1], on='accountname')
df['bidcpm'] = df.bidprice/df.bidsmade*1000
writer = pd.ExcelWriter(filename)
df.to_excel(writer, 'Sheet1')
df_list[2].to_excel(writer, 'Sheet2')
writer.save()

