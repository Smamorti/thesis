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

#runCommandAsJob('./main data/samples/samples_ttZ_npDD.txt runFullSelection selection:ttZ ', 'submision.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs.h5 -x yes -w noWorkingPointv2_finerBins -c samples/2018_total.conf -p samples/2018_total_finerBins.plot', 'lepPlots_NN_8020_fine.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs.h5 -x yes -w noWorkingPointv2 -c samples/2018_total.conf -p samples/2018_total.plot', 'lepPlots_NN_8020.sh')


# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w noWorkingPointv3_finerBins -c samples/2018_total_v3.conf -p samples/2018_total_finerBins.plot', 'lepPlots_NN_8020_fine_v3.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w noWorkingPointv3 -c samples/2018_total_v3.conf -p samples/2018_total.plot', 'lepPlots_NN_8020_v3.sh')




# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -x yes -w noWorkingPointv3_finerBins -c samples/2018_total_v3.conf -p samples/2018_total_BDT_finerBins.plot', 'lepPlots_BDT_v3_fine.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -x yes -p samples/2018_total_BDT.plot -w noWorkingPointv3 -c samples/2018_total_v3.conf', 'lepPlots_BDT_v3.sh')                      


# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20.bin -x yes -w noWorkingPointv2_finerBins -c samples/2018_total.conf -p samples/2018_total_BDT_finerBins.plot', 'lepPlots_BDT_v2_fine.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20.bin -x yes -p samples/2018_total_BDT.plot -w noWorkingPointv2 -c samples/2018_total.conf', 'lepPlots_BDT_v2.sh')                      


# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w normal -c samples/2018_total_v3.conf -p samples/2018_total.plot', 'lepPlots_NN_8020_v3.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w normal_fitWeights -f samples/NN.fit', 'lepPlots_NN_8020_v3.sh') 

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -x yes -p samples/2018_total_BDT.plot -w normal_fitWeights -c samples/2018_total_v3.conf -f samples/BDT.fit', 'lepPlots_BDT_v3.sh')   

# -------------------Pileup-----------------

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w pileupDown --pileupFile weights/pileup/pileup_down_total.root', 'NN_PDown.sh')
# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w pileupUp --pileupFile weights/pileup/pileup_up_total.root', 'NN_PUp.sh')
# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w pileupNominal --pileupFile weights/pileup/pileup_nominal_total.root', 'NN_PNominal.sh')
# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w noPileUp --pileupFile weights/pileup/noPileup.root', 'NN_noPileup.sh')


# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -x yes -w pileupDown --pileupFile weights/pileup/pileup_down_total.root -p samples/2018_total_BDT.plot', 'BDT_PDown.sh')
# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -x yes -w pileupUp --pileupFile weights/pileup/pileup_up_total.root -p samples/2018_total_BDT.plot', 'BDT_PUp.sh')
# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -x yes -w pileupNominal --pileupFile weights/pileup/pileup_nominal_total.root -p samples/2018_total_BDT.plot', 'BDT_PNominal.sh')
# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -x yes -w noPileup --pileupFile weights/pileup/noPileup.root -p samples/2018_total_BDT.plot', 'BDT_noPileUp.sh')



# ----------------JEC----------------

runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w pileupNominal_JECup --pileupFile weights/pileup/pileup_nominal_total.root --JEC up', 'NN_PNominal_JECup.sh')
runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w noPileUp_JECup --pileupFile weights/pileup/noPileup.root --JEC up', 'NN_noPileup_JECup.sh')

runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w pileupNominal_JECdown --pileupFile weights/pileup/pileup_nominal_total.root --JEC down', 'NN_PNominal_JECdown.sh')
runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w noPileUp_JECdown --pileupFile weights/pileup/noPileup.root --JEC down', 'NN_noPileup_JECdown.sh')

runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w pileupNominal_JECnominal --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal', 'NN_PNominal_jecnom.sh')
runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w noPileUp_JECnominal --pileupFile weights/pileup/noPileup.root --JEC nominal', 'NN_noPileup_JECnom.sh')



runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes -w pileupNominal_JECup --pileupFile weights/pileup/pileup_nominal_total.root --JEC up', 'BDT_PNominal_JECup.sh')
runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes -w noPileUp_JECup --pileupFile weights/pileup/noPileup.root --JEC up', 'BDT_noPileup_JECup.sh')

runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes -w pileupNominal_JECdown --pileupFile weights/pileup/pileup_nominal_total.root --JEC down', 'BDT_PNominal_JECdown.sh')
runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes -w noPileUp_JECdown --pileupFile weights/pileup/noPileup.root --JEC down', 'BDT_noPileup_JECdown.sh')

runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes -w pileupNominal_JECnominal --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal', 'BDT_PNominal_jecnom.sh')
runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes -w noPileUp_JECnominal --pileupFile weights/pileup/noPileup.root --JEC nominal', 'BDT_noPileup_JECnom.sh')



