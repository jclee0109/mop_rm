import re
import pandas as pd

tmp_string="화 19:00~21:00\n 목 12:00~21:00"
numbers = re.findall("\d+", tmp_string)
print('%s ==> %s'%(tmp_string,numbers))

text = "화 12:00~21:00\n 목 12:00~21:00"
days = re.compile("[가-힣]+").findall(text)
print(('%s ==> %s')%(text, days))

Location = 'C:/Users/이주찬/Desktop'
File = 'Excel_Timetable.xls'

Row = 10
Column = 7

data_pd = pd.read_excel('{}/{}'.format(Location, File),
                        header=None, index_col=None, names=None)
data_np = pd.DataFrame.to_numpy(data_pd)


print(data_pd)
print(data_np[Row][Column])