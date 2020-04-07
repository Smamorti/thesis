for wp in 0.85986 0.757869 0.758521 0.759173 0.960548
do
    cp BDT/BDT_final_fullData_wp=$wp/Hist_2018*SR*linear*.pdf SRplots/SR_BDT_$wp.pdf
done

for wp in 0.763306 0.813306 0.863306
do
    cp NN/NN_*_wp=$wp/Hist_2018*SR*linear*.pdf SRplots/SR_NN_$wp.pdf
done
