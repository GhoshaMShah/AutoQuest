from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect,Flask,request
from flaskblog import app
import mysql.connector as mysql
from mysql.connector import Error
from mysql.connector import errorcode




posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contactUs")
def contactUs():
    return render_template('contactUs.html', title='Contact')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        form = RegistrationForm()
        db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
        found = 0
        myName = form.username.data
        myEmail = form.email.data
        cur = db.cursor()
# Select data from table using SQL query.
        cur.execute("SELECT * FROM login")
# print the first and second columns    
        for row in cur.fetchall():
            if row[1]==myName:
                found=1
                flash('Username already exists', 'danger')
                break
            elif row[2]==myEmail:
                found=1
                flash('Email already exists', 'danger')
                break
        if found==0:
            val = (form.username.data,form.email.data,form.password.data)
            query ="INSERT INTO login(Username,Email,Password) VALUES (%s,%s,%s)"
## There is no need to insert the value of rollno 
## because in our table rollno is autoincremented #started from 1
## storing values in a variable
## executing the query with values
            cur.execute(query,val)
## to make final output we have to run 
## the 'commit()' method of the database object
            db.commit()
            flash(f'Account created for {myName} ! ', 'success')
    return render_template('register.html', title='Register', form=form)


@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    form = RegistrationForm()
    return render_template('welcome.html', title='Welcome',form=form)        
 


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    found = 0
    myName = form.username.data
    myEmail = form.email.data
    myPassword = form.password.data
    if form.validate_on_submit():
        form = LoginForm()
        found = 0
        myPassword = form.password.data
        db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
        cur = db.cursor()
# Select data from table using SQL query.
        cur.execute("SELECT * FROM login")
# print the first and second columns    
        for row in cur.fetchall():
            if row[1]==myName and row[3]==myPassword:
                if row[2]==myEmail:
                    found=2
                    break
                else:
                    found=1
                    flash('Login Unsuccessful. Please check email', 'danger')

        if found==0:
            flash('Login Unsuccessful. Please check username and password', 'danger')
        elif found==2:
            flash("Login successful",'success')
            return redirect(url_for('Index',username=myName))
    return render_template('login.html', title='Login', form=form)


@app.route('/index/<string:username>')
def Index(username):
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("SELECT * FROM questions WHERE Username=%s",(username,))
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', questions=data, username=username)



@app.route('/insert/<string:username>', methods = ['POST'])
def insert(username):

    if request.method == "POST":
        flash("Question Inserted Successfully")
        #driver = webdriver.Chrome(executable_path="E:/darshan sem 7/project/flaskTutorial/flaskAutoQuestCRUD/chromedriver.exe")
        #driver = webdriver.get("file:///E:/darshan%20sem%207/project/flaskTutorial/flaskAutoQuestCRUD/templates/addstudent.html")
        #element = driver.find_element_by_id("semesterDropDown")
        #drp = Select(element)
        #semester = drp.first_selected_option.text
        #print(select.first_selected_option.text)
        #print(select.first_selected_option.get_attribute("value"))
        
        semester = int(request.form.get('semester'))
        subject = request.form['subject']
        #marks = int(request.form['marks'])
        #difficultyLevel = request.form['difficultyLevel']
        marks = int(request.form['marks'])
        
        difficultyLevel = request.form.get('difficultyLevel')
        
        question = request.form['question']

        #if question==" ":
         #   root = tkinter.Tk()
          #  root.withdraw()

# message box display
           # messagebox.showerror("Error", "Please insert the question")
        
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "mydatabase")
        cur = db.cursor()
        cur.execute("INSERT INTO questions (Username,Semester,Subject,Marks,Difficulty_level,Question) VALUES (%s, %s, %s, %s , %s, %s)", (username,semester,subject,marks,difficultyLevel,question))
        db.commit()
        return redirect(url_for('Index',username=username))


    


@app.route('/delete/<string:id_data>/<string:username>', methods = ['POST','GET'])
def delete(id_data,username):
    flash("Question Has Been Deleted Successfully")
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("DELETE FROM questions WHERE id=%s", (id_data,))
    db.commit()
    return redirect(url_for('Index',username=username))



@app.route('/update/<string:username>',methods=['POST','GET'])
def update(username):

    if request.method == 'POST':
        id_data = request.form['id']
        
        #semester = request.form.select['semester']
        semester = int(request.form.get('semester'))

        subject = request.form['subject']
        marks = request.form['marks']
        difficultyLevel = request.form.get('difficultyLevel')
        question = request.form['question']
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "mydatabase")
        cur = db.cursor()
        cur.execute("""
               UPDATE questions
               SET Semester=%s, Subject=%s, Marks=%s, Difficulty_level=%s, Question=%s
               WHERE id=%s
            """, (semester,subject,marks,difficultyLevel,question, id_data))
        flash("Question Updated Successfully")
        db.commit()
        return redirect(url_for('Index',username=username))
