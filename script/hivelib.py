#coding=utf-8
import os,sys
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
def execHivecmd(cmd):
        execuser='sudo -u hdfs hive -e "'
        cmd=execuser+cmd+' ;"'
        print os.popen(cmd).read()
