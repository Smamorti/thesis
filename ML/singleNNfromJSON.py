import json

filename = 'bestModels_nn_extraParams2/generation_37/model_rank_1/configuration_relu_bat=203_bat=1_bat=0_bat=1_dro=0_dro=0_dro=0_lea=0p646007967891_lea=0p930081585622_num=200_num=3_Nadam_uni=511.json'

with open(filename) as f:

    dic = json.load(f)

outputstring = 'python runTraining.py input_nn_single.py'

for key in dic:

    outputstring += ' {}={}'.format(key, dic[key])

print(outputstring) 

