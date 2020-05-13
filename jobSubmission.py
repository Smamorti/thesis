#include python library classes
import subprocess
import time
import os
from pathlib import Path
import sys

#submit script of given name as a job with given wall-time ( Copied from my DeepLearning repository, consider making a submodule for jobsubmission )
def submitQsubJob( script_name, wall_time = '24:00:00', num_threads = 1, high_memory = False):

    #keep attempting submission until it succeeds
    submission_command = 'qsub {} -l walltime={}'.format( script_name, wall_time )

    if num_threads > 1:
        submission_command += ' -lnodes=1:ppn={}'.format(num_threads)

    if high_memory :
        submission_command += ' -q highmem'

    while True:
        try:
            qsub_output = subprocess.check_output( submission_command, shell=True, stderr=subprocess.STDOUT )

        #submission failed, try again after one second 
        except subprocess.CalledProcessError as error:
            print('Caught error : "{}".\t Attempting resubmission.'.format( error.output.decode().split('\n')[0] ) )
            time.sleep( 1 )

        #submission succeeded 
        else:
            first_line = qsub_output.decode().split('\n')[0]
            print( first_line )

            #break loop by returning job id when submission was successful 
            return first_line.split('.')[0]


def initializeJobScript( script, cmssw_version = 'CMSSW_10_2_17' ):

   	#TO DO : make code to extract CMSSW directory in a general way
    #this is already available in DeepLearning repository, submodule would be a good solution 
    script.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
    script.write('cd {}/src\n'.format( cmssw_version ) )
    script.write('eval `scram runtime -sh`\n')
    working_directory = os.path.abspath( os.getcwd() )
    script.write('cd {}\n'.format( working_directory ) )



def runCommandAsJob( command, script_name, wall_time = '24:00:00', num_threads = 1, high_memory = False, cmssw_version = 'CMSSW_10_2_17' ):
    with open( script_name, 'w' ) as script:
        initializeJobScript( script, cmssw_version )
        script.write( command + '\n' )
    submitQsubJob( script_name, wall_time, num_threads, high_memory )

NNmodels = ['NN_final_8020_8epochs.h5']

#NNmodels = ['NN_gen39_1_80_0_20_19epochs.h5']
#NNmodel = "NN_final_80_0_20_18epochs_v3.h5"
######
# NN #
######

#NNmodels = ['NN_1_8020_24epochs.h5', 'NN_2_8020_12epochs.h5','NN_2_8020_14epochs.h5','NN_3_8020_5epochs.h5','NN_3_8020_6epochs.h5','NN_5_8020_12epochs.h5', 'NN_2_8020_10epochs.h5']


for NNmodel in NNmodels:

    # ----------------nominal----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -w nominal '.format(NNmodel), 'NN_nominal.sh')

    # ----------------JEC----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC up -b central  -w JECup '.format(NNmodel), 'NN_JECup.sh')

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC down -b central  -w JECdown '.format(NNmodel), 'NN_JECdown.sh')

    # ----------------pileup----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_up_total.root --JEC nominal -b central  -w pileupUp '.format(NNmodel), 'NN_pileupUp.sh')

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_down_total.root --JEC nominal -b central  -w pileupDown '.format(NNmodel), 'NN_pileupDown.sh')

    # ----------------btag----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b up  -w btagUp '.format(NNmodel), 'NN_btagUp.sh')

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b down  -w btagDown '.format(NNmodel), 'NN_btagDown.sh')


# for NNmodel in NNmodels:

#     # ----------------nominal----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -w MVAcut_nominal --useMVAcut 0.7'.format(NNmodel), 'NN_nominal.sh')

#     # ----------------JEC----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC up -b central  -w MVAcut_JECup --useMVAcut 0.7'.format(NNmodel), 'NN_JECup.sh')

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC down -b central  -w MVAcut_JECdown --useMVAcut 0.7'.format(NNmodel), 'NN_JECdown.sh')

#     # ----------------pileup----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_up_total.root --JEC nominal -b central  -w MVAcut_pileupUp --useMVAcut 0.7'.format(NNmodel), 'NN_pileupUp.sh')

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_down_total.root --JEC nominal -b central  -w MVAcut_pileupDown --useMVAcut 0.7'.format(NNmodel), 'NN_pileupDown.sh')

#     # ----------------btag----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b up  -w MVAcut_btagUp --useMVAcut 0.7'.format(NNmodel), 'NN_btagUp.sh')

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b down  -w MVAcut_btagDown --useMVAcut 0.7'.format(NNmodel), 'NN_btagDown.sh')


#######
# BDT #
#######

# # ----------------nominal----------------

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -w MVAcut_nominal --useMVAcut 0.7', 'BDT_nominal.sh')

# # ----------------JEC----------------

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC up -b central  -w MVAcut_JECup --useMVAcut 0.7', 'BDT_JECup.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC down -b central  -w MVAcut_JECdown --useMVAcut 0.7', 'BDT_JECdown.sh')

# # ----------------pileup----------------

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_up_total.root --JEC nominal -b central  -w MVAcut_pileupUp --useMVAcut 0.7', 'BDT_pileupUp.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_down_total.root --JEC nominal -b central  -w MVAcut_pileupDown --useMVAcut 0.7', 'BDT_pileupDown.sh')

# # ----------------btag----------------

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b up  -w MVAcut_btagUp --useMVAcut 0.7', 'BDT_btagUp.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b down  -w MVAcut_btagDown --useMVAcut 0.7', 'BDT_btagDown.sh')


# runCommandAsJob('python makeTreeML.py -c samples/background_2018_v3.conf -s background_2018', 'bkg.sh')
# runCommandAsJob('python makeTreeML.py', 'signal.sh')

