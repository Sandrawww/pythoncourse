import mysql.connector
from mysql.connector.cursor import MySQLCursor
from drama import dramaticTyping
import datetime
import trade

def trade(currency):

    print trade.get_last_price('coinbase')

    buy_id(1) = trade.trusted_buy('btc', '1', '19500')
    buy_id(2) = trade.trusted_buy('ltc', '1', '37500')
    buy_id(3) = trade.trusted_buy('eth', '1', '11000')
    sell_id(4) = trade.trusted_sell('btc', '1', '19500')
    sell_id(4) = trade.trusted_sell('ltc', '1', '37500')
    sell_id(4) = trade.trusted_sell('eth', '1', '11000')


def fetchBestBidPriceFromDB(currency):
    def get_connection():
    return mc.connect(user='root',
    password='despotSR17',
    host='127.0.0.1',
    database='coinbase',
    auth_plugin='mysql_native_password')
    cursor = connection.cursor()
    query = "SELECT max(bid),timestamp from prices WHERE first_leg='{}' and second_leg='USD' and timestamp> '1520408341.52'".format(currency)
    cursor.execute(query)
    rows = cursor.fetchone()
    return rows[0], rows[1]


def runSimulation(boughtPrice, quantity, currency):
    valueThen = boughtPrice * quantity
    bestPrice, timestamp = fetchBestBidPriceFromDB(currency)
    bestValue = bestPrice * quantity
    priceDifference = (bestValue - valueThen)/float(valueThen) * 100
    time = datetime.datetime.fromtimestamp(timestamp).strftime('%A, %B %-d, %Y %I:%M %p')
    print("The best bid price for {} was ${} at {} \n".format(currency, bestPrice, time))
    if priceDifference>0:
        dramaticTyping("Your total asset value is ${}, it has increase by {}% \n".format(round(bestValue, 4), round(priceDifference,2)))
    else:
        dramaticTyping("Your total asset value is ${}, it has decreased by {} \n".format(round(bestValue, 4), round(priceDifference,2)))