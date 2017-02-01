from pprint import pprint
# first import the library and create an api object
from pyalma.alma import Alma
from datetime import datetime

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
    bibs = api.get_bibs(ids)
    end = datetime.now()
    diff = end - begin
    # for bib in bibs:
    #     pprint(bib)
    #     print(type(bib))
    print('Returned {} coroutine bibs'.format(len(bibs)))
    return diff


# for the below, if you'd like to compare how long it takes to run serially,
# un-comment the t-normal line, and the "print time elapsed for both normal and coroutines" line
# CAUTION: do not run for large numbers of mms_ids!
num = int(input("Enter number of items to test:  "))
ids = create_id_list(num)
t_coroutine = test_coroutines(ids)
# t_normal = test_normal(ids)

#print time elapsed for both normal and coroutines
# print("\n\nTime elapsed for {} ids: \n    Normal:     {} \n    Coroutines: {} \n ".format(num, t_normal, t_coroutine))

#print time elapsed for coroutines only
print("\n\nTime elapsed for {} ids: \n    Coroutines: {} \n ".format(num, t_coroutine))
