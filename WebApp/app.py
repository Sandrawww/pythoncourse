from flask import Flask, request, render_template, redirect, url_for
from mysql.connector.cursor import MySQLCursor
import mysql.connector as mc
import datetime
import cbpro
app = Flask(__name__)

# Windows: $env:FLASK_DEBUG=1
# Mac: export FLASK_DEBUG=1


@app.route('/signin')
def signin():
    print(request.args.get('u'))
    print(request.args.get('p'))
    if request.args.get('u') != 'farmer' or request.args.get('p') != '123':
        return redirect('/')
    else:
        return redirect('/order')

@app.route("/")
def index():
    fetchCoins()
    return render_template('index.html')

@app.route("/order")
def order():
    return render_template('order.html')


def get_connection():
    return mc.connect(user='root',
    password='',
    host='127.0.0.1',
    database='FinalProject'
    )

@app.route('/process',methods=['POST'])
def process_order():

    print(request.form)

    qty = request.form['Quantity']
    currency = request.form['product'] #btc, eth, ltc
    symbolMap = {
        'btc': 1,
        'eth': 2,
        'ltc': 4
    }
    symbolID= symbolMap[currency]

    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d %H:%M:%S')

    (btc_price, eth_price, ltc_price) = fetchCoins()
    price = 0
    if currency == 'btc':
        price = btc_price
    elif currency == 'eth':
        price = eth_price
    elif currency == 'ltc':
        price = ltc_price

    connection = get_connection()

    # Write this order to Trade table
    sql_trade = "INSERT INTO Trade (SymbolID,Date,Quantity,Price) VALUES ('%s', '%s', '%s', '%s')" % (symbolID, str(date), str(qty), str(price))
    print(sql_trade)
    result = connection.cmd_query(sql_trade)
    connection.commit()


    mycursor = connection.cursor()
    sql_curQuantity = "SELECT SUM(Quantity) FROM Trade WHERE SymbolID = ('%s')" % (symbolID)
    mycursor.execute(sql_curQuantity)
    myresult = mycursor.fetchall()

    for x in myresult:
        curQuantity = float(x[0])
        break


    sql_VWAP = "SELECT VWAP FROM PL WHERE PLID = (SELECT MAX(PLID) FROM PL WHERE SymbolId = '%s')" % (symbolID)
    mycursor.execute(sql_VWAP)
    myresult = mycursor.fetchall()
    for x in myresult:
        lastVWAP = float(x[0])
        break

    top = float(qty) * float(price) + float(curQuantity) * float(lastVWAP)
    bot = float(qty) + float(curQuantity)
    VWAP = top/bot

    UPL = float(price) - VWAP

    RPL = UPL

    a = format(VWAP, '.2f')
    b = format(UPL, '.2f')
    c = format(RPL, '.2f')

    # sql_insert_pl = "INERT INTO PL (SymbolID, Quantity, VWAP, UPL, RPL) VALUES ('%s', '%s', '%s', '%s')" % (symbolID, str(qty), a, b, c)

    sql = "INSERT INTO PL (SymbolID, Quantity, VWAP, UPL, RPL) VALUES (%s, %s, %s, %s, %s)"
    val = (symbolID, str(qty), a, b, c)

    mycursor.execute(sql, val)
    connection.commit()

    connection.close()
    return "Order processed"


def fetchCoins():
    # url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    # raw_response = requests.get(url)
    # print(raw_response.json())

    public_client = cbpro.PublicClient()
    btc_price = public_client.get_product_24hr_stats('BTC-USD')['last']
    eth_price = public_client.get_product_24hr_stats('ETH-USD')['last']
    ltc_price = public_client.get_product_24hr_stats('LTC-USD')['last']
    return (btc_price, eth_price, ltc_price)


'''
def get_products():
    connection = get_connection()
    result = connection.cmd_query("select * from products")
    rows = connection.get_rows()
    connection.close()
    return rows[0]
'''


#view history blotter
@app.route('/history')
def view_orders():
    connection = get_connection()
    sql = "select * from trade"
    result = connection.cmd_query(sql)
    rows = connection.get_rows()
    for row in rows:
        print(row)
    connection.close()
    print("hello")
    return render_template('history.html',orders=rows[0])


#View tracking
@app.route('/tracking')
def view_tracking():
    connection = get_connection()
    sql = "select * from PL"
    result = connection.cmd_query(sql)
    rows = connection.get_rows()
    for row in rows:
        print (row)
    connection.close()
    print("hello")
    return render_template('tracking.html',orders=rows[0])

if __name__ == '__main__':
    app.run(debug=True)
