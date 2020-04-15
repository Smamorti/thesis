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
#runCommandAsJob('python testJob.py' , 'submision.sh') 
# workingPoint = 0.863306
#runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_fullData.bin -w {} -x yes'.format(workingPoint), 'lepPlots_{}.sh'.format(workingPoint))
# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_Best_FullData_18epochs.h5 -w {} -x yes'.format(workingPoint), 'lepPlots_NN_{}.sh'.format(workingPoint))

#runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -w {} -x yes'.format(sys.argv[1], sys.argv[2]), 'lepPlots_{}.sh'.format(sys.argv[2]))

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_602020_run2.h5 -x yes', 'lepPlots_noMLcut_NN.sh')
# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_Best_FullData_18epochs.h5 -x yes', 'lepPlots_noMLcut_NN.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_fullData.bin -x yes -p samples/2018_total_BDT.plot -w noWorkingPointv2', 'lepPlots_noMLcut_BDT.sh')

# runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/NN_final_80_0_20_18epochs.h5 -x yes -w noWorkingPointv3_finerMObins -c samples/2018_total_v3.conf -p samples/2018_total_finerBins.plot', 'lepPlots_NN_8020_v3.sh')

runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20.bin -x yes -p samples/2018_total_BDT.plot -w noWorkingPointv2', 'lepPlots_BDT_v2.sh')

runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20.bin -x yes -p samples/2018_total_BDT.plot -w noWorkingPointv3 -c samples/2018_total_v3.conf', 'lepPlots_BDT_v3.sh')                      
