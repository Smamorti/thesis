cd
cd thesis
for i in normal JECUp JECDown
do
python pklPlot.py -f histograms/NN_final_80_0_20_18epochs_v3_wp\=$i/histList_2018_total.pkl -d histograms/NN_final_80_0_20_18epochs_v3_wp\=$i/histList_2018_total_data.pkl -p samples/2018_total.plot
python pklPlot.py -f histograms/BDT_final_80_0_20_v3_wp\=$i/histList_2018_total.pkl -d histograms/BDT_final_80_0_20_v3_wp\=$i/histList_2018_total_data.pkl -p samples/2018_total_BDT.plot
done