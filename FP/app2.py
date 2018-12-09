def get_connection():
    return mc.connect(user='root',
    password='Michelle1107',
    host='127.0.0.1',
    database='candystore',
    auth_plugin='mysql_native_password')

@app.route('/process',methods=['POST'])
def process_order():
    qty = request.form['qty']
    currency = request.form['itemorder']
    symbolID= request.form['symbolID']
    price = request.form['price']
    connection = get_connection()
    sql_trade = 'insert into Trade (symbolID,quantity,price) values ('+symbolID+','+qty+','+price+')'
    result = connection.cmd_query(sql)
    connection.commit()
    connection.close()
    return "Order processed"

@app.route('/history')
def view_orders():
    connection = get_connection()
    sql = "select * from trade"
    result = connection.cmd_query(sql)
    rows = connection.get_rows()
    connection.close()
    return render_template('history.html',orders=rows[0])






    sql_marketprice = """ select last_price from currency where currency_id = %s
                """
    sql_vwap = """select vwap from pl where symbolID = %s
                    """ 
    sql_rpl = """select UPL from PL where RPL= (
                """
    sql_PL = """insert into PL (PLID,symbolID,price,quantity,UPL,RPL)
               values(%s,%s,%s,%s,100000,%s)    """  

    sql_new_vwap = """ select sum(price*quanlity)/sum(quantity) from trade
                    where symbolID = %s
                    """
    sql_update = """ update PL set quantity = quantity + %s,vwap = %s
                    SymbolID = %s
                  """             
    sql_vwap = 'insert into PL (vwap) values ()'