#coding=utf-8
"""
	13.04.26 17:47:03 Peicheng Liao <peicheng5 (a) gmail.com>
	=========================
	Goal: given RDB DDL to gen hive table 
	Usage:
		python createHiveTableFromDDL.py [ddlfile]
		ex:
		python createHiveTableFromDDL.py ../DDL/WEBLOG.ddl
	History:
	
"""
import sys,os
if len(sys.argv)<2:
    print '''Goal: given RDB DDL to gen hive table 
Usage:
	python createHiveTableFromDDL.py [ddlfile]
	ex:
	python createHiveTableFromDDL.py ../DDL/WEBLOG.ddl
	python createHiveTableFromDDL.py ../DDL/WEBLOG_130426.ddl

'''
    exit()
"""
	FLAG DEFINE
"""
#if exec cmd set 1,not set 0 for debug and show cmd
hiveexec=0

"""
	DEF
	====
"""

"""
print color
input: str
"""
def colorprint(strp):
        print '\033[1;33m'+strp+'\033[0m'

"""
	getDDLlist
	goal:
	parse DDLFILE return FIELD NAME LIST
	input: DDLNAME
	output:ddlist
"""
def getDDLlist(DDLNAME):
    NEWDDLFILE=open(DDLNAME)
    NEWDDLFILE=NEWDDLFILE.read()
    NEWDDLFILE=NEWDDLFILE[NEWDDLFILE.find('(')+1:NEWDDLFILE.rfind(')')]
    #print NEWDDLFILE
    NEWDDLLIST=[]
    for l in NEWDDLFILE.split('\n'):
        #print l.spilt('')
        ddllist=l.split()
        if len(ddllist)>0:
            #print ddllist
            NEWDDLLIST.append(ddllist[0])
    return NEWDDLLIST

"""
	parse DDL from RDB
"""
DDLINPUTNAME=sys.argv[1]
HIVETABLENAME=DDLINPUTNAME.split('/')[-1]
#print HIVETABLENAME
CREATECMD="CREATE TABLE "+HIVETABLENAME+" ("
for l in NEWDDLLIST[:-1]:
    #CM_TX_DT                timestamp          
    if 'DT' in l:
        CREATECMD=CREATECMD+'\n'+l+" timestamp,"
    else:
        CREATECMD=CREATECMD+'\n'+l+" STRING,"

if 'DT' in l:
    CREATECMD=CREATECMD+"\n"+NEWDDLLIST[-1]+" TIMESTAMP)"
else:
    CREATECMD=CREATECMD+"\n"+NEWDDLLIST[-1]+" STRING)"

if __name__ == "__main__":
	print 'lol'
	colorprint('Test getDDLlist')
	print getDDLlist(sys.argv[1])
