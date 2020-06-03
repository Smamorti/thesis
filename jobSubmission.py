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

# NNmodels = ['NN_1_8020_24epochs.h5', 'NN_2_8020_12epochs.h5','NN_2_8020_14epochs.h5','NN_3_8020_5epochs.h5','NN_3_8020_6epochs.h5','NN_5_8020_12epochs.h5', 'NN_2_8020_10epochs.h5']

# NNmodels = ['NN_2_8020_10epochs.h5']

# NNmodels = ['NN_2_8020_8epochs.h5', 'NN_4_8020_6epochs.h5','NN_6_8020_7epochs.h5','NN_6_8020_8epochs.h5']

# NNmodels = ['NN_2_50_10epochs.h5', 'NN_2_50_8epochs.h5', 'NN_4_50_6epochs.h5', 'NN_6_50_7epochs.h5', 'NN_6_50_8epochs.h5']


NNmodels = ['NN_2_50_10epochs.h5', 'NN_2_50_8epochs.h5', 'NN_2_8020_8epochs.h5', 'NN_3_8020_23epochs.h5', 'NN_4_50_6epochs.h5', 'NN_4_8020_6epochs.h5', 'NN_6_50_7epochs.h5', 'NN_6_50_8epochs.h5', 'NN_6_8020_7epochs.h5','NN_6_8020_8epochs.h5']


# for y in [120, 122, 123, 133, 143, 171, 328, 365, 467, 475]:

#     runCommandAsJob('python makeShape.py -x BDT_GS_{} -a BDT'.format(y), '{}.sh'.format(y))
#     runCommandAsJob('python makeShape.py -x BDT_GS_{}_8020 -a BDT'.format(y), '{}_8020.sh'.format(y))


    # for x in ['JECdown', 'JECup']:#, 'nominal', 'pileupDown', 'pileupUp', 'btagDown', 'btagUp']:

    #     runCommandAsJob('python pklPlot.py -f histograms/BDT_GS_{}/{}/histList_2018_total.pkl -d histograms/BDT_GS_{}/{}/histList_2018_total_data.pkl'.format(y, x, y, x), '{}_{}.sh'.format(y, x))
    #     runCommandAsJob('python pklPlot.py -f histograms/BDT_GS_{}_8020/{}/histList_2018_total.pkl -d histograms/BDT_GS_{}_8020/{}/histList_2018_total_data.pkl'.format(y, x, y, x), '{}_{}_8020.sh'.format(y, x))


NNmodels = ['NN_3_8020_23epochs.h5']
# NNmodels = ['NN_3_8020_mll_23epochs.h5']

# NNmodels = ['NN_3_8020_mll_23epochs.h5']

for NNmodel in NNmodels:

    #----------------nominal----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot --DY 1.10 -w DYUp1.10'.format(NNmodel), 'NN_DYUp_{}.sh'.format(NNmodel))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot --DY 1.05 -w DYUp1.05'.format(NNmodel), 'NN_DYUp_{}.sh'.format(NNmodel))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot --DY 0.9 -w DYDown0.9'.format(NNmodel), 'NN_DYDown_{}.sh'.format(NNmodel))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot --DY 0.95 -w DYDown0.95'.format(NNmodel), 'NN_DYDown_{}.sh'.format(NNmodel))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot --QCD up -w moreMObins_QCDUp'.format(NNmodel), 'NN_QCDUp_{}.sh'.format(NNmodel))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot --QCD down -w moreMObins_QCDDown'.format(NNmodel), 'NN_QCDdown_{}.sh'.format(NNmodel))




for NNmodel in NNmodels:

    # ----------------nominal----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot -w moreMObins_nominal '.format(NNmodel), 'NN_nominal_{}.sh'.format(NNmodel))

    # ----------------JEC----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC up -b central  -p samples/2018_total_Alot.plot -w moreMObins_JECUp '.format(NNmodel), 'NN_JECup_{}.sh'.format(NNmodel))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC down -b central  -p samples/2018_total_Alot.plot -w moreMObins_JECDown '.format(NNmodel), 'NN_JECdown_{}.sh'.format(NNmodel))

    # ----------------pileup----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_up_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot -w moreMObins_pileupUp '.format(NNmodel), 'NN_pileupUp_{}.sh'.format(NNmodel))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_down_total.root --JEC nominal -b central  -p samples/2018_total_Alot.plot -w moreMObins_pileupDown '.format(NNmodel), 'NN_pileupDown_{}.sh'.format(NNmodel))

    # ----------------btag----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b up  -p samples/2018_total_Alot.plot -w moreMObins_btagUp '.format(NNmodel), 'NN_btagUp_{}.sh'.format(NNmodel))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b down  -p samples/2018_total_Alot.plot -w moreMObins_btagDown '.format(NNmodel), 'NN_btagDown_{}.sh'.format(NNmodel))


# for NNmodel in NNmodels:

#     # ----------------nominal----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -w MVAcut_nominal --useMVAcut 0.7'.format(NNmodel), 'NN_nominal_{}.sh'.format(NNmodel))

#     # ----------------JEC----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC up -b central  -w MVAcut_JECUp --useMVAcut 0.7'.format(NNmodel), 'NN_JECup_{}.sh'.format(NNmodel))

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC down -b central  -w MVAcut_JECDown --useMVAcut 0.7'.format(NNmodel), 'NN_JECdown_{}.sh'.format(NNmodel))

#     # ----------------pileup----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_up_total.root --JEC nominal -b central  -w MVAcut_pileupUp --useMVAcut 0.7'.format(NNmodel), 'NN_pileupUp_{}.sh'.format(NNmodel))

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_down_total.root --JEC nominal -b central  -w MVAcut_pileupDown --useMVAcut 0.7'.format(NNmodel), 'NN_pileupDown_{}.sh'.format(NNmodel))

#     # ----------------btag----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b up  -w MVAcut_btagUp --useMVAcut 0.7'.format(NNmodel), 'NN_btagUp_{}.sh'.format(NNmodel))

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b down  -w MVAcut_btagDown --useMVAcut 0.7'.format(NNmodel), 'NN_btagDown_{}.sh'.format(NNmodel))


#numbers = [120 ,121 ,122 ,123 ,130 ,131 ,132 ,133 ,143 ,171 ,328 ,329 ,330 ,331 ,332 ,333 ,365 ,449 ,450 ,451 ,452 ,453 ,454 ,467 ,468 ,469 ,470 ,471 ,475 ,476 ,477 ,478 ,479 ,480]

#numbers = [120, 122, 123, 133, 143 ,171, 328, 365, 453, 467, 475]

numbers = [365]

BDTs = ['BDT_GS_{}.bin'.format(x) for x in numbers]

#BDTs = ['BDT_GS_467.bin', 'BDT_GS_328.bin']
BDTs = ['BDT_GS_120.bin', 'BDT_GS_123.bin', 'BDT_GS_365.bin', 'BDT_GS_475.bin', 'BDT_GS_467.bin','BDT_GS_467_8020.bin', 'BDT_GS_123.bin']

BDTs = ['BDT_GS_467_8020.bin']

#BDTs = ['BDT_GS_467_8020_mll.bin']

#######
# BDT #
#######

for BDT in BDTs:

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central --DY 1.10 -w DYUp1.10 '.format(BDT), 'BDT_nominal_{}.sh'.format(BDT))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central --DY 1.05 -w DYUp1.05 '.format(BDT), 'BDT_nominal_{}.sh'.format(BDT))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central --DY 0.95 -w DYUp0.95 '.format(BDT), 'BDT_nominal_{}.sh'.format(BDT))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central --DY 0.9 -w DYDown0.9 '.format(BDT), 'BDT_nominal_{}.sh'.format(BDT))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central --QCD up -w moreMObins_QCDUp '.format(BDT), 'BDT_nominal_{}.sh'.format(BDT))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central --QCD down -w moreMObins_QCDDown '.format(BDT), 'BDT_nominal_{}.sh'.format(BDT))



    # ----------------nominal----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -w moreMObins_nominal '.format(BDT), 'BDT_nominal_{}.sh'.format(BDT))

    # ----------------JEC----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC up -b central  -w moreMObins_JECup '.format(BDT), 'BDT_JECup_{}.sh'.format(BDT))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC down -b central  -w moreMObins_JECdown '.format(BDT), 'BDT_JECdown_{}.sh'.format(BDT))

    # ----------------pileup----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_up_total.root --JEC nominal -b central  -w moreMObins_pileupUp '.format(BDT), 'BDT_pileupUp_{}.sh'.format(BDT))
 
    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_down_total.root --JEC nominal -b central  -w moreMObins_pileupDown '.format(BDT), 'BDT_pileupDown_{}.sh'.format(BDT))

    # ----------------btag----------------

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b up  -w moreMObins_btagUp '.format(BDT), 'BDT_btagUp_{}.sh'.format(BDT))

    runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/{} -p samples/2018_total_BDT_Alot.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b down  -w moreMObins_btagDown '.format(BDT), 'BDT_btagDown_{}.sh'.format(BDT))




# #######
# # BDT #
# #######

# # for BDT in BDTs:

#     # ----------------nominal----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b central  -w MVAcut_nominal --useMVAcut 0.7', 'BDT_nominal.sh')

#     # ----------------JEC----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC up -b central  -w MVAcut_JECup --useMVAcut 0.7', 'BDT_JECup.sh')

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC down -b central  -w MVAcut_JECdown --useMVAcut 0.7', 'BDT_JECdown.sh')

#     # ----------------pileup----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_up_total.root --JEC nominal -b central  -w MVAcut_pileupUp --useMVAcut 0.7', 'BDT_pileupUp.sh')

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_down_total.root --JEC nominal -b central  -w MVAcut_pileupDown --useMVAcut 0.7', 'BDT_pileupDown.sh')

#     # ----------------btag----------------

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b up  -w MVAcut_btagUp --useMVAcut 0.7', 'BDT_btagUp.sh')

#     runCommandAsJob('python leptonPlots.py -t no -m machineLearning/models/BDT_final_80_0_20_v3.bin -p samples/2018_total_BDT.plot -x yes --pileupFile weights/pileup/pileup_nominal_total.root --JEC nominal -b down  -w MVAcut_btagDown --useMVAcut 0.7', 'BDT_btagDown.sh')


# runCommandAsJob('python makeTreeML.py -c samples/background_2018_v3.conf -s background_2018', 'bkg.sh')
# runCommandAsJob('python makeTreeML.py', 'signal.sh')

