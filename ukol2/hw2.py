from random import choice


def add_random(row, candidates):
    empty_spaces = []

    if row == []:
        return(False)

    empty_spaces = zero_indexes(row)

    if empty_spaces == []:
        return(False)

    row[choice(empty_spaces)] = choice(candidates)
    return(True)


def zero_indexes(row):
    zeroes = []
    for i in range(0, len(row)):
        if row[i] == 0:
            zeroes.append(i)
    return(zeroes)


def zero_adder(row, zeroes, merged, to_left):
    if not to_left:
        row.reverse()
    for i in range(0, len(zeroes)+merged):
        if not to_left:
            row.insert(0, 0)
        else:
            row.append(0)
    return(row)


def slide_basic(row, to_left):
    old_row = row.copy()
    # get rid of zeroes
    if not to_left:
        row.reverse()

    zeroes = zero_indexes(row)
    # ak by som siel po indexoch, vyuzil by som fci zero_indexes iba raz
    for elem in reversed(zeroes):
        row.pop(elem)

    # compare
    index = 0
    merged = 0
    while index < len(row)-1:
        if row[index] == row[index+1]:
            row[index] += row[index+1]
            row.pop(index+1)
            merged += 1
        index += 1

    # add zeroes
    row = zero_adder(row, zeroes, merged, to_left)

    return row != old_row


def slide_multi(row, to_left):
    old_row = row.copy()
    # get rid of zeroes
    if not to_left:
        row.reverse()

    zeroes = zero_indexes(row)

    for elem in reversed(zeroes):
        row.pop(elem)
    # compare
    index = 0
    merged = 0
    while len(row) > index:
        taken = row[index]
        while (len(row) > index+1) and (taken == row[index+1]):
            row[index] += row[index+1]
            row.pop(index+1)
            merged += 1
        index += 1
    # add zeroes

    row = zero_adder(row, zeroes, merged, to_left)

    return row != old_row


def main():
    # --- add_random ---

    results = [[2, 1, 2, 0, 4], [2, 3, 2, 0, 4],
               [2, 0, 2, 1, 4], [2, 0, 2, 3, 4]]

    count = [0 for x in results]

    for i in range(1000):
        row = [2, 0, 2, 0, 4]
        assert add_random(row, [1, 3])
        for j in range(len(results)):
            if row == results[j]:
                count[j] += 1
                break

    assert sum(count) == 1000
    for freq in count:
        # if add_random is correct, the probability that this assert fails
        # is less than 1 in 500 000 000 (six sigma)
        assert 167 < freq < 333

    assert not add_random([2, 1, 2, 3, 4], [7, 5])

    # --- slide_basic ---

    row = [0, 2, 2, 0]
    assert slide_basic(row, True)
    assert row == [4, 0, 0, 0]
    row = [2, 2, 2, 2, 2]
    assert slide_basic(row, False)
    assert row == [0, 0, 2, 4, 4]
    row = [2, 0, 0, 2, 4, 2, 2, 2]
    assert slide_basic(row, True)
    assert row == [4, 4, 4, 2, 0, 0, 0, 0]
    row = [3, 0, 6, 3, 3, 3, 6, 0, 6]
    assert slide_basic(row, False)
    assert row == [0, 0, 0, 0, 3, 6, 3, 6, 12]
    row = [16, 8, 4, 2, 0, 0, 0]
    assert not slide_basic(row, True)
    assert row == [16, 8, 4, 2, 0, 0, 0]

    # --- slide_multi ---

    row = [0, 2, 2, 0]
    assert slide_multi(row, True)
    assert row == [4, 0, 0, 0]
    row = [2, 2, 2, 2, 2]
    assert slide_multi(row, False)
    assert row == [0, 0, 0, 0, 10]
    row = [2, 0, 0, 2, 4, 2, 2, 2]
    assert slide_multi(row, True)
    assert row == [4, 4, 6, 0, 0, 0, 0, 0]
    row = [3, 0, 6, 3, 3, 3, 6, 0, 6]
    assert slide_multi(row, False)
    assert row == [0, 0, 0, 0, 0, 3, 6, 9, 12]
    row = [16, 8, 4, 2, 0, 0, 0]
    assert not slide_multi(row, True)
    assert row == [16, 8, 4, 2, 0, 0, 0]


if __name__ == '__main__':
    main()
