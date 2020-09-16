from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import base64

app = Flask(__name__)


# MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ebromic'
app.config['MYSQL_PASSWORD'] = 'Ericsson1'
app.config['MYSQL_DB'] = 'ai'
mysql = MySQL(app)


# Session
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cursordb = mysql.connection.cursor()
    sql = 'SELECT * FROM contracts_info;'
    cursordb.execute(sql)
    agreements_list = cursordb.fetchall()
    agreements = []
    for agreement in agreements_list:
        agreementid = str(agreement[0]).encode('utf-8')
        agreementid = base64.b64encode(agreementid)
        agreementid = agreementid.decode('utf-8')
        agreement = list(agreement)
        agreement[0] = '"' + agreementid + '"'
        agreement = tuple(agreement)
        agreements.append(agreement)

    return render_template('index.html', agreements = agreements)


@app.route('/summary', methods = ['GET'])
def Summary():
    docID = request.args.get('docID')
    docID.replace('"', '')
    docID = docID.encode('utf-8')
    docID = base64.b64decode(docID)
    docID = docID.decode('utf-8')

    cursordb_agreement = mysql.connection.cursor()
    sql_agreement = "SELECT Summary FROM contracts_info WHERE id = %s;" % (docID)
    cursordb_agreement.execute(sql_agreement)
    print(sql_agreement)
    contract = cursordb_agreement.fetchall()
    for row in contract:
        contract = row[0]

    return contract


@app.route('/fullagreement', methods = ['GET'])
def Full_agreement():
    docID = request.args.get('docID')
    docID.replace('"', '')
    docID = docID.encode('utf-8')
    docID = base64.b64decode(docID)
    docID = docID.decode('utf-8')
    
    cursordb_agreement = mysql.connection.cursor()
    sql_agreement = "SELECT Digital_file FROM contracts_info WHERE id = %s;" % (docID)
    cursordb_agreement.execute(sql_agreement)
    print(sql_agreement)
    contract = cursordb_agreement.fetchall()
    for row in contract:
        contract = row[0]

    return contract


@app.route('/search', methods = ['POST'])
def Search():
    if request.method == 'POST':
        suppliername = request.form['suppliername']
        cursordb = mysql.connection.cursor()
        sql = "SELECT * FROM contracts_info WHERE Agreement_Supplier_name LIKE '%s';" % ('%'+suppliername+'%')
        cursordb.execute(sql)
        print(sql)
        data = cursordb.fetchall()
    return render_template('index.html', agreements = data)


@app.route('/compare', methods = ['POST'])
def Compare():
    if request.method == 'POST':
        ids = ''
        a = 0
        for checkbox in request.form.getlist('check'):
            checkbox.replace('"', '')
            checkbox = checkbox.encode('utf-8')
            checkbox = base64.b64decode(checkbox)
            checkbox = checkbox.decode('utf-8')
            
            if a == 0:
                ids = checkbox
            else:
                ids = ids + ' OR ci.id = ' + checkbox
            a += 1
    cursordb = mysql.connection.cursor()
    #sql = "SELECT Agreement_name, Agreement_Supplier_name, Parent_agreement_ID, Payment_terms_daysn, Agreement_type, Pages FROM contracts_info WHERE id = %s;" % (ids)
    sql = "SELECT ci.Agreement_name, ci.Agreement_Supplier_name, cr.Agreement_Manager, cr.Product_Category, cr.Master_Cluster, ci.Parent_agreement_ID, ci.Payment_terms_daysn, ci.Agreement_type, ci.Pages, cr.Created\
         FROM contracts_info ci LEFT JOIN clm_report cr ON cr.Master_Agreement_ID = ci.Parent_agreement_ID WHERE ci.id = %s;" % (ids)
    cursordb.execute(sql)
    print(sql)
    data = cursordb.fetchall()

    return render_template('compare.html', agreements = data)


if __name__ == '__main__':
    app.run(port = 3000, debug = True)