from flask import render_template, request, redirect
from app import cursor
from routes import bp_ctm


@bp_ctm.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date'] or None
        email = request.form['email']
        address = request.form['address']

        try:
            cursor.execute("""INSERT INTO customers (name, birth_date, email, address) VALUES (?, ?, ?, ?)""",
                           (name, birth_date, email, address))
            cursor.commit()
        except Exception as e:
            return str(e)

        return redirect('/customers')
    else:
        try:
            customers = cursor.execute("SELECT * FROM customers")
        except Exception as e:
            return str(e)

        return render_template('customers/index.html', customers=customers)


@bp_ctm.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    try:
        customers = cursor.execute("SELECT * FROM customers WHERE id = ?", id)
    except Exception as e:
        return str(e)

    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date'] or None
        email = request.form['email']
        address = request.form['address']

        try:
            cursor.execute("""UPDATE customers SET name = ?, birth_date = ?, email = ?, address = ? WHERE id = ?""",
                           (name, birth_date, email, address, id))
            cursor.commit()
        except Exception as e:
            return str(e)

        return redirect('/customers')
    else:
        return render_template('customers/update.html', customer=customers.fetchone())


@bp_ctm.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    try:
        cursor.execute("""DELETE FROM customers WHERE id = ?""", id)
        cursor.commit()
    except Exception as e:
        return str(e)

    return redirect('/customers')


@bp_ctm.route('/search', methods=['POST', 'GET'])
def search():
    try:
        keywords = '%' + request.form['keywords'] + '%'
        customers = cursor.execute("""
            SELECT * FROM customers 
            WHERE name LIKE ? 
            OR birth_date LIKE ? 
            OR email LIKE ? 
            OR address LIKE ?
        """,
                                   (keywords, keywords, keywords, keywords))
    except Exception as e:
        return str(e)

    return render_template('customers/index.html', customers=customers)
