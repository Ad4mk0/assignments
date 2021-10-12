from typing import List, Set, Dict, Optional


class Transaction:
    def __init__(self, buyer_id: str, seller_id: str, amount: int, price: int):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.amount = amount
        self.price = price


class Order:
    def __init__(self, trader_id: str, amount: int, price: int):
        self.trader_id = trader_id
        self.amount = amount
        self.price = price


class Stock:
    def __init__(self) -> None:
        self.history: List[Transaction] = []
        self.buyers: List[Order] = []
        self.sellers: List[Order] = []


StockExchange = Dict[str, Stock]


def add_new_stock(stock_exchange: StockExchange, ticker_symbol: str) -> bool:
    if ticker_symbol in stock_exchange:
        return False
    stock_exchange[ticker_symbol] = Stock()
    return True


def place_buy_order(stock_exchange: StockExchange,
                    ticker_symbol: str,
                    trader_id: str,
                    amount: int, price: int) -> None:
    execute_order(stock_exchange, ticker_symbol,
                  trader_id, amount, price, True)


def place_sell_order(stock_exchange: StockExchange,
                     ticker_symbol: str,
                     trader_id: str,
                     amount: int, price: int) -> None:
    execute_order(stock_exchange, ticker_symbol,
                  trader_id, amount, price, False)


def execute_order(stock_exchange: StockExchange,
                  ticker_symbol: str,
                  trader_id: str,
                  amount: int,
                  price: int, sell: bool) -> None:
    new_order = Order(trader_id, amount, price)
    index = 0
    while condition(stock_exchange, ticker_symbol, price, sell, index):
        index += 1
    if sell:
        stock_exchange[ticker_symbol].buyers.insert(
            index, new_order)
    else:
        stock_exchange[ticker_symbol].sellers.insert(
            index, new_order)

    settle(stock_exchange, ticker_symbol, trader_id, amount, price)


def condition(stock_exchange: StockExchange,
              ticker_symbol: str, price: int, sell: bool, index: int) -> bool:
    list_buyers = stock_exchange[ticker_symbol].buyers
    list_sellers = stock_exchange[ticker_symbol].sellers
    if sell:
        return (index < len(list_buyers) and
                price > list_buyers[index].price)
    else:
        return (index < len(list_sellers) and
                price < list_sellers[index].price)


def settle(stock_exchange: StockExchange, ticker_symbol: str,
           trader_id: str, amount: int, price: int) -> None:
    for ticker_symbol in stock_exchange:
        list_sellers = stock_exchange[ticker_symbol].sellers
        list_buyers = stock_exchange[ticker_symbol].buyers
        while list_sellers and list_buyers \
                and list_sellers[-1].price <= list_buyers[-1].price:

            last_seller = list_sellers[-1]
            last_buyer = list_buyers[-1]

            if last_seller.amount == last_buyer.amount:
                amount_ = last_buyer.amount
                list_sellers.pop(-1)
                list_buyers.pop(-1)

            elif last_seller.amount > last_buyer.amount:
                last_seller.amount = last_seller.amount - last_buyer.amount
                amount_ = last_buyer.amount
                list_buyers.pop(-1)

            elif last_seller.amount < last_buyer.amount:
                last_buyer.amount = last_buyer.amount - last_seller.amount
                amount_ = last_seller.amount
                list_sellers.pop(-1)

            stock_exchange[ticker_symbol].history.append(
                Transaction(last_buyer.trader_id,
                            last_seller.trader_id,
                            amount_,
                            last_seller.price))


def stock_owned(stock_exchange: StockExchange,
                trader_id: str) -> Dict[str, int]:
    owned = dict()

    for symbol in stock_exchange:
        counter = 0
        for elem in stock_exchange[symbol].history:
            ticker = symbol
            if elem.seller_id == trader_id:
                counter -= (elem.amount)

            if elem.buyer_id == trader_id:
                counter += (elem.amount)

        if counter != 0:
            owned[ticker] = counter
    return owned


def all_traders(stock_exchange: StockExchange) -> Set[str]:
    traders = set()
    for symbol in stock_exchange:
        for x in range(len(stock_exchange[symbol].buyers)):
            traders.add(stock_exchange[symbol].buyers[x].trader_id)
        for x in range(len(stock_exchange[symbol].sellers)):
            traders.add(stock_exchange[symbol].sellers[x].trader_id)
        for x in range(len(stock_exchange[symbol].history)):
            traders.add(stock_exchange[symbol].history[x].buyer_id)
            traders.add(stock_exchange[symbol].history[x].seller_id)
    return traders


def transactions_by_amount(stock_exchange: StockExchange,
                           ticker_symbol: str) -> List[Transaction]:
    history = stock_exchange[ticker_symbol].history
    sorted_history = sorted(history, key=lambda x: x.amount, reverse=True)
    return sorted_history


def process_batch_commands(stock_exchange: StockExchange,
                           commands: List[str]) -> Optional[int]:
    index = 0
    for com in commands:
        index += 1
        splited = com.split(' ')
        if "ADD" in splited and len(splited) == 2:
            if "ADD" in splited[0]:
                if add_new_stock(stock_exchange, splited[1]) is False:
                    return index-1
            else:
                return index-1
        elif valider(com, stock_exchange, commands):
            name_postfix = com.split(':', 1)
            splited = name_postfix[1].split(' ')

            name = name_postfix[0]
            order_type = splited[1]
            amount = int(splited[2])
            ticker = splited[3]
            price = int(splited[5])
            if order_type == "BUY":
                place_buy_order(stock_exchange, ticker, name, amount, price)
            if order_type == "SELL":
                place_sell_order(stock_exchange, ticker, name, amount, price)
        else:
            return index-1
    return None


def valider(com: str, stock_exchange: StockExchange,
            commands: List[str]) -> bool:
    # retrns True if batch format of sell/buy order is valid
    separator_count = 5
    # checks for ':' occurence
    if com.count(':') > 2:
        return False

    name = com.split(':', 1)[0]
    postfix = com.split(':', 1)[1]
    # checks for unempty name
    if name == '':
        return False

    # checks for number of separators (5)
    if postfix.count(' ') != separator_count:
        return False
    splited = postfix.split(' ')

    # check if order type(BUY/SELL) is valid str
    order_type = splited[1]
    if "BUY" != order_type and "SELL" != order_type:
        return False

    amount = splited[2]
    # checks if amount is positive integer
    if amount.isdigit() is False or int(amount) <= 0:
        return False

    # checks if ticker symbol is on exchange
    ticker = splited[3]
    if ticker not in stock_exchange:
        return False
    # checks for "AT"
    at = splited[4]
    if at != "AT":
        return False

    price = splited[5]
    # checks if price is positive integer
    if price.isdigit() is False or int(price) <= 0:
        return False
    return True


def print_stock(stock_exchange: StockExchange, ticker_symbol: str) -> None:
    assert ticker_symbol in stock_exchange

    stock = stock_exchange[ticker_symbol]
    print(f"=== {ticker_symbol} ===")
    print("     price amount  trader")
    print("  -------------------------------------------------------------")

    for order in stock.sellers:
        print(f"    {order.price:6d} {order.amount:6d} ({order.trader_id})")
    print("  -------------------------------------------------------------")

    for order in reversed(stock.buyers):
        print(f"    {order.price:6d} {order.amount:6d} ({order.trader_id})")
    print("  -------------------------------------------------------------")

    for transaction in stock.history:
        print(f"    {transaction.seller_id} -> {transaction.buyer_id}: "
              f"{transaction.amount} at {transaction.price}")


def check_order(order: Order, trader_id: str, amount: int, price: int) -> None:
    assert order.trader_id == trader_id
    assert order.amount == amount
    assert order.price == price


def check_transaction(transaction: Transaction, buyer_id: str, seller_id: str,
                      amount: int, price: int) -> None:
    assert transaction.buyer_id == buyer_id
    assert transaction.seller_id == seller_id
    assert transaction.amount == amount
    assert transaction.price == price


def test_scenario1() -> None:
    duckburg_se: StockExchange = {}
    add_new_stock(duckburg_se, 'ACME')
    # print_stock(duckburg_se, 'ACME')

    place_sell_order(duckburg_se, 'ACME', 'Strýček Skrblík', 50, 120)

    place_buy_order(duckburg_se, 'ACME', 'Rampa McKvák', 100, 90)
    place_sell_order(duckburg_se, 'ACME', 'Hamoun Držgrešle', 70, 110)
    place_sell_order(duckburg_se, 'ACME', 'Kačer Donald', 20, 120)

    acme = duckburg_se['ACME']
    assert acme.history == []
    print_stock(duckburg_se, 'ACME')
    assert len(acme.buyers) == 1
    check_order(acme.buyers[0], 'Rampa McKvák', 100, 90)

    assert len(acme.sellers) == 3
    check_order(acme.sellers[0], 'Kačer Donald', 20, 120)
    check_order(acme.sellers[1], 'Strýček Skrblík', 50, 120)
    check_order(acme.sellers[2], 'Hamoun Držgrešle', 70, 110)

    place_buy_order(duckburg_se, 'ACME', 'Paní Čvachtová', 90, 110)

    assert len(acme.history) == 1
    check_transaction(acme.history[0], 'Paní Čvachtová', 'Hamoun Držgrešle',
                      70, 110)

    assert len(acme.buyers) == 2
    check_order(acme.buyers[0], 'Rampa McKvák', 100, 90)
    check_order(acme.buyers[1], 'Paní Čvachtová', 20, 110)

    assert len(acme.sellers) == 2
    check_order(acme.sellers[0], 'Kačer Donald', 20, 120)
    check_order(acme.sellers[1], 'Strýček Skrblík', 50, 120)

    place_buy_order(duckburg_se, 'ACME', 'Magika von Čáry', 60, 130)
    print_stock(duckburg_se, 'ACME')

    assert len(acme.history) == 3
    check_transaction(acme.history[0], 'Paní Čvachtová', 'Hamoun Držgrešle',
                      70, 110)
    check_transaction(acme.history[1], 'Magika von Čáry', 'Strýček Skrblík',
                      50, 120)
    check_transaction(acme.history[2], 'Magika von Čáry', 'Kačer Donald',
                      10, 120)

    assert len(acme.buyers) == 2
    check_order(acme.buyers[0], 'Rampa McKvák', 100, 90)
    check_order(acme.buyers[1], 'Paní Čvachtová', 20, 110)

    assert len(acme.sellers) == 1
    check_order(acme.sellers[0], 'Kačer Donald', 10, 120)

    # stock_owned(duckburg_se,'Kačer Donald')

    all_traders(duckburg_se)
    # transactions_by_amount(duckburg_se,'ACME')
    all_transactions = transactions_by_amount(duckburg_se, 'ACME')
    check_transaction(all_transactions[0],
                      'Paní Čvachtová', 'Hamoun Držgrešle',
                      70, 110)
    check_transaction(all_transactions[1],
                      'Magika von Čáry', 'Strýček Skrblík',
                      50, 120)
    check_transaction(all_transactions[2],
                      'Magika von Čáry', 'Kačer Donald',
                      10, 120)
    assert all_traders(duckburg_se) == {
        'Kačer Donald',
        'Strýček Skrblík',
        'Hamoun Držgrešle',
        'Paní Čvachtová',
        'Magika von Čáry',
        'Rampa McKvák', }

    for name, amount in [
            ('Kačer Donald', -10),
            ('Strýček Skrblík', -50),
            ('Hamoun Držgrešle', -70),
            ('Paní Čvachtová', 70),
            ('Magika von Čáry', 60),
    ]:
        assert stock_owned(duckburg_se, name) == {'ACME': amount}

    assert stock_owned(duckburg_se, 'Rampa McKvák') == {}
    assert stock_owned(duckburg_se, 'Šikula') == {}


def test_scenario2() -> None:
    duckburg_se: StockExchange = {}
    result = process_batch_commands(duckburg_se, [
        "ADD ACME",
        "Uncle Scrooge: SELL 50 ACME AT 120",
        "Launchpad McQuack: BUY 100 ACME AT 90",
        "Flintheart Glomgold: SELL 70 ACME AT 110",
        "Donald Duck: SELL 20 ACME AT 120",
        "Mrs. Beakley: BUY 90 ACME AT 110",
        "Magica De Spell: BUY 60 ACME AT 130",

    ])
    print_stock(duckburg_se, 'ACME')

    assert result is None
    assert 'ACME' in duckburg_se
    acme = duckburg_se['ACME']
    assert len(acme.history) == 3
    check_transaction(acme.history[0], 'Mrs. Beakley', 'Flintheart Glomgold',
                      70, 110)
    check_transaction(acme.history[1], 'Magica De Spell', 'Uncle Scrooge',
                      50, 120)
    check_transaction(acme.history[2], 'Magica De Spell', 'Donald Duck',
                      10, 120)

    assert len(acme.buyers) == 2
    check_order(acme.buyers[0], 'Launchpad McQuack', 100, 90)
    check_order(acme.buyers[1], 'Mrs. Beakley', 20, 110)

    assert len(acme.sellers) == 1
    check_order(acme.sellers[0], 'Donald Duck', 10, 120)


def test_scenario3() -> None:
    nnyse: StockExchange = {}
    result = process_batch_commands(nnyse, [
        "ADD Momcorp",
        "Mom: SELL 1000 Momcorp AT 5000",
        "Walt: BUY 10 Momcorp AT 5600",
        "Larry: BUY 7 Momcorp AT 5000",
        "Igner: BUY 1 Momcorp AT 4000",
        "ADD PlanetExpress",
        "Mom: BUY 1000 PlanetExpress AT 100",
        "Zoidberg: BUY 1000 PlanetExpress AT 199",
        "Professor Farnsworth: SELL 1020 PlanetExpress AT 100",
        "Bender B. Rodriguez: BUY 20 Momcorp AT 100",
        "Fry: INVALID COMMAND",
        "Leela: BUY 500 PlanetExpress AT 150",

    ])

    assert result == 10

    assert set(nnyse) == {'Momcorp', 'PlanetExpress'}

    momcorp = nnyse['Momcorp']
    pe = nnyse['PlanetExpress']

    assert len(momcorp.history) == 2
    check_transaction(momcorp.history[0], 'Walt', 'Mom', 10, 5000)
    check_transaction(momcorp.history[1], 'Larry', 'Mom', 7, 5000)

    assert len(momcorp.sellers) == 1
    check_order(momcorp.sellers[0], 'Mom', 983, 5000)

    assert len(momcorp.buyers) == 2
    check_order(momcorp.buyers[0], 'Bender B. Rodriguez', 20, 100)
    check_order(momcorp.buyers[1], 'Igner', 1, 4000)
    print_stock(nnyse, 'PlanetExpress')

    assert len(pe.history) == 2
    check_transaction(pe.history[0], 'Zoidberg', 'Professor Farnsworth',
                      1000, 100)
    check_transaction(pe.history[1], 'Mom', 'Professor Farnsworth',
                      20, 100)

    assert pe.sellers == []
    assert len(pe.buyers) == 1
    check_order(pe.buyers[0], 'Mom', 980, 100)


def test_scenario4() -> None:
    se: StockExchange = {}
    add_new_stock(se, 'ACME')
    place_buy_order(se, 'ACME', 'Strýček Skrblík', 1, 1)
    place_sell_order(se, 'ACME', 'Kačer Donald', 1, 1)
    print_stock(se, 'ACME')


def test_scenario5() -> None:
    se: StockExchange = {}
    add_new_stock(se, 'ACME')
    place_buy_order(se, 'ACME', 'Strýček Skrblík', 1, 1)
    place_buy_order(se, 'ACME', 'Kačer Donald', 1, 1)
    place_buy_order(se, 'ACME', 'Karol', 1, 1)
    place_buy_order(se, 'ACME', 'Karoll', 1, 1)
    place_buy_order(se, 'ACME', 'Karol', 1, 20)
    place_sell_order(se, 'ACME', 'Kačerald', 100, 100)
    place_sell_order(se, 'ACME', 'Kačerald', 100, 130)
    place_sell_order(se, 'ACME', 'Geralt', 90, 100)
    place_sell_order(se, 'ACME', 'Visenna', 90, 100)
    print_stock(se, 'ACME')


def test_scenario6() -> None:
    se: StockExchange = {}
    add_new_stock(se, 'ACME')
    place_buy_order(se, 'ACME', 'Strycek', 1, 1)
    place_buy_order(se, 'ACME', 'Stryce', 1, 1)
    place_buy_order(se, 'ACME', 'Strycek', 1, 1)
    place_buy_order(se, 'ACME', 'Haluzar', 1, 100)
    place_buy_order(se, 'ACME', 'Stryc', 1, 1)
    place_buy_order(se, 'ACME', 'Kacer', 1, 1)

    place_sell_order(se, 'ACME', 'Kačeralt', 100, 100)
    place_sell_order(se, 'ACME', 'Kačerald', 100, 130)
    place_sell_order(se, 'ACME', 'Geralt', 90, 100)
    place_sell_order(se, 'ACME', 'Visenna', 90, 100)

    # place_sell_order(se,'ACME','0',3,1)
    print_stock(se, 'ACME')
    '''print(se["ACME"].history[0].buyer_id)
    print(se["ACME"].history[1].buyer_id)
    print(se["ACME"].history[2].buyer_id)'''


def test_scenario7() -> None:
    se: StockExchange = {}
    add_new_stock(se, 'ACME')
    place_buy_order(se, 'ACME', 'Strycek', 1, 1)
    place_sell_order(se, 'ACME', 'Strycek', 1, 1)
    print_stock(se, 'ACME')
    print(se["ACME"].history[0].buyer_id)


def tiker_fail() -> None:  # fixed stock_owned
    se: StockExchange = {}
    add_new_stock(se, 'ACME')
    add_new_stock(se, '0')
    place_buy_order(se, 'ACME', 'Strýček Skrblík', 1, 1)
    place_buy_order(se, '0', 'Strýček Skrblík', 1, 1)
    place_buy_order(se, 'ACME', 'Strýček Skrblík', 1, 1)
    place_buy_order(se, 'ACME', 'Strýček Skrblík', 1, 1)
    place_buy_order(se, 'ACME', 'Strýček Skrblík', 1, 1)
    # place_sell_order(se, 'ACME', 'Kačer Donald', 1, 1)
    place_sell_order(se, '0', 'Kačer Donald', 1, 1)
    # result = stock_owned(se, 'Strýček Skrblík')
    # stock_owned()
    # print_stock(se,"ACME")
    # print(res)
    # print(mama)
    # print(result)
    # print_stock(se,"0")


def sranda() -> None:
    se: StockExchange = {}
    add_new_stock(se, 'ACME')
    place_buy_order(se, 'ACME', 'Strýček Skrblík', 56, 1)
    place_sell_order(se, 'ACME', 'Strýček Skrblík', 56, 1)
    # place_sell_order(se, 'ACME', 'Strýček Skrblík', 1, 1)
    place_buy_order(se, 'ACME', 'Strýček Skrblík', 3, 1)
    place_sell_order(se, 'ACME', 'Kačer Donald', 3, 1)

    place_buy_order(se, 'ACME', 'Strýček', 5, 1)
    place_sell_order(se, 'ACME', 'Kačer', 5, 1)

    place_buy_order(se, 'ACME', 'mama', 3, 1)
    place_sell_order(se, 'ACME', 'ele', 3, 1)
    print_stock(se, 'ACME')
    all_transactions = transactions_by_amount(se, 'ACME')
    # print(len(all_transactions))

    check_transaction(all_transactions[0],
                      'Strýček Skrblík', 'Strýček Skrblík',
                      56, 1)
    check_transaction(all_transactions[2],
                      'Strýček Skrblík', 'Kačer Donald',
                      3, 1)
    check_transaction(all_transactions[1],
                      'Strýček', 'Kačer',
                      5, 1)
    check_transaction(all_transactions[3],
                      'mama', 'ele',
                      3, 1)


def batches() -> None:
    nnyse: StockExchange = {}
    result = process_batch_commands(nnyse, [
        "ADD Mom:corp",
        'ADD ADD',
        'ADD BUY',
        "ADD SELL",


        " : SELL 1000 Mom:corp AT 5000",
        "Walt: BUY 10 ADD AT 5600",
        "Larry: BUY 7 Mom:corp AT 5000",

        "ADD Momcorp: BUY 1 Mom:corp AT 4000",
        " : BUY 1 Mom:corp AT 1",
        "ADD: BUY 10 SELL AT 10",
        'Bender B. Rodriguez: BUY 10 ACME',
        "ADD ADD: SELL 10 SELL AT 50",
    ])
    # print_stock(nnyse, "SELL")
    print(result)


def nove() -> None:
    se: StockExchange = {}
    add_new_stock(se, 'ACME')
    mam = process_batch_commands(se, [
        'AI::StockBot: BUY 10 ACME AT 10',
    ])
    print(mam)


if __name__ == '__main__':
    test_scenario1()
    test_scenario2()
    test_scenario3()
    test_scenario4()
    test_scenario5()
    test_scenario6()
    test_scenario7()
    tiker_fail()
    sranda()
    # nove()
    # batches()
