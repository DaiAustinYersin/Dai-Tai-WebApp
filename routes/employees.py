from flask import render_template, request, redirect
from app import cursor
from routes import bp_emp


@bp_emp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date'] or None
        salary = request.form['salary']

        try:
            cursor.execute("""INSERT INTO employees (name, start_date, end_date, salary) VALUES (?, ?, ?, ?)""",
                           (name, start_date, end_date, salary))
            cursor.commit()
        except Exception as e:
            return str(e)

        return redirect('/employees')
    else:
        try:
            employees = cursor.execute("SELECT * FROM employees")
        except Exception as e:
            return str(e)

        return render_template('employees/index.html', employees=employees)


@bp_emp.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    try:
        employees = cursor.execute("SELECT * FROM employees WHERE id = ?", id)
    except Exception as e:
        return str(e)

    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date'] or None
        salary = request.form['salary']

        try:
            cursor.execute("""UPDATE employees SET name = ?, start_date = ?, end_date = ?, salary = ? WHERE id = ?""",
                           (name, start_date, end_date, salary, id))
            cursor.commit()
        except Exception as e:
            return str(e)

        return redirect('/employees')
    else:
        return render_template('employees/update.html', employee=employees.fetchone())


@bp_emp.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    try:
        cursor.execute("""DELETE FROM employees WHERE id = ?""", id)
        cursor.commit()
    except Exception as e:
        return str(e)

    return redirect('/employees')


@bp_emp.route('/search', methods=['POST', 'GET'])
def search():
    try:
        keywords = '%' + request.form['keywords'] + '%'
        employees = cursor.execute("""
            SELECT * FROM employees 
            WHERE name LIKE ? 
            OR start_date LIKE ? 
            OR end_date LIKE ? 
            OR salary LIKE ?
        """,
                                   (keywords, keywords, keywords, keywords))
    except Exception as e:
        return str(e)

    return render_template('employees/index.html', employees=employees)
