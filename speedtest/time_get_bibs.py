from pprint import pprint
# first import the library and create an api object
from pyalma.alma import Alma
from datetime import datetime
import csv

api = Alma(apikey='', region='')


# creates a list of ids of number length
# def create_id_list(number):
#     ids = []
#     counter = number
#     while counter > 0:
#         ids.append('9927390750001551')
#         counter -= 1
#     return ids


# def test_normal(mm_ids):
#         # creates a datetime object showing how long it took for mm_ids
#         # to be retrieved serially
#     begin = datetime.now()
#     bibs = []
#     for mm_id in mm_ids:
#         bib = api.get_bib(mm_id)
#         bibs.append(bib)
#         # pprint(bib)
#     end = datetime.now()
#     diff = end - begin
#     print('Returned {} normal bibs'.format(len(bibs)))
#     return diff


def test_coroutines(mms_ids):
        # creates a datetime object showing long it took for mm_ids
        # to be retrieved async via coroutines
    begin = datetime.now()
    input_params = [{"ids": {'mms_id': mms_id}, "data": None} for mms_id in mms_ids]
    bibs = api.cor_get_bibs(input_params)
    end = datetime.now()
    diff = end - begin
    count = 0
    for bib in bibs:
        if bib[1] > 200:
            count += 1
    print('\n\nReturned {} coroutine bibs, with {} errors'.format((len(bibs)-count),count))
    return [diff, bibs]


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
    print("\n\nTime elapsed for {} ids: \n    Coroutines: {} \n ".format(num, t_coroutine[0]))


def write_to_csv(coroutines):
    with open('bibs_output.csv', 'w') as csvfile:
        bibwriter = csv.writer(csvfile)
        # bibwriter.writerow(['mms_id', 'status', 'msg'])
        bib_list = coroutines
        bibwriter.writerow(["ids", "status", "msg"])
        for bib in bib_list:
            bibwriter.writerow(bib)


def test_from_csv(handle, num):
    ids = list_from_csv(handle, num)
    t_coroutine = test_coroutines(ids)
    print("\n\nTime elapsed for {} ids: \n    Coroutines: {} \n ".format(num, t_coroutine[0]))
    return t_coroutine[1]


if __name__ == '__main__':
    num = int(input("Enter number of items to test:  "))
    handle = 'bibs.csv'
    bib_list = test_from_csv(handle, num)
    write_to_csv(bib_list)
