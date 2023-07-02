from flask import Flask, render_template, request, session, flash, redirect
from flask_mysqldb import MySQL
import yaml, os
from flask import g
import importlib
import sqls, helpers

app = Flask(__name__)

yaml_file_path = os.path.join(os.path.dirname(__file__), 'db.yaml')

with open(yaml_file_path, 'r') as file:
    db = yaml.load(file, Loader=yaml.SafeLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_PORT'] = db['mysql_port']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
app.config['SECRET_KEY'] = os.urandom(24)

@app.before_request
def before_request():
    g.db = mysql.connection
    g.cur = g.db.cursor()

@app.route('/')
def index():
    data = {}
    data['users'] = []
    return render_template('index.html', data = data)

# Product
@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/product/list')
def product_list():    
    result_value = g.cur.execute("SELECT * FROM `Product`;")
    if result_value > 0:
        data = {'products': g.cur.fetchall()}        
    return render_template('product_list.html', data=data if data else {})

@app.route('/product/view/<pid>')
def product_view(pid):
    data = { 'pid': pid }
    g.cur.execute("SELECT * FROM `Product` WHERE `product_id` = %s;", [pid])
    data['count'] = g.cur.rowcount
    if g.cur.rowcount == 0:
        flash("No such product id")
    else:
        row = g.cur.fetchone()
        if row is not None:
            data['name'] = row['name']
            data['Location'] = helpers.data_movement(pid, 'Location')            

    return render_template('product_view.html', data = data)

@app.route('/product/add', methods = ['GET', 'POST'])
def product_add():
    if request.method == 'POST':
        helpers.add_edit_product(mysql, crud="add")
    return render_template('product_add.html')

@app.route('/product/edit/<pid>', methods = ['GET', 'POST'])
def product_edit(pid):

    if request.method == 'POST':
        return helpers.product_edit_post(pid)
    else:
        data = helpers.product_edit_get(pid)
        return render_template('product_edit.html', data = data)
    
# Location
@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/location/list')
def location_list():
    data = {}    
    result_value = g.cur.execute("SELECT * FROM `Location`;")
    if result_value > 0:
        data['locations'] = g.cur.fetchall()
    return render_template('location_list.html', data = data)

@app.route('/location/view/<lid>')
def location_view(lid):
    data = { 'lid': lid }    
    
    g.cur.execute("SELECT * FROM `Location` WHERE `location_id` = %s;", [lid])
    data['count'] = g.cur.rowcount
    if g.cur.rowcount == 0:
        flash("No such location id")
    else:
        row = g.cur.fetchone()
        if row is not None:

            data['name'] = row['name']
            g.cur.execute(sqls.ProductMovement % (lid, lid))
            pm_rows = g.cur.fetchall()
            data["Product"] = dict()

            for pm_row in pm_rows:

                if pm_row['from_location'] == int(lid):                    
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
                    g.cur.execute(sqls.location_add, [name])
                    mysql.connection.commit()
                    flash("Successfully added product", "success")
                    return redirect(("/location/view/%s" % (g.cur.lastrowid)), code=302) # This is to disable refresh
                else:
                    flash("Location name cannot be empty")
            else:
                return "No hacking !"
        except Exception as e:
            flash("Error : {}".format(e), "danger")

    return render_template('location_add.html')

@app.route('/location/edit/<pid>', methods = ['GET', 'POST'])
def location_edit(pid):

    if request.method == 'POST':
        return helpers.location_edit_post(pid)
    else:
        data = helpers.location_edit_get(pid)
        return render_template('location_edit.html', data = data)

# Movement
@app.route('/move')
def move():
    return render_template('move.html')

@app.route('/move/list')
def move_list():
    data = {}
    result_value = g.cur.execute(sqls.move_list)
    if result_value > 0:
        data['movements'] = g.cur.fetchall()
    return render_template('move_list.html', data = data)

@app.route('/move/push', methods = ['GET', 'POST'])
def move_push():    
    
    if request.method == 'POST':
        data = helpers.move_push_post(mysql)
    else:
        data = helpers.move_push_get()

    return render_template('move_push.html', data = data)

@app.route('/move/pop', methods = ['GET', 'POST'])
def move_pop():
    data = {}    
    return render_template('move_pop.html', data = data)

@app.route('/move/move', methods = ['GET', 'POST'])
def move_move():    
    if request.method == 'POST':
        data = helpers.move_move_post(mysql)
    else:
        data = helpers.move_move_get()

    return render_template('move_move.html', data = data)

@app.route('/balance')
def balance():
    data = {}
    
    result_value = g.cur.execute("SELECT * FROM `Product`;")
    if result_value > 0:
        rows = g.cur.fetchall()
        for row in rows:            
            data[row['name']] = helpers.data_movement(row['product_id'], row['name'])

    return render_template('balance.html', data = data)

@app.errorhandler(404)
def page_not_found(e):
    return "This page was not found"

if __name__ == "__main__":
    app.run(debug=True);
