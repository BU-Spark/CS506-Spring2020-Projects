import numpy as np
import pandas as pd

def import_data(file):
    data_set = pd.read_csv(file, engine='python')
    return data_set

def category_to_numeric(data):
    for column in data [['Status', 'D-Attorney', 'Judgement Type', 'JudgeMent Method']]:
        # Select column contents by column name using [] operator
        columnSeriesObj = data[column]
        print('Colunm Name : ', column)
        print(type(columnSeriesObj.values))
        for i in range(len(columnSeriesObj.values)):
            if column == 'Status':
                if columnSeriesObj.values[i] == None:
                    pass
                elif columnSeriesObj.values[i] == '':
                    columnSeriesObj.values[i] = 0
                elif columnSeriesObj.values[i] == 'Disposed for Statistical Purposes':
                    columnSeriesObj.values[i] = 1
                elif columnSeriesObj.values[i] == 'Closed Case Transfered':
                    columnSeriesObj.values[i] = 2
                elif columnSeriesObj.values[i] == 'Open':
                    columnSeriesObj.values[i] = 3
                elif columnSeriesObj.values[i] == 'Closed':
                    columnSeriesObj.values[i] = 4
                elif columnSeriesObj.values[i] == 'Active':
                    columnSeriesObj.values[i] = 5

            if column == 'Judgement Type':
                if columnSeriesObj.values[i] == None:
                    pass
                elif columnSeriesObj.values[i] == '':
                    columnSeriesObj.values[i] = 0
                elif columnSeriesObj.values[i] == 'Judgment for Plaintiff for Possession and Rent':
                    columnSeriesObj.values[i] = 1
                elif columnSeriesObj.values[i] == 'Not Held But Event Resolved':
                    columnSeriesObj.values[i] = 2
                elif columnSeriesObj.values[i] == 'Notice of dismissal without prejudice':
                    columnSeriesObj.values[i] = 3
                elif columnSeriesObj.values[i] == 'Case removed to Housing Court':
                    columnSeriesObj.values[i] = 4
                elif columnSeriesObj.values[i] == 'NA':
                    columnSeriesObj.values[i] = 5

            if column == 'JudgeMent Method':
                if columnSeriesObj.values[i] == None:
                    pass
                elif columnSeriesObj.values[i] == '':
                    columnSeriesObj.values[i] = 0
                elif columnSeriesObj.values[i] == 'after defendant(s) failed to appear':
                    columnSeriesObj.values[i] = 1
                elif columnSeriesObj.values[i] == 'by agreement of the parties':
                    columnSeriesObj.values[i] = 2
                elif columnSeriesObj.values[i] == 'NA':
                    columnSeriesObj.values[i] = 3
    return data
data = import_data("./csv/csvData.csv")
data = category_to_numeric(data)
print(data)
data_array = np.array(data)





