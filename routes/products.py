from flask import render_template, request, redirect, current_app
from app import cursor
from routes import bp_prod
import os


@bp_prod.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = request.form['price']
            url_img = None

            if 'url_img' in request.files:
                file = request.files['url_img']

                if file:
                    filename = file.filename
                    file.save(os.path.join(current_app.root_path, 'static/images', filename))
                    url_img = '/static/images/' + filename

            cursor.execute("""INSERT INTO products (name, price, url_img) VALUES (?, ?, ?)""",
                           (name, price, url_img))
            cursor.commit()
        except Exception as e:
            return str(e)

        return redirect('/products')
    else:
        try:
            products = cursor.execute("SELECT * FROM products")
        except Exception as e:
            return str(e)
        return render_template('products/index.html', products=products)


@bp_prod.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    try:
        products = cursor.execute("SELECT * FROM products WHERE id = ?", id)
    except Exception as e:
        return str(e)

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        url_img = None

        if 'url_img' in request.files:
            file = request.files['url_img']

            if file:
                filename = file.filename
                file.save(os.path.join(current_app.root_path, 'static/images', filename))
                url_img = '/static/images/' + filename

        try:
            cursor.execute("""UPDATE products SET name = ?, price = ?, url_img = ? WHERE id = ?""",
                           (name, price, url_img, id))
            cursor.commit()
        except Exception as e:
            return str(e)

        return redirect('/products')
    else:
        return render_template('products/update.html', product=products.fetchone())


@bp_prod.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    try:
        cursor.execute("""DELETE FROM products WHERE id = ?""", id)
        cursor.commit()
    except Exception as e:
        return str(e)

    return redirect('/products')


@bp_prod.route('/search', methods=['POST', 'GET'])
def search():
    try:
        keywords = '%' + request.form['keywords'] + '%'
        products = cursor.execute("""
            SELECT * FROM products 
            WHERE name LIKE ? 
            OR price LIKE ? 
        """, (keywords, keywords))
    except Exception as e:
        return str(e)

    return render_template('products/index.html', products=products)
