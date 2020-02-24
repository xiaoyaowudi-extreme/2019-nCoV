import json
from matplotlib import pyplot
import matplotlib.pyplot as plt
import matplotlib
import csv
import os
data_c={}
tmp={}

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']

days=[0,0,31,60,91,121,152,182,213,244,274,305,335,366]
names=["1月25号","1月26号","1月27号","1月28号","1月29号","1月30号","1月31号","2月1号","2月2号","2月3号","2月4号","2月5号","2月6号","2月7号","2月8号",
       "2月9号","2月10号","2月11号","2月12号","2月13号","2月14号","2月15号","2月16号","2月17号","2月18号","2月19号","2月20号","2月21号"]

def extract_day(a):
	return str(days[int(a.split("-")[1])]+int((a.split("-")[2]).split(" ")[0]))

with open("DXYArea.csv",encoding='utf-8') as f:
	f_csv=csv.reader(f)
	f_csv_data=[]
	for row in f_csv:
		f_csv_data.append(row)
	for row in f_csv_data:
		# print(row)
		if row[1]!="provinceEnglishName":
			data_c[row[2]]=[]
			tmp[row[2]]={}
	for row in f_csv_data:
		if row[1]=="provinceEnglishName":
			continue
		# print(extract_day(row[-1]))
		if extract_day(row[-1]) in tmp[row[2]]:
			continue
		data_c[row[2]].append({"number":int(row[6]),"yday":int(extract_day(row[-1]))})
		tmp[row[2]][extract_day(row[-1])]=int(row[6])
	# print(tmp)
	calc_days=["24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39","40","41","42","43","44","45","46","47","48","49","50","51","52"]
	nums1=[0]*(len(calc_days)-1)
	nums2=[0]*(len(calc_days)-1)
	nums3=[0]*(len(calc_days)-1)
	regions=list(data_c.keys())
	for i in regions:
		if not (calc_days[0] in tmp[i]):
			tmp[i][calc_days[0]]=0
			data_c[i].append({"number":0,"yday":int(calc_days[0])})
		for j in range(1,len(calc_days)):
			if calc_days[j] in tmp[i]:
				continue
			tmp[i][calc_days[j]]=tmp[i][calc_days[j-1]]
			data_c[i].append({"number":tmp[i][calc_days[j]],"yday":int(calc_days[j])})
		for j in range(1,len(calc_days)):
			nums1[j-1]+=tmp[i][calc_days[j]]-tmp[i][calc_days[j-1]]
			if i=="420000":
				nums2[j-1]+=tmp[i][calc_days[j]]-tmp[i][calc_days[j-1]]
			else:
				nums3[j-1]+=tmp[i][calc_days[j]]-tmp[i][calc_days[j-1]]
	plt.plot(names, nums1, marker='o', mec='#68838B', mfc='#68838B',c='#68838B',label='全国')
	plt.plot(names, nums2, marker='o', mec='#CD8500', mfc='#CD8500',c='#CD8500',label='湖北')
	plt.plot(names, nums3, marker='o', mec='#4169E1', mfc='#4169E1',c='#4169E1',label='湖北外')
	plt.legend()
	plt.tight_layout()
	plt.title("各地区新增人数对比")
	# plt.show()
	fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(18.5, 10.5)
	plt.savefig(os.path.join(".","nums.jpg"),dpi=300)
