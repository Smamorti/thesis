for y in NN_1_8020_24epochs NN_2_8020_10epochs NN_2_8020_12epochs NN_2_8020_14epochs NN_3_8020_5epochs NN_3_8020_6epochs NN_5_8020_12epochs
do
    for x in JECdown JECup nominal pileupDown pileupUp btagDown btagUp
    do
    python pklPlot.py -f histograms/$y/$x/histList_2018_total.pkl -d histograms/$y/$x/histList_2018_total_data.pkl
    done
done
