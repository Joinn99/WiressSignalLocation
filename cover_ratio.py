import csv
import numpy as np


class CombinationsFinder:
    def __init__(self):
        with open('./data/dataAll.csv', encoding='utf-8') as csvfile:
            test_reader = csv.reader(csvfile, delimiter=',')
            next(test_reader)
            train_set, target_set = [], []
            for row in test_reader:
                train_set.append([float(signal) for signal in row[:-2]])
                target_set.append([float(coord) for coord in row[-2:]])
            self.data = np.array(train_set)
            self.target = np.array(target_set)
        with open('./data/testAll.csv', encoding='utf-8') as csvfile:
            test_reader = csv.reader(csvfile, delimiter=',')
            next(test_reader)
            test_set = []
            for row in test_reader:
                test_set.append([float(signal) for signal in row])
            self.data = np.vstack((self.data, np.array(test_set)))

    def cover_number(self, sector_list, index):
        number = np.sum((np.max(self.data[:, sector_list[:index]+sector_list[index+1:]],
                                axis=1) > -105.0).astype(np.int))
        return number

    def cover_ratio(self, sector_list, index):
        ratio = np.sum((np.max(self.data[:, sector_list[:index]+sector_list[index+1:]], axis=1) > -
                        105.0).astype(np.int)) / float(len(sector_list)-1)
        return ratio


def find_the_deepest(cof, sector_list, min_sector, final_list):
    cover_list, max_cover = [], 0
    for index, _ in enumerate(sector_list):
        cover_list.append(cof.cover_number(sector_list, index))
        max_cover = max(max_cover, cover_list[index])
    if max_cover > 4234:
        max_list = [index for index, cover in enumerate(
            cover_list) if cover == max_cover]
        next_sector_list = [list(sector_list) for _ in range(len(max_list))]
        for index, _ in enumerate(next_sector_list):
            del next_sector_list[index][max_list[index]]
            find_the_deepest(cof, next_sector_list[index], min_sector, final_list)
    else:
        if len(sector_list) == min_sector[0]:
            if sector_list not in final_list:
                final_list += [sector_list]
        elif len(sector_list) < min_sector[0]:
            final_list = [sector_list]
            min_sector[0] = len(sector_list)
        else:
            pass
    return final_list


if __name__ == "__main__":
    COF = CombinationsFinder()
    LIST = find_the_deepest(COF, [IND for IND in range(25)], [25], [])
    np.savetxt('./Sector.txt', np.array(LIST, dtype=np.int8), fmt='%d')
