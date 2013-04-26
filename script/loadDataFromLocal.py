#coding=utf-8
"""
	13.04.26 19:10:15 Peicheng Liao <peicheng5 (a) gmail.com>
	=========================
	goal:
		Load data from local fs to hive table
	usage:
		python loadDataFromLocal.py [DATAPATH]

	hivecmd:
		 load data local inpath '' into table WEBLOG partition (dt='20130426',logm='1');

"""
import sys,os
from hivelib import colorprint,getDDLlist,execHivecmd
if len(sys.argv)<2:
    print '''Goal: given DATEFILE put to hive table
Usage:
	python loadDataFromLocal.py [DATFILE]
	ex:
	python loadDataFromLocal.py [DATFILE]
'''
    exit()
#WEBLOG_1_130426.dat

#args (DATAPATH,TABLENAME,FILEDDELIMITETER,LINEDELIMITETER)
def loadDataToHiveTable(*args):
	print args
	DATAPATH=args[0]
	TABLENAME=args[1]
	loadCMD="LOAD DATA LOCAL INPATH '"+DATAPATH+"'" 
	loadCMD=loadCMD+' into table '+TABLENAME
	return loadCMD




if __name__ == "__main__":

	execflag=1
	argvlist=sys.argv[1].split('/')[-1].split('_')
	print argvlist
	TABLE_NEME=argvlist[0].split('.')[0]
	TABLE_DATE=argvlist[2].split('.')[0]
	print TABLE_NEME,TABLE_DATE
	print 'lol'
	print TABLE_NEME,TABLE_DATE
	print loadDataToHiveTable(sys.argv[1],TABLE_NEME)
	
	if execflag == 1:
		execHivecmd(loadDataToHiveTable(sys.argv[1],TABLE_NEME))
