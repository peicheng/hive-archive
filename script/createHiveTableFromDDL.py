#coding=utf-8
"""
	13.04.26 17:47:03 Peicheng Liao <peicheng5 (a) gmail.com>
	=========================
	Goal: given RDB DDL to gen hive table 
	Usage:
		python createHiveTableFromDDL.py [ddlfile] [[FIELDDELIMITER]] [[LINEDELIMITER]]
		ex:
		python createHiveTableFromDDL.py ../DDL/WEBLOG.ddl
		python createHiveTableFromDDL.py ../DDL/WEBLOG.ddl '\t'
		python createHiveTableFromDDL.py ../DDL/WEBLOG.ddl '\t'	'\n'
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
hiveexecflag=1

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

#print HIVETABLENAME
#def createHiveTableCMD(HIVETABLENAME,NEWDDLLIST,FIELDDELIMITER):
def createHiveTableCMD(*args,**kwargs):
	'''
	argslist=['HIVETABLENAME','NEWDDLLIST','FIELDDELIMITER']
	'''
	HIVETABLENAME=args[0]
	NEWDDLLIST=args[1]
	#print len(args),args
	CREATECMD="CREATE TABLE IF NOT EXISTS "+HIVETABLENAME+" ("
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
	
	if len(args)>2:
		FIELDDELIMITER=args[2]
		CREATECMD=CREATECMD+"\nROW FORMAT DELIMITED\nFIELDS TERMINATED BY '"+FIELDDELIMITER+"'"
	if len(args)>3:
		LINEDELIMITER=args[3]
		CREATECMD=CREATECMD+"\nLINES TERMINATED BY '"+LINEDELIMITER+"'"
	return CREATECMD
"""
	execHivecmd
"""
def execHivecmd(cmd):
        execuser='sudo -u hdfs hive -e "'
        cmd=execuser+cmd+' ;"'
        print os.popen(cmd).read()

if __name__ == "__main__":
	print 'lol'
	colorprint('Test getDDLlist')
	NEWDDLLIST=getDDLlist(sys.argv[1])
	print NEWDDLLIST
	DDLINPUTNAME=sys.argv[1]
	#WEBLOG_130426
	#HIVETABLENAME=DDLINPUTNAME.split('/')[-1].split('.')[0]
	#WEBLOG
	HIVETABLENAME=DDLINPUTNAME.split('/')[-1].split('_')[0]
	
	"""
	if len(sys.argv)>2:
		print createHiveTableCMD(HIVETABLENAME,NEWDDLLIST,sys.argv[2])
	else:
		print createHiveTableCMD(HIVETABLENAME,NEWDDLLIST)
	if len(sys.argv)>3:
		print createHiveTableCMD(HIVETABLENAME,NEWDDLLIST,sys.argv[2],sys.argv[3])
	"""
	print createHiveTableCMD(HIVETABLENAME,NEWDDLLIST,*sys.argv[2:])
	#print createHiveTableCMD(*sys.argv[0:])
	
	if hiveexecflag == 1:
		colorprint('=====execHiveCmd=====')
		execHivecmd(createHiveTableCMD(HIVETABLENAME,NEWDDLLIST,*sys.argv[2:]))
