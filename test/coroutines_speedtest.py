from pyalma import alma
from datetime import datetime
import csv
import ast

'''
The following is a series of functional tests that will
allow you to run speed tests on coroutine methods.
To use, set the number of items you want to test in "TEST_NUM"
You can only test one method at a time.
However, the suite is designed to be run sequentially, to generate the
files you need for later tests.
'''


# set the number of items you would like to test
# and your API key and Region
TEST_NUM = 100
API_KEY = ''
REGION = ''

api = alma.Alma(API_KEY, REGION)


def list_from_csv(csvfile, number):
    '''
    Takes a csv file, column headings may be either:
    - ids (with each row containin a dictionary of mms_id,
      holding_id, item_pid, and/or request_id)and data,
        OR
    - mms_id, holding_id, item_pid, and or request_id; and data
    Returns a list of dictionaries in format required for coroutines:
        [{
            'data': data,
            'ids':  {
                    'mms_id': mms_id,
                    'holding_id': holding_id,
                    'item_pid': item_pid,
                    'request_id': request_id
                    }
          },
          ...
          ]
    '''
    with open(csvfile, 'rt') as handle:
        reader = csv.DictReader(handle, delimiter=',')
        headers = reader.fieldnames
        dict_rows = []
        count = number
        for row in reader:
            dict_row = {}
            if 'ids' not in headers:
                dict_row['ids'] = {}
                if count > 0:
                    if 'data' not in headers:
                        dict_row['data'] = None
                    for header in headers:
                        if header == 'data':
                            dict_row[header] = row[header]
                        elif header == "":
                            continue
                        else:
                            dict_row['ids'][header] = row[header]
                    dict_rows.append(dict_row)
                    count -= 1
                else:
                    break
            else:
                if count > 0:
                    dict_row['ids'] = ast.literal_eval(row['ids'])
                    dict_row['data'] = row['data']
                    dict_rows.append(dict_row)
                    count -= 1
                else:
                    break

        return dict_rows


def write_to_csv(results, handle):
    '''
    Takes a list of results (a list of dictionaries),
    Returns a CSV file with the given filename.
    '''
    with open(handle, 'w') as csvfile:
        linewriter = csv.writer(csvfile)
        linewriter.writerow(["ids", "status", "data"])
        for line in results:
            linewriter.writerow(line)


def test_general(input_file, output_file, test_func):
    '''
    Takes a CSV of the data you wish to feed into a function, the filename you
    desire for the output, and the name of the function you wish to test.
    Returns a list of results (a list of dictionaries).
    '''
    begin = datetime.now()
    test_input = list_from_csv(input_file, TEST_NUM)
    test_output = test_func(test_input)
    output_len = len(test_output)
    end = datetime.now()
    diff = end - begin
    errors = 0
    for line in test_output:
        if line[1] > 200:
            errors += 1
    print('\n\nReturned {} rows, with {} errors'.format((output_len - errors), errors))
    print("\n\nTime elapsed for {} ids: \n    Coroutines: {} \n ".format(output_len, diff))
    write_to_csv(test_output, output_file)
    return test_output


'''
Below are tests for each coroutine method.
'''


def test_cor_get_bib(input_file='test/mms.csv',
                     output_file='test/output_get_bib.csv', content_type='xml', accept='xml'):
    print("\n\nTesting cor_get_bib")
    test_func = api.cor_get_bib
    return test_general(input_file, output_file, test_func)


def test_cor_put_bib(input_file="test/output_get_bib.csv",
                     output_file='test/output_put_bib.csv', content_type='xml', accept='xml'):
    print("\n\nTesting cor_put_bib")
    test_func = api.cor_put_bib
    return test_general(input_file, output_file, test_func)


def test_cor_get_holdings(input_file='test/mms_in.csv',
                          output_file='test/output_get_holdings.csv'):
    print("\n\nTesting cor_get_holdings")
    test_func = api.cor_get_holdings
    test_general(input_file, output_file, test_func)


def test_cor_get_holding(input_file='test/mms_holding.csv',
                         output_file="test/output_get_holding.csv"):
    print("\n\nTesting cor_get_holding")
    test_func = api.cor_get_holding
    test_general(input_file, output_file, test_func)


def test_cor_put_holding(input_file='test/output_get_holding.csv',
                         output_file='test/output_put_holding.csv'):
    print("\n\nTesting cor_put_holding")
    test_func = api.cor_put_holding
    test_general(input_file, output_file, test_func)

def test_cor_get_items(input_file='test/mms_holding.csv',
                       output_file='test/output_get_items.csv'):
    print("\n\nTesting cor_get_items")
    test_func = api.cor_get_items
    test_general(input_file, output_file, test_func)


def test_cor_get_item(input_file='test/mms_holding_item.csv',
                      output_file='test/output_get_item.csv'):
    print("\n\nTesting cor_get_item")
    test_func = api.cor_get_item
    test_general(input_file, output_file, test_func)


def test_cor_put_item(input_file='test/output_get_item.csv',
                      output_file='test/output_put_item.csv'):
    print("\n\nTesting cor_put_item")
    test_func = api.cor_put_item
    test_general(input_file, output_file, test_func)


def test_cor_post_loan(input_file='test/mms_holding_item_data.csv',
                       output_file='test/output_post_loan.csv'):
    print("\n\nTesting cor_post_loan")
    test_func = api.cor_post_loan
    test_general(input_file, output_file, test_func)


def test_cor_get_bib_requests(input_file='test/mms_in.csv',
                              output_file='test/output_get_bib_requests.csv'):
    print("\n\nTesting cor_get_bib_requests")
    test_func = api.cor_get_bib_requests
    test_general(input_file, output_file, test_func)


def test_cor_get_item_requests(input_file='test/mms_holdings_items_with_requests.csv',
                               output_file='test/output_get_item_requests.csv'):
    print("\n\nTesting cor_get_item_requests")
    test_func = api.cor_get_item_requests
    test_general(input_file, output_file, test_func)


def test_cor_post_bib_request(input_file='test/item_request_objects.csv',
                              output_file='test/output_post_bib_request.csv'):
    print("\n\nTesting cor_post_bib_request")
    test_func = api.cor_post_bib_request
    test_general(input_file, output_file, test_func)


def test_cor_post_item_request(input_file='test/item_request_objects.csv',
                               output_file='test/output_put_item_request.csv'):
    print("\n\nTesting cor_post_item_request")
    test_func = api.cor_post_item_request
    test_general(input_file, output_file, test_func)


def test_cor_put_bib_request(input_file='test/output_get_bib_requests.csv',
                               output_file='test/output_put_bib_request.csv'):
    print("\n\nTesting cor_put_bib_request")
    test_func = api.cor_put_bib_request
    test_general(input_file, output_file, test_func)

def test_cor_put_item_request(input_file='test/output_get_item_requests.csv',
                               output_file='test/output_put_item_request.csv'):
    print("\n\nTesting cor_put_item_request")
    test_func = api.cor_put_item_request
    test_general(input_file, output_file, test_func)


def test_cor_del_item_request(input_file='test/item_request_objects.csv',
                               output_file='test/output_del_item_request.csv'):
    print("\n\nTesting cor_del_item_request")
    test_func = api.cor_del_item_request
    test_general(input_file, output_file, test_func)


def test_cor_del_bib_request(input_file='test/item_request_objects.csv',
                               output_file='test/output_del_bib_request.csv'):
    print("\n\nTesting cor_del_bib_request")
    test_func = api.cor_del_bib_request
    test_general(input_file, output_file, test_func)


def test_cor_get_bib_booking_availability(input_file='test/mms.csv',
                                          output_file='test/output_get_bib_booking_availability.csv'):
    print("\n\nTesting cor_get_bib_booking_availability")
    test_func = api.cor_get_bib_booking_availability
    test_general(input_file, output_file, test_func)


def test_cor_get_item_booking_availability(input_file='test/mms_holding_item.csv',
                                           output_file='test/output_get_item_booking_availability.csv'):
    print("\n\nTesting cor_get_item_booking_availability")
    test_func = api.cor_get_item_booking_availability
    test_general(input_file, output_file, test_func)


if __name__ == '__main__':

    test_cor_get_bib()
    # test_cor_put_bib()

    # test_cor_get_holdings()

    # test_cor_get_holding()
    # test_cor_put_holding()

    # test_cor_get_items()

    # test_cor_get_item()
    # test_cor_put_item()

    # test_cor_get_bib_requests()
    # test_cor_get_item_requests()



    '''
    Tests below are for not finalized methods:
    '''

    # test_cor_del_bib_request()
    # test_cor_del_item_request()

    # test_cor_post_loan()

    # test_cor_post_bib_request()
    # test_cor_post_item_request()

    # test_cor_put_bib_request()
    # test_cor_put_item_request()

    # test_cor_get_bib_booking_availability()
    # test_cor_get_item_booking_availability()
