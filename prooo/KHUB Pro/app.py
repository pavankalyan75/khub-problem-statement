from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import plotly.graph_objs as go
from plotly.offline import plot

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ABHI@1289' 
app.config['MYSQL_DB'] = 'flaskapp'
app.config['SECRET_KEY'] = 'secret_key'
app.config['TEMPLATES_AUTO_RELOAD'] = True

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    mobile = request.form['mobile']
    grade = request.form['grade']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(name, age, gender, mobile, grade) VALUES(%s, %s, %s, %s, %s)",
                (name, age, gender, mobile, grade))
    mysql.connection.commit()
    cur.close()

    flash('Submitted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        if userid == '100' and password == '200':
            return redirect(url_for('data'))
        else:
            flash('Invalid credentials!', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/data')
def data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE age BETWEEN 0 AND 10")
    age_0_10 = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE age BETWEEN 11 AND 20")
    age_11_20 = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE age BETWEEN 21 AND 30")
    age_21_30 = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE gender='Male'")
    male_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE gender='Female'")
    female_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE mobile='Yes'")
    mobile_yes = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE mobile='No'")
    mobile_no = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE grade='A'")
    grade_a = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE grade='B'")
    grade_b = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE grade='C'")
    grade_c = cur.fetchone()[0]

    cur.close()

    age_labels = ['0-10', '11-20', '21-30']
    age_values = [age_0_10, age_11_20, age_21_30]

    gender_labels = ['Male', 'Female']
    gender_values = [male_count, female_count]

    mobile_labels = ['Yes', 'No']
    mobile_values = [mobile_yes, mobile_no]

    grade_labels = ['A', 'B', 'C']
    grade_values = [grade_a, grade_b, grade_c]

    age_chart_labels = age_labels
    age_chart_values = age_values
    gender_chart_labels = gender_labels
    gender_chart_values = gender_values
    mobile_chart_labels = mobile_labels
    mobile_chart_values = mobile_values
    grade_chart_labels = grade_labels
    grade_chart_values = grade_values

    return render_template('data.html', total_users=total_users,
                           age_chart_labels=age_chart_labels, age_chart_values=age_chart_values,
                           gender_chart_labels=gender_chart_labels, gender_chart_values=gender_chart_values,
                           mobile_chart_labels=mobile_chart_labels, mobile_chart_values=mobile_chart_values,
                           grade_chart_labels=grade_chart_labels, grade_chart_values=grade_chart_values)

def create_pie_chart(labels, values, title):
    data = [go.Pie(labels=labels, values=values)]
    layout = go.Layout(title=title)

    fig = go.Figure(data=data, layout=layout)
    chart_data = plot(fig, output_type='div', include_plotlyjs=False)

    return chart_data


if __name__ == '__main__':
    app.run(debug=True)
