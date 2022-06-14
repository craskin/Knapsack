import pandas as pd
from itertools import chain

def printMatrix(m):
    for row in m:
        print(row)

def investmentFilename(file):
    df = pd.read_csv(file)
    frame = pd.DataFrame(df)
    frame = frame.drop(0) # dropping the United States
    # print(frame)
    return frame

def loadInvestments(frame):
    portfolio = []
    state = frame['RegionName'].tolist()
    avg = frame['Zhvi'].tolist()
    dfAvg = pd.DataFrame(avg)
    # print(dfAvg)
    tenyr = (frame['10Year'].tolist())
    tenyr = pd.DataFrame(tenyr)
    roi = tenyr.multiply(dfAvg, axis='columns', level=None, fill_value=None)
    # print(roi)
    # roi = pd.DataFrame(roi)
    ROI = roi.values.tolist()
    ROI = list(chain.from_iterable(ROI))
    print("InvestmentName InvestmentCost EstimatedReturnOnInvestment")
    for i in range(len(state)):
        portfolio.append([state[i], int(avg[i]), float(ROI[i])])
        print(state[i], '\t', avg[i], '\t', ROI[i])

    return portfolio

def optimizeInvestments(invstmt, money):
    """ knapsack problem """
    n = len(invstmt)
    val = []
    name = []
    roi = []

    for i in invstmt:
        name.append(i[0])
        val.append(i[-1])
        roi.append(i[1])

    K = [[0 for x in range(money + 1)] for x in range(n + 1)]
    I = [[0 for x in range(money + 1)] for x in range(n + 1)]
    traceback = [[False for x in range(money + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(money + 1):
            if i == 0 or w == 0:
                K[i][w] = float(0)
                I[i][w] = ""
                traceback[i][w] = False

            elif roi[i - 1] <= w:

                if (val[i - 1] + K[i - 1][w - roi[i - 1]] > K[i - 1][w]):
                    K[i][w] = val[i - 1] + K[i - 1][w - roi[i - 1]]
                    traceback[i][w] = True

                    if len(I[i - 1][w - roi[i - 1]]) > 0:
                        I[i][w] = name[i - 1] + " & " + I[i - 1][w - roi[i - 1]]
                    else:
                        I[i][w] = name[i - 1]

                else:
                    K[i][w] = K[i - 1][w]
                    I[i][w] = I[i - 1][w]
                    traceback[i][w] = False

            else:
                K[i][w] = K[i - 1][w]
                I[i][w] = I[i - 1][w]
                traceback[i][w] = False

        print('optimal: ')
        printMatrix(K)
        print("traceback: ")
        printMatrix(traceback)

    portfolio = 'With $'+ str(money) + ", invest in " + str(I[n][money]) + " for a ROI of $" + str(K[n][money])
    """print("Picked: ", I[n][money])
    print("Estimated return: ", K[n][money])"""
    return portfolio

if __name__ == '__main__':
    dataFrame = investmentFilename("zhvi-short.csv")
    # dataFrame = investmentFilename('state_zhvi_summary_allhomes.csv')

    money = int(input("Enter the amount of money you want to invest here: ")) # having this be an input is easier than adjusting this number everytime
    items = loadInvestments(dataFrame)
    print(items)

    print(optimizeInvestments(items, money))

