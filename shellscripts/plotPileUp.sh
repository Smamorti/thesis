for source in ttZ ttX ttW tt other DY
do
python pklPlot.py -p samples/nTrueInt.plot -f weights/pkl/ratio.pkl -d weights/pkl/data_data.pkl -t $source -e _$source
done