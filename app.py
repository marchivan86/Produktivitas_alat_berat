from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = "^A%DJAJU^JJ123"
app.config['MYSQL_HOST'] = 'produktivitasalatberat.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'produktivitasala'
app.config['MYSQL_PASSWORD'] = 'oeealatberat123'
app.config['MYSQL_DB'] = 'produktivitasala$oeealatberat'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)



@app.route('/')
def home():
    if 'name' in session:
        return render_template('homeadmin.html')
    else:
        return render_template('home.html')

@app.route('/account_login')
def account_login():
    return render_template("accountlogin.html")

@app.route('/account_register')
def account_register():
    return render_template("accountregister.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Proses login di sini
        return redirect(url_for('dashboard'))
    return render_template('dashboardadmin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Proses registrasi di sini
        flash('Registrasi berhasil. Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('dashboardadmin.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')


@app.route('/AvailabilityDash')
def AvailabilityDash():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('AvailabilityDash.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')

@app.route('/UtilizationDash')
def UtilizationDash():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('UtilizationDash.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')

@app.route('/ProductivityDash')
def ProductivityDash():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('ProductivityDash.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')

@app.route('/OEEDash')
def OEEDash():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('OEEDash.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')


@app.route('/cycletime')
def cycletime():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('cycletime.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')

@app.route('/max_prductivity')
def max_prductivity():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('max_prductivity.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')

@app.route('/pmpdashboard')
def pmpdashboard():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('pmpdashboard.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')

# Akun Admin
@app.route('/login_admin', methods=["GET", "POST"])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users_admin WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if user:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("homeadmin.html")
            else:
                return render_template("accountloginpsemailnotmatch.html")
        else:
            return render_template("accountloginusernotfound.html")
    else:
        return render_template("loginadmin.html")

@app.route('/register_admin', methods=["GET", "POST"])
def register_admin():
    if request.method == 'GET':
        return render_template("registeradmin.html")
    else:
        name = request.form['name']
        email = request.form['email']
        otp = request.form['otp']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        if otp == 'heavy':
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users_admin (name, email, password) VALUES (%s,%s,%s)",
                        (name, email, hash_password,))
            mysql.connection.commit()
            # session['name'] = request.form['name']
            # session['email'] = request.form['email']
            return render_template("registersucces.html")
        else:
            return render_template("otpsalah.html")
# end akun admin

@app.route('/dashboardadmin')
def dashboardadmin():
    if 'name' in session:
        # Tampilkan halaman dashboard
        return render_template('dashboardadmin.html')
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')

@app.route('/homeadmin')
def homeadmin():
    if 'name' in session:
        # Tampilkan halaman homeadmin
        return render_template("homeadmin.html")
    else:
        flash('Silakan login terlebih dahulu.', 'danger')
        return render_template('home.html')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")

#if __name__ == '__main__':
#    app.secret_key = "^A%DJAJU^JJ123"
#    app.run(debug=True)
#    #app.run(host='0.0.0.0', debug=True)
