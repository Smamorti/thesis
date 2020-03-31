import os

rootdir = 'bestModels_xgboost_extraParams'

bestFive = [0,0,0,0,0,0,0,0,0,0]
bestFiveDirecs = ['','','','','','','','','','']

for subdir, dirs, files in os.walk(rootdir):

    for file in files:

        if '/trainingOutput' in os.path.join(subdir, file):
#        if 'model_rank_1/trainingOutput' in os.path.join(subdir, file):

            lines = []

            with open(os.path.join(subdir, file)) as f:

                line = f.readline()

                while line:

                    lines.append(line)
                    line = f.readline()

                auc = float(lines[-2].split('=')[-1].strip())

                for i in range(len(bestFive)):

                    if auc > bestFive[i]:

                        bestFive.insert(i, auc)
                        bestFive.pop()
                        
                        bestFiveDirecs.insert(i, str(os.path.join(subdir, file)))
                        bestFiveDirecs.pop()

                        break
# Print results

print('Five best neural nets:')

for i in range(len(bestFive)):

    print('{}: AUC = {}, hyperparams = {}'.format(i+1, bestFive[i], bestFiveDirecs[i]))

