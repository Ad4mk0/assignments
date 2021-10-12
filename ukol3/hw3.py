# from time import sleep
# for game uncomment lines 1 , 214, 229
from typing import List, Optional, Tuple
from random import choice
PlayG = List[List[str]]


def new_playground(height: int, width: int) -> PlayG:
    playground = [[' ' for x in range(width)] for y in range(height)]
    return playground


def get(playground: PlayG, row: int, col: int) -> Optional[str]:
    return playground[row][col]


def put(playground: PlayG, row: int, col: int, symbol: str) -> bool:
    if playground[row][col] == ' ':
        playground[row][col] = symbol
        return True
    return False


def put_empty(playground: PlayG, row: int, col: int, symbol: str) -> None:
    playground[row][col] = symbol


def draw(playground: PlayG) -> None:
    x = 0
    char = ''
    for i in range(len(playground)):
        edge2 = ''
        edge = ''
        x += 1
        y = 0
        for elem in playground[i]:
            edge += ("+---")
            edge2 += ('| '+str(elem)+' ')
            y += 1
        if (x-1) < 10:
            edge2 = ' '+str(x-1)+' '+edge2
        else:
            edge2 = str(x-1)+' '+edge2
        edge = '   '+edge
        edge2 += ('|')
        edge += ('+')
        print(edge)
        print(edge2)
    print(edge)
    for i in range(ord('A'), ord('A')+y):
        char += ('   '+chr(i))
    print('  '+char)


def get_rows(playground: PlayG) -> PlayG:
    lst = playground
    return [[col for col in row] for row in lst]


def get_cols(playground: PlayG) -> PlayG:
    lst = playground
    return(list(map(list, zip(*lst))))


def get_diagonals(playground: PlayG, rvrsd: bool) -> PlayG:
    comeback = []
    lst = playground
    buf = ['#'] * (len(lst) - 1)

    if not rvrsd:
        comeback += [(buf[i:] + row + buf[:i])
                     for i, row in enumerate(get_rows(lst))]
    else:
        comeback += [(buf[:i] + row + buf[i:])
                     for i, row in enumerate(get_rows(lst))]

    return [[col for col in row if col != '#'] for row in get_cols(comeback)]


def who_won(playground: PlayG) -> Optional[str]:
    length_to_win = 5
    elem5count = 0
    strings = []
    elems5 = []
    all_dimensions = []
    zero_flag = 0

    all_dimensions += get_diagonals(playground, False) + \
        get_cols(playground) + \
        get_rows(playground) + \
        get_diagonals(playground, True)

    for elem in all_dimensions:
        fst = elem[0]
        for e in elem[1:]:
            if (e != fst[-1]):
                strings.append(fst)
                fst = e
            else:
                fst = fst + e
        strings.append(fst)

    for elem2 in strings:
        if elem2.count(" ") > 0:
            zero_flag += 1
        elif len(elem2) == length_to_win:
            elem5count += 1
            elems5.append(elem2)

    # nobody won and there is space
    if elem5count == 0 and zero_flag > 0:
        return None

    # somebody won
    elif elem5count > 0:
        check = True
        hah = elems5[0][0]
        for ele in elems5:
            if hah != ele[0]:
                check = False

        if check:
            return hah
        else:
            return 'invalid'

    # nobody won out of space
    elif zero_flag == 0 and elem5count == 0:
        return 'tie'
    assert False


def strategy(playground: PlayG, symbol: str) -> Tuple[int, int]:
    play = playground
    empty = []
    tupl: Tuple[int, int] = (-1, -1)

    if who_won(play) != symbol:
        for x in range(0, len(play)):

            for y in range(0, len(play[0])):
                if play[x][y] == ' ':
                    empty.append((x, y))

        for elem in empty:
            put(play, elem[0], elem[1], symbol)
            if who_won(play) == symbol:
                tupl = (elem)
                put_empty(play, elem[0], elem[1], " ")
                break
            else:
                put_empty(play, elem[0], elem[1], " ")

    if tupl == (-1, -1):
        if empty != []:
            a = choice(empty)
            return a
    return tupl


def game(height: int, width: int) -> None:
    print("Welcome to:")
    print(r"""
      ___          ___          ___          ___          ___          ___
     /\  \        /\  \        /\__\        /\  \        /\__\        /\__\
    /::\  \      /::\  \      /::|  |      /::\  \      /:/  /       /:/  /
   /:/\:\  \    /:/\:\  \    /:|:|  |     /:/\:\  \    /:/__/       /:/  /
  /:/  \:\  \  /:/  \:\  \  /:/|:|__|__  /:/  \:\  \  /::\__\____  /:/  /  ___
 /:/__/_\:\__\/:/__/ \:\__\/:/ |::::\__\/:/__/ \:\__\/:/\:::::\__\/:/__/  /\__\
 \:\  /\ \/__/\:\  \ /:/  /\/__/~~/:/  /\:\  \ /:/  /\/_|:|~~|~   \:\  \ /:/  /
  \:\ \:\__\   \:\  /:/  /       /:/  /  \:\  /:/  /    |:|  |     \:\  /:/  /
   \:\/:/  /    \:\/:/  /       /:/  /    \:\/:/  /     |:|  |      \:\/:/  /
    \::/  /      \::/  /       /:/  /      \::/  /      |:|  |       \::/  /
     \/__/        \/__/        \/__/        \/__/        \|__|        \/__/
    """)
    playground = new_playground(height, width)

    symboll = False
    while not symboll:
        symbol = input("Type X or O to choose your symbol   ")
        if symbol == 'X' or symbol == 'O':
            print('symbol chosen!', symbol)
            symboll = True
        else:
            print('invalid symbol!')

    if symbol == 'X':
        robot = 'O'
    else:
        robot = 'X'

    order = False
    while not order:
        who_when = input("Do you want to go first? type yes/no ")
        if who_when == 'yes':
            print('You go first')
            order = True
        if who_when == 'no':
            print('You go second')
            order = True
        if who_when != 'yes' and who_when != 'no':
            print('invalid decision')

    if who_when == 'yes':
        while who_won(playground) is None:
            player(playground, symbol, height, width)
            if who_won(playground) == symbol:
                print('Game was won by: ', symbol)
                break

            for i in reversed(range(1, 4)):
                # sleep(1)
                print("%s\r" % i)

            computer(playground, robot)
            if who_won(playground) == robot:
                print('Game was won by: ', robot)
                break
    if who_when == 'no':
        while who_won(playground) is None:
            computer(playground, robot)
            if who_won(playground) == robot:
                print('Game was won by: ', robot)
                break

            for i in reversed(range(1, 4)):
                # sleep(1)
                print("%s\r" % i)

            player(playground, symbol, height, width)
            if who_won(playground) == symbol:
                print('Game was won by: ', symbol)
                break


def player(playground: PlayG, symbol: str, height: int, width: int) -> None:

    print(r"""Please input the coordinates in format: row column
where both are numbers for example: 1,1""")

    val = input("Type your coordinates: ").split(',')
    while len(val) != 2 \
            or not val[0].isdecimal() or not val[1].isdecimal() \
            or int(val[0])+1 > height or int(val[1])+1 > width \
            or not put(playground, int(val[0]), int(val[1]), symbol):
        print(r"""Coordinates already in use or out of range
or not decimals or invalid format!""")
        val = input("Type your coordinates: ").split(',')
    put(playground, int(val[0]), int(val[1]), symbol)
    draw(playground)


def computer(playground: PlayG, robot: str) -> None:
    comp = (strategy(playground, robot))
    put(playground, comp[0], comp[1], robot)
    draw(playground)


if __name__ == '__main__':
    # write your own tests here
    playground = new_playground(6, 7)

    '''m = [(0, 0), (0, 1), (0, 2),
         (0, 4), (0, 5), (1, 3), (2, 0), (2, 1), (2,5),
         (3, 2), (3, 3), (3, 6), (4, 0),
         (4, 1), (4, 4), (4, 5), (5, 0), (5, 1), (5, 4), (5, 6)]
    n = [(0,3), (1, 0), (1, 1), (1, 2), (1, 4), (1, 5),
    (1, 6), (2, 2), (2, 3), (2, 4), (2,6),
        (3, 0), (3, 1), (3, 4), (3, 5), (4, 2),
        (4, 3), (4, 6), (5, 2), (5, 3), (5, 5)]'''

    '''for elem in m:
        # print(elem[0])
        put(playground, elem[0], elem[1], 'X')
    for elem in n:
        put(playground, elem[0], elem[1], 'O')'''

    # get_cols(playground)
    # draw(playground)
    # print(playground)
    # dataset(playground)
    # who_won(playground)
    # strategy(playground, 'O')
    # draw(playground)
    # game(10, 10)
