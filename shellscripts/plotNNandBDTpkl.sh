cd ..
python pklPlot.py -f histograms/BDT_final_fullData_wp\=0.757869/histList_2018_total.pkl
python pklPlot.py -f histograms/BDT_final_fullData_wp\=0.758521/histList_2018_total.pkl
python pklPlot.py -f histograms/BDT_final_fullData_wp\=0.759173/histList_2018_total.pkl
python pklPlot.py -f histograms/BDT_final_fullData_wp\=0.85986/histList_2018_total.pkl
python pklPlot.py -f histograms/BDT_final_fullData_wp\=0.960548/histList_2018_total.pkl

python pklPlot.py -f histograms/NN_Best_FullData_18epochs_wp\=0.763306/histList_2018_total.pkl
python pklPlot.py -f histograms/NN_Best_FullData_18epochs_wp\=0.813306/histList_2018_total.pkl
python pklPlot.py -f histograms/NN_Best_FullData_18epochs_wp\=0.863306/histList_2018_total.pkl

for wp in 0.5 0.6 0.65 0.75 0.8 0.85 0.9 0.95
do
python pklPlot.py -f histograms/NN_Best_FullData_18epochs_wp\=$wp/histList_2018_total.pkl
python pklPlot.py -f histograms/BDT_final_fullData_wp\=$wp/histList_2018_total.pkl
done