#!/usr/bin/env python
#coding=utf-8
#____________________________________________________________
#
#  Submit Jobs locally
#
# Example:
#
#Matteo Abis
#matteo.abis@cern.ch
#
#based on a script by Yanyan Gao
#
#____________________________________________________________

from __future__ import division, print_function
import sys,os,re,string
import commands
import subprocess
from optparse import OptionParser

#####
release = os.environ["CMSSW_VERSION"]

###############################
####### Main Program
###############################

parser = OptionParser()
parser.add_option("-s", "--dataset", metavar="DATASET", dest="dataset", help="DATASET to look for on DBS")
parser.add_option("-m", "--datamode", metavar="MODE", dest="datamode", help="MODE can be fullsim, fastsim or data")
parser.add_option("-d", "--dir", metavar="DIR", dest="dir", default=".", help="work directory")
parser.add_option("-o", "--ntupledir", metavar="NTUPLEDIR", dest="ntupledir", default="/afs/cern.ch/user/a/abis/scratch0/ntuple", help="ntuple dir")
parser.add_option("-t", "--globaltag", metavar="GTAG", dest="globaltag", help="global tag (looks up the DBS if not specified here)")
parser.add_option("-l", "--lumi", metavar="LUMISECTION", dest="lumi", help="lumisections (optional)")
parser.add_option("-n", "--nevents", metavar="MAXEVENTS",  type="int", dest="nevents", default=50000, help="max number of events to analyze. defaults to 50000")
parser.add_option("-r", "--run", dest="run", metavar="RUNMODE", help="RUNMODE = local or crab. run locally (cmsRun) or on CRAB. Default is None. (only creates cfgfiles)")

options, args = parser.parse_args()

if not(options.dataset and options.datamode):
    print(parser.print_help())
    example = "python PF2Pat_submitJob.py  --dataset /MinimumBias/Run2010A-PromptReco-v4/RECO --datamode 138747 --lumi 138747:1-138747:max --globaltag GR10_P_V7::All --nevents 1000"
    print(example)
    sys.exit()
    
global_tag = ''
if(options.globaltag):
    print('Using globaltag {0} specified by -gtag flag.'.format(options.globaltag))
    global_tag = options.globaltag
else:       
    print( 'Getting global tag from DBS...')
    dbs_result = '';
    command = 'dbsql find config.name,config.content where dataset={0.dataset}>config.content; while read line; do globaltag=`echo $line | sed -n \'s/^.*process.GlobalTag.globaltag = \([^p]*\).*$/\\1/p\'`; if [ "$globaltag" != "" ]; then echo $globaltag; break; fi; done <config.content; rm config.content'.format(options)
    dbsquery = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE);
    dbs_result = dbsquery.communicate()[0]
    dbs_result = re.sub('\n', '', dbs_result)
    global_tag = re.sub('#.+$', '', dbs_result)
    print(global_tag)
    if global_tag == "":
        print('\n GlobalTag is empty from the DBS, please specifiy globalTag manually by -gtag options in the format of(TAG::All) ')
        sys.exit()

dataname = "_".join(options.dataset.split('/')[1:3])
print(dataname)

if options.datamode in ["fullsim", "data", "fastsim"]:
    dbsquery = 'dbs search --noheader --query="find file where dataset={0.dataset}" > tmplist.txt'.format(options)
else:
    dbsquery = 'dbs search --noheader --query="find file where dataset={0.dataset} and run ={0.datamode} > tmplist.txt'.format(options)

print(dbsquery)
try:
    subprocess.check_call(dbsquery, shell=True)
except CalledProcessError:
    print("Execution failed", file=sys.stderr)

lfiles = []
with open("tmplist.txt") as input_file:
    lineList = input_file.readlines()
    nfiles = len(lineList) - 1
    lineList = map(string.strip, lineList)
    prefix = ""

    for n, line in enumerate(lineList):
        if "store" in line:
            if n < nfiles:
                if not n % 256:
                    if not n:
                        lfiles.append("      '" + prefix + line + "',\n")
                    else:
                        lfiles.append("      '" + prefix + line + "' ] ) ;\n")
                        lfiles.append("readFiles.extend( [\n")
                else:
                    lfiles.append("      '" + prefix + line + "',\n")
            else:
                lfiles.append("      '" + prefix + line + "'\n")
                    
dataname = "_".join(options.dataset.split('/')[1:3])

ntupledir = options.ntupledir
cfgdir = os.path.join(options.dir, "cfgfiles")
logdir = os.path.join(options.dir, "log")

try:
    subprocess.check_call("mkdir -p {0} {1} {2}".format(cfgdir, logdir, ntupledir), shell=True)
except subprocess.CalledProcessError:
    print("Execution failed", file=sys.stderr)

if options.datamode == "fullsim":
    cmsswSkelFile = "PF2Pat_template_FullSim_cfg.py"
elif options.datamode == "fastsim":
    cmsswSkelFile = "PF2Pat_template_FastSim_cfg.py"
else:
    cmsswSkelFile = "PF2Pat_template_Data_cfg.py"

if not os.path.exists(cmsswSkelFile):
    print('CMSSW skeleton file does not exist. Exiting')
    sys.exit()
    
cfg_file_name = os.path.join(cfgdir, dataname + "_" + options.datamode + "_cfg.py")
output_root_file_name = "{0}_{1}.root".format(dataname, options.datamode)
output_root_file_name = os.path.join(ntupledir, output_root_file_name)
with open(cmsswSkelFile) as inFile:
    with open(cfg_file_name, 'w') as outFile:
        print('Writing CMS2 CMSSW python config file :', cfg_file_name)

        for template_line in inFile:
            if "INPUTFILES" in template_line:
                for f in lfiles:
                    outFile.write(f);
                continue
            elif "GLOBALTAG" in template_line:
                template_line = 'process.GlobalTag.globaltag = "{0}"\n'.format(global_tag)
            elif "NEVENT" in template_line:
                template_line = 'process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32({0.nevents}))\n'.format(options)
            elif "LUMIRANGE" in template_line:
                if options.lumi: 
                    template_line = 'process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange( \'{0.lumi}\')\n'.format(options) 
                else:
                    template_line = ''
            elif "OUTFILE" in template_line:
                template_line = 'process.out.fileName = cms.untracked.string("{0}")\n'.format(output_root_file_name)
            outFile.write(template_line)        

#create crab configuration file
crab_template_file = "crab_template.cfg"
crab_file_name = "crab_{0}_{1}.cfg".format(dataname, options.datamode)
crab_file_name = os.path.join(cfgdir, crab_file_name)

if not os.path.exists(crab_template_file):
    print('CRAB skeleton file does not exist. Exiting')
    sys.exit()
    
with open(crab_template_file) as inFile:
    print('Writing CRAB config file :', crab_file_name)
    outFile = open(crab_file_name, 'w')

    for template_line in inFile:
        if "DATASET" in template_line:
            template_line = "datasetpath = {0}\n".format(options.dataset)
        if "CFGFILE" in template_line:
            template_line = "pset = {0}\n".format(cfg_file_name)
        if "NEVENT" in template_line:
           template_line = "total_number_of_events = {0}\n".format(options.nevents)
        if "NJOBS" in template_line:
            template_line = "number_of_jobs = {0}\n".format(options.nevents // 50000)
        outFile.write(template_line)        
    outFile.close()

#compile
try:
    subprocess.check_call("cd $CMSSW_BASE/src/ ; scram b ;", shell=True)
except subprocess.CalledProcessError:
    print("Execution failed", file=sys.stderr)

log_file_name = dataname+"_"+options.datamode+"_.log"
log_file_name = os.path.join(logdir, log_file_name)

#run either on lxplus or on CRAB

if(options.run) == "local":
    try:
        runjobcmd = "cmsRun {0} >& {1} &".format(cfg_file_name, log_file_name)
        print(runjobcmd)
        subprocess.check_call(runjobcmd, shell=True)
    except subprocess.CalledProcessError:
        print("Execution failed", file=sys.stderr)

if(options.run) == "crab":
    try:
        runjobcmd = "crab -cfg {0} -create -submit".format(crab_file_name)
        print(runjobcmd)
        subprocess.check_call(runjobcmd, shell=True)
    except subprocess.CalledProcessError:
        print("Execution failed", file=sys.stderr)
