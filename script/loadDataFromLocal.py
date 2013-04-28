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
    history:
        - 13.04.28 22:09:54 Peicheng Liao : ADD partition


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
partitionflag=1


#args (DATAPATH,TABLENAME,FILEDDELIMITETER,LINEDELIMITETER)
def loadDataToHiveTable(*args):
    print args
    DATAPATH=args[0]
    TABLENAME=args[1]
    
    loadCMD="LOAD DATA LOCAL INPATH '"+DATAPATH+"'" 
    loadCMD=loadCMD+' into table '+TABLENAME
    if partitionflag == 1:
        #../script/WEBLOG_1_130426.dat
        DT=DATAPATH.split('/')[-1].split('_')[-1].split('.')[0]
        NO=DATAPATH.split('/')[-1].split('_')[-2]
        loadCMD=loadCMD+'\nPARTITION (dt="'+DT+'",no='+NO+')'
    return loadCMD




if __name__ == "__main__":
    execflag=0
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
