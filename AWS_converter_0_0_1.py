# -*- coding: utf-8 -*-

"""
read CMA AWS data
@author: qzhang
"""

import numpy as np
import string
from array import array

# read data
def AWS_extract(input_file_path):
	aws_flag=open(input_file_path,"r")
	data_raw=aws_flag.read().split("\n")
	file_record=data_raw[1].split(" ")
	data_main_str=[]
	data_main_str=[cell.split(" ") for cell in data_raw[2:]][:-1]
	data_main=np.empty([int(string.atof(file_record[-1])),9])
	station_num=[]
	count=0
	for cell in data_main_str:
		station_num=station_num+["%8d" % string.atof(cell[0])]
		data_main[count,0]=string.atof(cell[2])
		data_main[count,1]=string.atof(cell[1])
		data_main[count,2]=string.atof(cell[3])
		data_main[count,3]=string.atof(cell[6])
		data_main[count,4]=string.atof(cell[7])
		data_main[count,5]=string.atof(cell[8])
		data_main[count,6]=string.atof(cell[12])
		data_main[count,7]=string.atof(cell[16])
		data_main[count,8]=string.atof(cell[19])
		count+=1
	aws_flag.close()
	return station_num,data_main,string.atof(file_record[-1])

"""
data_main type:	[:,0]:lat
									[:,1]:lon
									[:,2]:height
									[:,3]:wind direction
									[:,4]:wind speed
									[:,5]:pressure
									[:,6]:precipitation
									[:,7]:td
									[:,8]:temperature
string.atof(file_record[-1]): 	AWS record number
"""

# write as grads readable
def grads_compile(input_station_num,input_data,record_num):
	count=0
	record=[]
	while count<=int(record_num)-1:
		stid=input_station_num[count]
		lat=float(input_data[count,0])
		lon=float(input_data[count,1])
		t=0.0
		if count==int(record_num)-1:
			nlev=0
		else:
			nlev=1
		flag=1
		record=record+[[stid,lat,lon,t,nlev,flag,float(input_data[count,2]),float(input_data[count,3]),\
										float(input_data[count,4]),float(input_data[count,5]),float(input_data[count,6]),\
										float(input_data[count,7]),float(input_data[count,8])]]
		count+=1
	return record

# save data
def grads_save(data_to_write,output_file_path):
	flag_output_file_path=open(output_file_path,"wb")
	for cell in data_to_write:
		#save station id
		float_array = array('c', cell[0])
		float_array.tofile(flag_output_file_path)
		#save lat lon time
		float_array = array('f', cell[1:4])
		float_array.tofile(flag_output_file_path)
		#save flags
		float_array = array('i', cell[4:6])
		float_array.tofile(flag_output_file_path)
		#save variables
		float_array = array('f', cell[6:13])
		float_array.tofile(flag_output_file_path)
	flag_output_file_path.close()
	return flag_output_file_path

#create ctl file
def ctl_create(input_file_path,date_tm):
	flag_input_file_path=open(input_file_path,"w")
	flag_input_file_path.write("DSET /home/qzhang/2011_07_18/AWS/"+date_tm+".dat\n")
	flag_input_file_path.write("DTYPE station\n")
	flag_input_file_path.write("STNMAP /home/qzhang/2011_07_18/AWS/"+date_tm+".map\n")
	flag_input_file_path.write("UNDEF 9999.00000\n")
	flag_input_file_path.write("TITLE Station Data\n")
	if string.atof(date_tm[2:4])==1.0:
		mnth="Jan"
	if string.atof(date_tm[2:4])==2.0:
		mnth="Feb"
	if string.atof(date_tm[2:4])==3.0:
		mnth="Mar"
	if string.atof(date_tm[2:4])==4.0:
		mnth="Apr"
	if string.atof(date_tm[2:4])==5.0:
		mnth="May"
	if string.atof(date_tm[2:4])==6.0:
		mnth="Jun"
	if string.atof(date_tm[2:4])==7.0:
		mnth="Jul"
	if string.atof(date_tm[2:4])==8.0:
		mnth="Aug"
	if string.atof(date_tm[2:4])==9.0:
		mnth="Sep"
	if string.atof(date_tm[2:4])==10.0:
		mnth="Oct"
	if string.atof(date_tm[2:4])==11.0:
		mnth="Nov"
	if string.atof(date_tm[2:4])==12.0:
		mnth="Dec"
	flag_input_file_path.write("TDEF 1 linear "+date_tm[6:8]+"z"+date_tm[4:6]+mnth+"20"+date_tm[0:2]+" 1hr\n")
	flag_input_file_path.write("VARS 7\n")
	flag_input_file_path.write("hgt 0 99 heigt\n")
	flag_input_file_path.write("uwnd 0 99 wind direction\n")
	flag_input_file_path.write("vwnd 0 99 wind speed\n")
	flag_input_file_path.write("pres 0 99 pressure\n")
	flag_input_file_path.write("rain 0 99 rain\n")
	flag_input_file_path.write("td 0 99 dew point temprature\n")
	flag_input_file_path.write("t 0 99 temperature\n")
	flag_input_file_path.write("ENDVARS\n")
	flag_input_file_path.close()
	return flag_input_file_path

"""
test!test!
"""
count=0
while count<24:
	cvt_flie_path="/media/qzhang/240E5CF90E5CC608/2011_07_18/AWS/110718"
	if count<10:
		cvt_full_path=cvt_flie_path+"0"+str(int(string.atof(count)))
	else:
		cvt_full_path=cvt_flie_path+str(int(string.atof(count)))
	station_num,data,record=AWS_extract(cvt_full_path+".AWS")
	#calculate U conponent wind and V conponent Wind
	for cell in data:
		if cell[3]==9999.0 or cell[4]==9999.0:
			uwnd=9999.0
			vwnd=9999.0
		else:
			if cell[3]<=90:
				uwnd=-cell[4]*np.sin(cell[3]*np.pi/180)
				vwnd=-cell[4]*np.cos(cell[3]*np.pi/180)
			if cell[3]>90 and cell[3]<=180:
				uwnd=-cell[4]*np.sin((180-cell[3])*np.pi/180)
				vwnd=cell[4]*np.cos((180-cell[3])*np.pi/180)
			if cell[3]>180 and cell[3]<=270:
				uwnd=cell[4]*np.sin((cell[3]-180)*np.pi/180)
				vwnd=cell[4]*np.cos((cell[3]-180)*np.pi/180)
			if cell[3]>270 and cell[3]<=360:
				uwnd=cell[4]*np.sin((360-cell[3])*np.pi/180)
				vwnd=-cell[4]*np.cos((360-cell[3])*np.pi/180)
			cell[3]=uwnd
			cell[4]=vwnd
	rslt=grads_compile(station_num,data,record)
	grads_save(rslt,cvt_full_path+".dat")
	ctl_create(cvt_full_path+".ctl",cvt_full_path[46:])
	print cvt_full_path
	count+=1

