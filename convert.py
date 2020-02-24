import json
import csv
data_c={}
tmp={}

days=[0,0,31,60,91,121,152,182,213,244,274,305,335,366]

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
			if row[5]!="-1.0" and row[5]!="":
				data_c[str(int(float(row[5])))]=[]
				tmp[str(int(float(row[5])))]={}
			tmp[row[2]]={}
	for row in f_csv_data:
		if row[1]=="provinceEnglishName":
			continue
		# print(extract_day(row[-1]))
		if row[5]!="-1.0" and row[5]!="" and (not(extract_day(row[-1]) in tmp[str(int(float(row[5])))])):
			data_c[str(int(float(row[5])))].append({"number":int(row[-5]),"yday":int(extract_day(row[-1]))})
			tmp[str(int(float(row[5])))][extract_day(row[-1])]=int(row[-5])
		if extract_day(row[-1]) in tmp[row[2]]:
			continue
		data_c[row[2]].append({"number":int(row[6]),"yday":int(extract_day(row[-1]))})
		tmp[row[2]][extract_day(row[-1])]=int(row[6])
	# print(tmp)
	calc_days=["24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39","40","41","42","43","44","45","46","47","48","49","50","51","52"]
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
	with open("data-c.json","w") as f0:
		f0.write(json.dumps({"data":data_c}))
