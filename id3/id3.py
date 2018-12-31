# id3

"""

 data_set :

    attribute values : integer

 [[1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]]

 target :

    target values : integer

 [target_row_0, target_row_1, target_row_2]


"""


def generate_2d(rows, cols, rand_low, rand_high):
    from random import randint
    return [[randint(rand_low, rand_high)
             for _ in range(cols)] for _ in range(rows)]


def print_data(data_set, target):
    # print data like 2d table with the target of each row
    if ((not data_set) or
        (not data_set[0]) or
        (not target) or
            (len(target) != len(data_set))):
        return
    print("rows = ", len(data_set), " cols = ", len(data_set[0]), " :\n")
    for i in range(len(target)):
        for n in data_set[i]:
            print("{0:<4} ".format(n), end="")
        print("-   ", target[i])
    print("\n\n")


def print_id3_result(result, output_file, tabs=0, newline='\n'):
    if type(result) == list:
        # if its list only the attribute and his value
        # are printed and there is call for its content
        for r in result:
            for _ in range(tabs):
                print("\t" * 2, end="")
                output_file.write("\t" * 2)
            print("attr =", r[len(r) - 2], ", val =", r[len(r) - 1])
            output_file.write("attr = {0} , val = {1}{2}".format(
                r[len(r) - 2], r[len(r) - 1], newline))
            for i in range(len(r) - 2):
                print_id3_result(r[i], output_file, tabs + 1, newline)
    else:
        # if its dictionary it will be printed
        d = result["data_set"]
        t = result["target"]
        print()
        output_file.write(newline)
        for i in range(len(d)):
            for _ in range(tabs):
                print("\t" * 2, end="")
                output_file.write("\t" * 2)
            print(d[i], " - ", t[i])
            output_file.write("{0} - {1}{2}".format(d[i], t[i], newline))
        print()
        output_file.write(newline)


def h(target):
    from math import log
    from collections import Counter
    count_items = Counter(target).items()
    len_target = len(target)
    hr = -1 * sum([(value / len_target) * log((value / len_target), 2)
                   for key, value in count_items])
    return hr + 0.0  # to avoid -0.0


def ig(data_set, attr, target):
    h_target = h(target)
    attr_row_values = [row[attr] for row in data_set]
    attr_available_values = list(set(attr_row_values))
    sum_of_subsets = 0
    for v in attr_available_values:
        attr_target_values = []
        for i in range(len(data_set)):
            if data_set[i][attr] == v:
                attr_target_values.append(target[i])
        sum_of_subsets += len(attr_target_values) / \
            len(data_set) * h(attr_target_values)
    return h_target - sum_of_subsets


def id3_recursive(data_set, target):
    # check that the there is data
    if (not data_set) or (not data_set[0]) or (not target):
        return {'data_set': [], 'target': []}

    # find attribute with max gain
    cols = len(data_set[0])
    max_index = 0

    # get list of each attribute and it's information gain
    ig_result = [[i, ig(data_set, i, target)] for i in range(cols)]
    for i in range(len(ig_result)):
        if ig_result[i][1] > ig_result[max_index][1]:
            max_index = i

    # there is no need to split the data
    if ig_result[max_index][1] == 0:
        return {'data_set': data_set, 'target': target}

    # split by attribute
    attr_available_values = list(set([row[max_index] for row in data_set]))
    result = []

    # create subset of the data and target
    # for each attribute value and call id3 for it
    for attr_val in attr_available_values:
        data_subset = []
        target_subset = []
        for i in range(len(data_set)):
            if data_set[i][max_index] == attr_val:
                data_subset.append(data_set[i])
                target_subset.append(target[i])
        result.append(
            [id3_recursive(data_subset, target_subset), max_index, attr_val])
    return result


def ig_calculation_example():
    # example of information gain calculation
    from random import randint
    rows = 100
    cols = rows // 10
    data_set = generate_2d(rows, cols, 0, rows // 10)
    target = [randint(0, 1) for _ in range(rows)]
    max_index = 0
    result = [[i, ig(data_set, i, target)] for i in range(cols)]
    for i in range(len(result)):
        if result[i][1] > result[max_index][1]:
            max_index = i
        print("attribute = ", "{0:<4}".format(
            result[i][0]), ", information gain = ", result[i][1])
    if len(result) > 0:
        print("\nmax information gain : attribute = ",
              result[max_index][0], ", information gain = ",
              result[max_index][1])


def main():
    from random import randint
    from os import linesep

    rows = 100
    cols = 10
    data_set = generate_2d(rows, cols, 0, 3)
    target = [randint(0, 1) for _ in range(rows)]
    r = id3_recursive(data_set, target)

    output_file = 'id3_output.txt'

    try:
        with open(output_file, 'w') as f:
            print_id3_result(r, f, 0, linesep)
    except Exception as e:
        print("\n\nthere was error to write to file '{0}' : {1}".format(
            output_file, e))


if __name__ == '__main__':
    main()
