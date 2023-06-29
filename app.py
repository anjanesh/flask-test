from flask import Flask, render_template, request, session, flash, redirect
from flask_mysqldb import MySQL
import yaml, os

import importlib

app = Flask(__name__)

with open('db.yaml', 'r') as file:
    db = yaml.load(file, Loader=yaml.SafeLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_PORT'] = db['mysql_port']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    data = {}
    data['users'] = []
    return render_template('index.html', data = data)

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/product/list')
def product_list():
    data = {}
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM `Product`;")
    if result_value > 0:
        data['products'] = cur.fetchall()
    return render_template('product_list.html', data = data)

@app.route('/product/view/<pid>')
def product_view(pid):
    data = {}
    data['pid'] = pid
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `Product` WHERE `product_id` = %s;", [pid])
    data['count'] = cur.rowcount
    if cur.rowcount == 0:
        flash("No such product id")
    else:
        row = cur.fetchone()
        if row is not None:
            data['name'] = row['name']
            data['Location'] = data_movement(pid, 'Location')
            print("data['Location'] = ", data['Location'])

    return render_template('product_view.html', data = data)

@app.route('/product/add', methods = ['GET', 'POST'])
def product_add():
    if request.method == 'POST':
        try:
            if "name" in request.form:
                name = request.form['name']
                if name:
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO `Product` (`product_id`, `name`) VALUES (NULL, %s); ", [name])
                    mysql.connection.commit()
                    flash("Successfully added product", "success")
                    return redirect(("/product/view/%s" % (cur.lastrowid)), code=302) # This is to disable refresh
                else:
                    flash("Product name cannot be empty")
            else:
                return "No hacking !"
        except Exception as e:
            flash("Error : {}".format(e), "danger")

    return render_template('product_add.html')

@app.route('/product/edit/<pid>', methods = ['GET', 'POST'])
def product_edit(pid):
    data = {}
    data['pid'] = pid
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        try:
            if "name" in request.form:
                name = request.form['name']
                if name:
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE `Product` SET `name` = '%s' WHERE `product_id` = %s;" % (name, pid))
                    mysql.connection.commit()
                    data['name'] = name
                    flash("Successfully updated product", "success")
                else:
                    flash("Product name cannot be empty")
            else:
                return "No hacking !"
        except Exception as e:
            flash("Error : {}".format(e), "danger")
            # print("UPDATE `Product` SET `name` = '%s' WHERE `product_id` = %s);" % (name, pid))
    else:
        cur.execute("SELECT * FROM `Product` WHERE `product_id` = %s;", [pid])
        data['count'] = cur.rowcount
        if cur.rowcount == 0:
            flash("No such product id")
        else:
            row = cur.fetchone()
            if row is not None:
                data['name'] = row['name']


    return render_template('product_edit.html', data = data)

# Location
@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/location/list')
def location_list():
    data = {}
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM `Location`;")
    if result_value > 0:
        data['locations'] = cur.fetchall()
    return render_template('location_list.html', data = data)

@app.route('/location/view/<lid>')
def location_view(lid):
    data = {}
    data['lid'] = lid
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `Location` WHERE `location_id` = %s;", [lid])
    data['count'] = cur.rowcount
    if cur.rowcount == 0:
        flash("No such location id")
    else:
        row = cur.fetchone()
        if row is not None:
            data['name'] = row['name']

            sql = """
            SELECT pm.`from_location`, pm.`to_location`, pm.`product_id`, pm.`qty`,
            (SELECT `name` FROM Product p WHERE p.`product_id` = pm.`product_id`) AS `product_name`
            FROM `ProductMovement` pm
            WHERE
            pm.`from_location` = %s OR
            pm.`to_location` = %s
            """ % (lid, lid)
            cur.execute(sql)
            pm_rows = cur.fetchall()
            data["Product"] = dict()

            for pm_row in pm_rows:

                if pm_row['from_location'] == int(lid):
                    print("Same")
                    if pm_row['product_name'] not in data["Product"]:
                        data["Product"][pm_row['product_name']] = 0
                    data["Product"][pm_row['product_name']] -= pm_row['qty']

                if pm_row['to_location'] == int(lid):
                    if pm_row['product_name'] not in data["Product"]:
                        data["Product"][pm_row['product_name']] = 0
                    data["Product"][pm_row['product_name']] += pm_row['qty']

    return render_template('location_view.html', data = data)

@app.route('/location/add', methods = ['GET', 'POST'])
def location_add():
    if request.method == 'POST':
        try:
            if "name" in request.form:
                name = request.form['name']
                if name:
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO `Location` (`location_id`, `name`) VALUES (NULL, %s); ", [name])
                    mysql.connection.commit()
                    flash("Successfully added product", "success")
                    return redirect(("/location/view/%s" % (cur.lastrowid)), code=302) # This is to disable refresh
                else:
                    flash("Location name cannot be empty")
            else:
                return "No hacking !"
        except Exception as e:
            flash("Error : {}".format(e), "danger")

    return render_template('location_add.html')

@app.route('/location/edit/<pid>', methods = ['GET', 'POST'])
def location_edit(pid):
    data = {}
    data['pid'] = pid
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        try:
            if "name" in request.form:
                name = request.form['name']
                if name:
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE `Location` SET `name` = '%s' WHERE `location_id` = %s;" % (name, pid))
                    mysql.connection.commit()
                    data['name'] = name
                    flash("Successfully updated location", "success")
                else:
                    flash("Product name cannot be empty")
            else:
                return "No hacking !"
        except Exception as e:
            flash("Error : {}".format(e), "danger")
    else:
        cur.execute("SELECT * FROM `Location` WHERE `location_id` = %s;", [pid])
        data['count'] = cur.rowcount
        if cur.rowcount == 0:
            flash("No such location id")
        else:
            row = cur.fetchone()
            if row is not None:
                data['name'] = row['name']

    return render_template('location_edit.html', data = data)

# Movement
@app.route('/move')
def move():
    return render_template('move.html')

@app.route('/move/list')
def move_list():
    data = {}
    cur = mysql.connection.cursor()
    sql = """
    SELECT
    pm.movement_id, pm.timestamp, pm.qty,
    (SELECT name FROM Product p where pm.product_id = p.product_id) as name,
    (SELECT name FROM Location l where pm.from_location = l.location_id) as from_location,
    (SELECT name FROM Location l where pm.to_location = l.location_id) as to_location
    FROM `ProductMovement` pm
    """
    result_value = cur.execute(sql)
    if result_value > 0:
        data['movements'] = cur.fetchall()
    return render_template('move_list.html', data = data)

@app.route('/move/push', methods = ['GET', 'POST'])
def move_push():
    data = {}
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        try:
            """
            TODO : Check for existence of POST variables

            PHP :
            if (count(array_diff(['product_id', 'location_id', 'qty']], array_keys($_POST))) == 0)
                return TRUE;

            Python : Something like this
            https://www.php2python.com/wiki/function.array-diff/
            if len([item for item in ['product_id', 'location_id', 'qty'] if item not in request.form]):
                return "No Hacking"
            """
            product_id = request.form['product_id']
            location_id = request.form['location_id']
            qty = request.form['qty']

            sql = """
            INSERT INTO `ProductMovement` SET
            `timestamp` = NOW(),
            `from_location` = 0,
            `to_location` = %s,
             `product_id` = %s,
             `qty` = %s
            """ % (location_id, product_id, qty)
            cur.execute(sql)
            mysql.connection.commit()
            flash("Successfully added product to location", "success")
            return redirect("/move/list", code=302) # This is to disable refresh
        except Exception as e:
            flash("Error : {}".format(e), "danger")
    else:
        cur.execute("SELECT * FROM `Product`")
        if cur.rowcount == 0:
            return "No Products yet"
        else:
            row = cur.fetchall()
            data['products'] = row

        cur.execute("SELECT * FROM `Location`")
        if cur.rowcount == 0:
            return "No Locations yet"
        else:
            row = cur.fetchall()
            data['locations'] = row


    return render_template('move_push.html', data = data)

@app.route('/move/pop', methods = ['GET', 'POST'])
def move_pop():
    data = {}
    cur = mysql.connection.cursor()
    return render_template('move_pop.html', data = data)

@app.route('/move/move', methods = ['GET', 'POST'])
def move_move():
    data = {}
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        try:
            product_id = request.form['product_id']
            from_location_id = request.form['from_location_id']
            to_location_id = request.form['to_location_id']
            qty = request.form['qty']

            sql = """
            SELECT pm.`from_location`, pm.`to_location`, pm.`qty`
            FROM `ProductMovement` pm
            WHERE pm.`product_id` = %s AND pm.`to_location` = %s
            """ % (product_id, from_location_id) # From Vashi to Seawoods, need to look how many products are there in Vashi (from_location_id)
            cur.execute(sql)
            pm_rows = cur.fetchall()
            data["Product_in_Location"] = 0

            for pm_row in pm_rows:

                print("Location : %s", data["Product_in_Location"])

                if pm_row['from_location'] != 0:
                    data["Product_in_Location"] -= pm_row['qty']

                if pm_row['to_location'] != 0:
                    data["Product_in_Location"] += pm_row['qty']

            print("Product ID %s left in location %s = %s" % (product_id, to_location_id, data["Product_in_Location"]))
            if data["Product_in_Location"] <= 0:
                return "No Products in Location"

            sql = """
            INSERT INTO `ProductMovement` SET
            `timestamp` = NOW(),
            `from_location` = %s,
            `to_location` = %s,
             `product_id` = %s,
             `qty` = %s
            """ % (from_location_id, to_location_id, product_id, qty)
            cur.execute(sql)
            mysql.connection.commit()
            flash("Successfully moved product to location", "success")
            return redirect("/move/list", code=302) # This is to disable refresh
        except Exception as e:
            flash("Error : {}".format(e), "danger")
    else:
        cur.execute("SELECT * FROM `Product`")
        if cur.rowcount == 0:
            return "No Products yet"
        else:
            row = cur.fetchall()
            data['products'] = row

        cur.execute("SELECT * FROM `Location`")
        if cur.rowcount == 0:
            return "No Locations yet"
        else:
            row = cur.fetchall()
            data['locations'] = row

    return render_template('move_move.html', data = data)

@app.route('/balance')
def balance():
    data = {}
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM `Product`;")
    if result_value > 0:
        rows = cur.fetchall()
        for row in rows:            
            data[row['name']] = data_movement(row['product_id'], row['name'])
    return render_template('balance.html', data = data)

def data_movement(product_id, dict_index):
    data = {}
    cur = mysql.connection.cursor()
    
    sql = """
    SELECT pm.`from_location`, pm.`to_location`, pm.`qty`,
    (SELECT `name` FROM Location l WHERE l.`location_id` = pm.`from_location`) AS `from_location_name`,
    (SELECT `name` FROM Location l WHERE l.`location_id` = pm.`to_location`) AS `to_location_name`
    FROM `ProductMovement` pm
    WHERE pm.`product_id` = %s
    """ % (product_id)
    cur.execute(sql)
    pm_rows = cur.fetchall()

    data[dict_index] = dict()

    for pm_row in pm_rows:

        if pm_row['from_location'] != 0:
            if pm_row['from_location_name'] not in data[dict_index]:
                data[dict_index][pm_row['from_location_name']] = 0
            data[dict_index][pm_row['from_location_name']] -= pm_row['qty']

        if pm_row['to_location'] != 0:
            if pm_row['to_location_name'] not in data[dict_index]:
                data[dict_index][pm_row['to_location_name']] = 0
            data[dict_index][pm_row['to_location_name']] += pm_row['qty']

    print("data_movement = ", data)
    print("data_movement[dict_index] = ", data[dict_index])
    
    return data[dict_index]


@app.errorhandler(404)
def page_not_found(e):
    return "This page was not found"

if __name__ == "__main__":
    app.run(debug=True);
