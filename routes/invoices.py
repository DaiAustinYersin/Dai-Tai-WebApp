from flask import render_template, request, redirect
from app import cursor
from routes import bp_inv


@bp_inv.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            customer_id = request.form['customer_id']
            total_price = request.form['total_price']

            # Insert into invoices table
            cursor.execute(
                'INSERT INTO invoices (customer_id, total_price) VALUES (?, ?)',
                (customer_id, total_price)
            )

            cursor.commit()

            # Get the last inserted ID
            cursor.execute('SELECT MAX(id) from invoices')
            invoice_id = cursor.fetchone()[0]  # Fetch the first column of the first row

            # Insert into invoice_details table
            product_ids = request.form.getlist('product_id[]')
            quantities = request.form.getlist('quantity[]')
            total_prices = request.form.getlist('total_price[]')

            for i in range(len(product_ids)):
                cursor.execute(
                    'INSERT INTO invoice_details (invoice_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                    (invoice_id, product_ids[i], quantities[i], total_prices[i])
                )

            cursor.commit()
        except Exception as e:
            cursor.rollback()
            return str(e)

        return redirect('/invoices')
    else:
        try:
            cursor.execute("SELECT * FROM customers")
            customers = cursor.fetchall()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            cursor.execute("""
                SELECT i.id, CONCAT(c.id, ' - ', c.name) customer, total_price, created_date
                FROM invoices i
                INNER JOIN customers c on i.customer_id = c.id
            """)
            invoices = cursor.fetchall()
        except Exception as e:
            return str(e)

        return render_template('invoices/index.html', customers=customers, products=products, invoices=invoices)


@bp_inv.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    try:
        cursor.execute("""DELETE FROM invoices WHERE id = ?""", id)
        cursor.commit()
    except Exception as e:
        return str(e)

    return redirect('/invoices')


@bp_inv.route('/view/<int:id>')
def view(id):
    try:
        cursor.execute("""
            SELECT i.id, CONCAT(c.id, ' - ', c.name) customer, total_price, created_date
            FROM invoices i
            INNER JOIN customers c on i.customer_id = c.id
            WHERE i.id = ?
        """, id)
        invoice = cursor.fetchone()
        cursor.execute("""SELECT i.id, p.url_img, p.name, quantity, i.price
                            FROM invoice_details i
                            INNER JOIN products p on i.product_id = p.id 
                            WHERE invoice_id = ?
        """, id)
        invoice_details = cursor.fetchall()
    except Exception as e:
        return str(e)

    return render_template('invoices/view.html', invoice=invoice, invoice_details=invoice_details)
