import re
import pandas as pd
import numpy

# tmp_string="화 19:00~21:00\n 목 12:00~21:00"
# numbers = re.findall("\d+", tmp_string)
# print('%s ==> %s'%(tmp_string,numbers))
#
# text = "화 12:00~21:00\n 목 12:00~21:00 화 12:00~13:00"
# days = re.compile("[가-힣]+").findall(text)
# print(('%s ==> %s')%(text, days))

Location = 'C:/Users/이주찬/Desktop/rmathing/mop_rm/Timetable'
File = 'Excel_Timetable.xls'

data_pd = pd.read_excel('{}/{}'.format(Location, File),
                        header=None, index_col=None, names=None)
data_np = pd.DataFrame.to_numpy(data_pd)
time = []
for i in range(1,len(data_pd)):
    time.append(re.findall("\d+", str(data_pd[11][i])))
for i in range(len(time)):
    time[i] = numpy.array(time[i]).reshape(len(time[i])//4,2,2)
day = []
for i in range(1,len(data_pd)):
    day.append(re.compile("[가-힣]+").findall(str(data_pd[11][i])))
prof = []
for i in range(1,len(data_pd)):
    prof.append(re.compile("[가-힣]+").findall(str(data_pd[8][i])))
sub = []
for i in range(1, len(data_pd)):
    sub.append(data_pd[5][i])
code = []
for i in range(1, len(data_pd)):
    code.append(data_pd[4][i])

print(time[42])
print(day[42])
print(prof[42])
print(sub[42])
print(code[42])
