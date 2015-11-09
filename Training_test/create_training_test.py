import pandas as pd

trainingSet = []

csvFile = pd.read_csv("training.csv", low_memory=False)

for i in range(len(csvFile["tweets"])):
    
    trainingSet.append((csvFile["tweets"][i],csvFile["category"][i]))
