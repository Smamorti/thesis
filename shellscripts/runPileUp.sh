python leptonPlots.py -t yes -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w testing_down --pileupFile weights/pileup/pileup_down_total.root
python pklPlot.py -f histograms/NN_final_80_0_20_18epochs_v3_wp\=testing_down/histList_2018_total.pkl -d histograms/NN_final_80_0_20_18epochs_v3_wp\=testing_down/histList_2018_total_data.pkl

python leptonPlots.py -t yes -m machineLearning/models/NN_final_80_0_20_18epochs_v3.h5 -x yes -w testing_nominal --pileupFile weights/pileup/pileup_nominal_total.root
python pklPlot.py -f histograms/NN_final_80_0_20_18epochs_v3_wp\=testing_nominal/histList_2018_total.pkl -d histograms/NN_final_80_0_20_18epochs_v3_wp\=testing_nominal/histList_2018_total_data.pkl
