from pprint import pprint
# first import the library and create an api object
from pyalma.alma import Alma
from datetime import datetime
import csv

api = Alma(apikey='l7xxf7040f318112496b8c1862370d5679fe', region='US')


# creates a list of ids of number length
def create_id_list(number):
    ids = []
    counter = number
    while counter > 0:
        ids.append('9927390750001551')
        counter -= 1
    return ids


def test_normal(mm_ids):
        # creates a datetime object showing how long it took for mm_ids
        # to be retrieved serially
    begin = datetime.now()
    bibs = []
    for mm_id in mm_ids:
        bib = api.get_bib(mm_id)
        bibs.append(bib)
        # pprint(bib)
    end = datetime.now()
    diff = end - begin
    print('Returned {} normal bibs'.format(len(bibs)))
    return diff


def test_coroutines(mm_ids):
        # creates a datetime object showing long it took for mm_ids
        # to be retrieved async via coroutines
    begin = datetime.now()
    bibs = api.get_bibs(mm_ids)
    end = datetime.now()
    diff = end - begin
    count = 0
    for bib in bibs:
        if bib == None:
            count += 1
    print('\n\nReturned {} coroutine bibs, with {} errors'.format((len(bibs)-count),count))
    return diff


def list_from_csv(csvfile, number):
    with open(csvfile, 'rt', encoding='utf8') as handle:
        reader = csv.reader(handle)
        ids = []
        counter = number
        for row in reader:
            if counter > 0:
                ids.append(row[0])
            counter -= 1
    return ids


def test_repeat_bibs():
    num = int(input("Enter number of items to test:  "))
    ids = create_id_list(num)
    t_coroutine = test_coroutines(ids)
    print("\n\nTime elapsed for {} ids: \n    Coroutines: {} \n ".format(num, t_coroutine))


def test_from_csv(handle, num):
    ids = list_from_csv(handle, num)
    t_coroutine = test_coroutines(ids)
    print("\n\nTime elapsed for {} ids: \n    Coroutines: {} \n ".format(num, t_coroutine))


if __name__ == '__main__':
    num = int(input("Enter number of items to test:  "))
    handle = 'bibs.csv'
    test_from_csv(handle, num)
