#create the app 

from flask import Flask,render_template,request,url_for
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/option")
def option():
    return render_template("option.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_check", methods=["GET","POST"])
def login_check():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        
        data=[email,password]
        # Establish connection to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Jee_Mains"
        )
        cursor = conn.cursor(buffered=True)
        
        cursor.execute("""SELECT * FROM data WHERE email = %s AND password = %s """, data)
        result = cursor.fetchall()
        
        if len(result)==0:
            return render_template("Incorrect.html")
            
        elif len(result)==1:
            return render_template("Welcome.html")
         
    return data



@app.route("/sign")
def sign():
    return render_template("sign.html")

@app.route("/sign_data" , methods=["POST","GET"])
def sign_data():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        cp=request.form["confirm-password"]
        l=[name,email,password,cp]
        if password==cp:
            data=(name,email,password)
            # Establish connection to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Jee_Mains"
            )
            cursor = conn.cursor(buffered=True)
            # Insert data into the MySQL database
            cursor.execute("""
                INSERT INTO data (name,email,password)
                VALUES (%s, %s, %s)
            """,data)
            
            # Commit the transaction
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            return render_template("Sucessfully.html")
        
        else:
            return render_template("try_again.html")
    

    return l

@app.route('/result')
def result():
    # Connect to the database and fetch candidate data
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Jee_Mains"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from candidate where sno=(select max(sno) from candidate)")
    candidates = cursor.fetchall()
    cursor.close()
    conn.close()

    # Render the template and pass the candidates data to it
    return render_template('result.html',candidates=candidates)

@app.route("/Regstration_form")
def Registration_form():
    return render_template("index.html")

@app.route("/data",methods=["POST","GET"])  
def data():
    if request.method=="POST":
        nm=request.form["name"]
        email=request.form["email"]
        phn=request.form["phone"]
        dob=request.form["date"]
        sex=request.form["gender"]
        cat=request.form["cat"]
        adr=request.form["address"]
        s1=request.form["s1"]
        c1=request.form["c1"]
        s2=request.form["s2"]
        c2=request.form["c2"]
        s3=request.form["s3"]
        c3=request.form["c3"]
        pay=request.form["payment"]
        
    data=[nm,email,phn,dob,sex,cat,s1,c1,s2,c2,s3,c3,pay,adr]
    
    # Establish connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Jee_Mains"
    )
    cursor = conn.cursor(buffered=True)
    # Insert data into the MySQL database
    cursor.execute("""
        INSERT INTO candidate(name,email,phn,dob,sex,cat,s1, c1, s2, c2, s3, c3, pay,ad)
        VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,data)
    
    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return result()
        



if __name__ == "__main__":
    app.run(debug=True)  
    

