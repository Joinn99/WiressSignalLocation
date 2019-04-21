import csv
from itertools import combinations
import numpy as np



def train_data_load(file):
    with open(file, encoding='utf-8') as csvfile:
        test_reader = csv.reader(csvfile, delimiter=',')
        next(test_reader)
        train_set, target_set = [], []
        for row in test_reader:
            train_set.append([float(signal) for signal in row[:-2]])
            target_set.append([float(coord) for coord in row[-2:]])
        return np.array(train_set), np.array(target_set)


def test_data_load(file):
    with open(file, encoding='utf-8') as csvfile:
        test_reader = csv.reader(csvfile, delimiter=',')
        next(test_reader)
        test_set = []
        for row in test_reader:
            test_set.append([float(signal) for signal in row])
        return np.array(test_set)


def cover_ratio(signal_data):
    ratio = np.sum((np.max(signal_data, axis=1) > -
                    105.0).astype(np.int)) / float(signal_data.shape[0])
    return ratio

def cover_number(signal_data):
    number = np.sum((np.max(signal_data, axis=1) > -105.0).astype(np.int))
    return number


def ratio_calculation(signal_data, sector_number):
    max_ratio = 0
    with open('./Combinations.txt', 'w') as record:
        if sector_number > 0:
            sector_number = [sector_number]
        else:
            sector_number = [index for index in range(30)]
        for index in sector_number:
            sector_comb = combinations([sector for sector in range(24)], index)
            for comb in sector_comb:
                ratio = cover_ratio(signal_data[:, comb])
                max_ratio = max(ratio, max_ratio)
                if ratio > 0.95:
                    record.write(str(comb) +'\t' + str(ratio)[:8] + '%\n')
            print('\rIndex: ' + str(index), end='', flush=True)
    print('\nMax Ratio: ' + str(max_ratio))


if __name__ == "__main__":
    DATA, TARGET = train_data_load('./data/dataAll.csv')
    DATA_TEST = test_data_load('./data/testAll.csv')
    ALL = np.vstack((DATA, DATA_TEST))
    print(TARGET.shape)
    print(DATA.shape)
    print(DATA_TEST.shape)
    print(ALL.shape)
    