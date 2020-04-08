cd ..
for wp in 0.5 0.6 0.65 0.75 0.8 0.85 0.9 0.95
do 
    python3 jobSubmission.py BDT_final_fullData.bin $wp
    python3 jobSubmission.py NN_Best_FullData_18epochs.h5 $wp
done