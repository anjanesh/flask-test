from flask import request, flash, redirect, g
import sqls

def product_edit_get(pid):
    g.cur.execute("SELECT * FROM `Product` WHERE `product_id` = %s;", [pid])    
    data = { 'pid': pid, 'count': g.cur.rowcount }

    if g.cur.rowcount == 0:
        flash("No such product id")
    else:
        row = g.cur.fetchone()
        if row is not None:
            data['name'] = row['name']

    return data

def product_edit_post(pid):
    return add_edit_product("edit", pid)    

def add_edit_product(mysql, crud="add", pid=0):
    try:
        if "name" in request.form:
            name = request.form['name']
            if name:     
                if crud == "add":
                    g.cur.execute("INSERT INTO `Product` (`product_id`, `name`) VALUES (NULL, %s); ", [name])
                elif crud == "edit":
                    g.cur.execute("UPDATE `Product` SET `name` = '%s' WHERE `product_id` = %s;" % (name, pid))                
                
                mysql.connection.commit()
                flash("Successfully {} product".format("added" if crud == "add" else "updated"), "success")

                return redirect("/product/view/%s" % (g.cur.lastrowid if crud == "add" else pid), code=302) # This is to disable refresh
            else:
                flash("Product name cannot be empty")
        else:
            return "No hacking !"
    except Exception as e:
        flash("Error : {}".format(e), "danger")

    return None

def location_edit_get(pid):
    g.cur.execute("SELECT * FROM `Location` WHERE `location_id` = %s;", [pid])
    data = { 'count': g.cur.rowcount }
    if g.cur.rowcount == 0:
        flash("No such location id")
    else:
        row = g.cur.fetchone()
        if row is not None:
            data['name'] = row['name']
    return data

def location_edit_post(mysql, pid):
    data = {}
    try:
        if "name" in request.form:
            name = request.form['name']
            if name:                    
                g.cur.execute(sqls.location_edit % (name, pid))
                mysql.connection.commit()
                data['name'] = name
                flash("Successfully updated location", "success")
            else:
                flash("Product name cannot be empty")            
            return data
        else:
            return "No hacking !"
    except Exception as e:
        flash("Error : {}".format(e), "danger")


def move_push_get():
    data = {}
    
    g.cur.execute("SELECT * FROM `Product`")
    if g.cur.rowcount == 0:
        return "No Products yet"
    else:
        row = g.cur.fetchall()
        data['products'] = row

    g.cur.execute("SELECT * FROM `Location`")
    if g.cur.rowcount == 0:
        return "No Locations yet"
    else:
        row = g.cur.fetchall()
        data['locations'] = row

    return data

def move_push_post(mysql):
    try:
        product_id = request.form['product_id']
        location_id = request.form['location_id']
        qty = request.form['qty']
        g.cur.execute(sqls.move_push % (location_id, product_id, qty))
        mysql.connection.commit()
        flash("Successfully added product to location", "success")
        return redirect("/move/list", code=302) # This is to disable refresh
    except Exception as e:
        flash("Error : {}".format(e), "danger")

def move_move_post(mysql):
    data = {}
    try:
        product_id = request.form['product_id']
        from_location_id = request.form['from_location_id']
        to_location_id = request.form['to_location_id']
        qty = request.form['qty']

        # From Vashi to Seawoods, need to look how many products are there in Vashi (from_location_id)
        g.cur.execute(sqls.ProductMovement_to_Location % (product_id, from_location_id))
        pm_rows = g.cur.fetchall()
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

        g.cur.execute(sqls.ProductMovement_add % (from_location_id, to_location_id, product_id, qty))
        mysql.connection.commit()
        flash("Successfully moved product to location", "success")
        return redirect("/move/list", code=302) # This is to disable refresh
    except Exception as e:
        flash("Error : {}".format(e), "danger")
    
    return data

def move_move_get():
    data = {}
    g.cur.execute("SELECT * FROM `Product`")
    if g.cur.rowcount == 0:
        return "No Products yet"
    else:
        row = g.cur.fetchall()
        data['products'] = row

    g.cur.execute("SELECT * FROM `Location`")
    if g.cur.rowcount == 0:
        return "No Locations yet"
    else:
        row = g.cur.fetchall()
        data['locations'] = row
    
    return data


def data_movement(product_id, dict_index):
    data = {}
    g.cur.execute(sqls.data_movement % product_id)
    pm_rows = g.cur.fetchall()

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