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
		data_main[count,0]=string.atof(cell[1])
		data_main[count,1]=string.atof(cell[2])
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
def ctl_create(input_file_path):
	flag_input_file_path=open(input_file_path,"w")
	flag_input_file_path.write("DSET /media/qzhang/UUI/20110718/11071800.dat\n")
	flag_input_file_path.write("DTYPE station\n")
	flag_input_file_path.write("STNMAP /media/qzhang/UUI/20110718/11071800.map\n")
	flag_input_file_path.write("UNDEF 9999.00000\n")
	flag_input_file_path.write("TITLE Station Data\n")
	flag_input_file_path.write("TDEF 1 linear 00z18jul2011 1hr\n")
	flag_input_file_path.write("VARS 7\n")
	flag_input_file_path.write("hgt 0 99 heigt\n")
	flag_input_file_path.write("wnddir 0 99 wind direction\n")
	flag_input_file_path.write("wndspd 0 99 wind speed\n")
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
station_num,data,record=AWS_extract("/media/qzhang/UUI/20110718/11071800.AWS")
rslt=grads_compile(station_num,data,record)
grads_save(rslt,"/media/qzhang/UUI/20110718/11071800.dat")
ctl_create("/media/qzhang/UUI/20110718/11071800.ctl")
