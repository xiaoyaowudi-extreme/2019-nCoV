import json
from matplotlib import pyplot
import matplotlib.pyplot as plt
import matplotlib
import csv
import os
data_c={}

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

names=["1月25号","1月26号","1月27号","1月28号","1月29号","1月30号","1月31号","2月1号","2月2号","2月3号","2月4号","2月5号","2月6号","2月7号","2月8号",
       "2月9号","2月10号","2月11号","2月12号"]

days=[0,0,31,60,91,121,152,182,213,244,274,305,335,366]

from scipy import log as log
import numpy as np
from scipy import exp
from scipy.optimize import curve_fit

def func(x, a,b):
    y = a * log(x) + b
    return y

def polyfit(x, y):
    popt, pcov = curve_fit(func, x, y)

    return popt

def extract_day(a):
	return str(days[int(a.split("-")[1])]+int((a.split("-")[2]).split(" ")[0]))

with open("DXYArea.csv",encoding='utf-8') as f:
	f_csv=csv.reader(f)
	f_csv_data=[]
	for row in f_csv:
		if row[1]!="provinceEnglishName" and row[5]!="-1.0" and row[5]!="":
			if str(int(float(row[5])))=="420100":
				f_csv_data.append(row)
	print(f_csv_data)
	for row in f_csv_data:
		# print(extract_day(row[-1]))
		if extract_day(row[-1]) in data_c:
			continue
		data_c[extract_day(row[-1])]=int(row[-5])
	# print(tmp)
	calc_days=["24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39","40","41","42","43","44","45","46","47","48","49","50","51","52"]
	nums1=[0]*(len(calc_days)-9) # I
	nums2=[0]*(len(calc_days)-9) # E
	nums3=[0]*(len(calc_days)-10)
	for i in range(len(calc_days)-9):
		for j in range(1,4):
			nums1[i]+=data_c[calc_days[i+j]]
		for j in range(1,10):
			nums2[i]+=data_c[calc_days[i+j]]
		if i>0:
			nums3[i-1]=(nums2[i]-nums2[i-1])/(nums1[i]+0.1*nums2[i])
	plt.plot(names, nums3, marker='o', mec='#4169E1', mfc='#4169E1',c='#4169E1',label='传染率')
	plt.legend()
	plt.tight_layout()
	# plt.title("武汉传染率")
	# plt.show()
	# fig = matplotlib.pyplot.gcf()
	# fig.set_size_inches(18.5, 10.5)
	# plt.savefig(os.path.join(".","nums.jpg"),dpi=300)
	# plt.clf()
	x,y=list(range(1,len(calc_days)-10)),nums3[1:]
	popt=polyfit(x,y)
	samples=np.linspace(1,len(calc_days)-11,200)
	plt.plot(samples,func(samples,popt[0],popt[1]),c='#CD8500',label='传染率拟合曲线')
	plt.legend()
	plt.title("武汉传染率")
	fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(18.5, 10.5)
	plt.savefig(os.path.join(".","nums2.jpg"),dpi=300)
