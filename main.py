import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.stats import pearsonr

if __name__ == "__main__":
    # Creating dataset

    data_1 = np.random.normal(100, 10, 200)
    data_2 = np.random.normal(90, 20, 200)
    data_3 = np.random.normal(80, 30, 200)
    data_4 = np.random.normal(70, 40, 200)
    data_5 = np.random.normal(60, 50, 200)
    data = [data_1, data_2, data_3, data_4, data_5]

    df = pd.DataFrame()
    my_dict = {}

    for index in range(5):
        my_dict.setdefault(str(index), data[index])

    df = df.assign(**my_dict)

    mean = df.mean()
    median = df.median()
    print(df)

    print(mean)
    print(median)

    fig = plt.figure(figsize=(10, 7))

    # Creating axes instance
    ax = fig.add_axes([0, 0, 1, 1])

    # Creating plot
    bp = ax.boxplot(data)

    # show plot
    plt.show()

    for row in data:
        print("cov:")
        print(np.cov(row))
        print("cor:")
        print(pearsonr(row, row))
