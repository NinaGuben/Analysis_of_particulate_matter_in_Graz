import requests
import xlrd
import matplotlib
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime

# get data from website and continue if request succeeds (2xx)

url = "https://www.umwelt.steiermark.at/luft2/export.php?mittelwert=21&von_tag=7&von_monat=8&von_jahr=2020&station1=171&mw_typ=21&komponente1=114"

r = requests.get(url)
r.raise_for_status()

#print(r.content)

# parse as excel file using latin1 as text encoding, use first sheet (=0)
# check out https://xlrd.readthedocs.io/en/latest/api.html

wb = xlrd.open_workbook(file_contents=r.content, encoding_override='latin1')
print(wb)

sheet = wb.sheet_by_index(0)

# prints 6th row
#for cell in sheet.row(5):
#    print (cell.value)

#prints third column
#x = sheet.col(2)
#print(x)

#print(x[5:])

# print third column sixth row, produce list of floats 

values=sheet.col_values(2,5)
# print(y)

date_strings = sheet.col_values(0,5)
# print(x)

time_strings = sheet.col_values(1,5)

dates = []
for date, time in zip(date_strings,time_strings):
    date_time_str = date + " " + time
    date_time_obj = datetime.datetime.strptime(date_time_str, '%d.%m.%y %H:%M')
    dates.append(date_time_obj)

print(values, dates)


# Data for plotting

fig, ax = plt.subplots()
ax.plot(dates, values)

ax.set(xlabel='Datum', ylabel='Feinstaubkonzentration [µg/m³]',
       title='Feinstaubkonzentration Graz Ost Petersgasse')
ax.grid()
fig.autofmt_xdate()
plt.axhline(y=50.0, linewidth=4, color='r')
ax.set_ylim(ymin=0)
ax.set_ylim(ymax=240)


fig.savefig("test.png")
plt.show()
