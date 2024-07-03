# Importing the Flask class from flask module
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# let's see the content of the flask module
# print( dir(flask) )

# let's create the object of the Flask class
app = Flask(__name__)






# connecting the flask app (server) with sqllite database
# let's write the url: This command tells the flask app to connect with a sqllite type database named task.db
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'


# creating an object of SQLalchemy class
# Telling the SQLAlchemy class, which flask app to connect with
database = SQLAlchemy(app)




# writing python class which will be used to insert data into table
class Task(database.Model):

    sno = database.Column(database.Integer, primary_key= True)
    taskTitle = database.Column(database.String(100), nullable= False)
    taskDescription = database.Column(database.String(200), nullable= False)







# First route: Index route/default route
@app.route('/', methods = ["GET", "POST"])
def index():

    # print(request.form)

    # let's check if the request is get or post
    # if request is post --> 
    if request.method == "POST":
        
        # fetch the values of title and description
        task_title = request.form.get('title')
        task_description = request.form.get('description')
        print(task_title, task_description)

        # add it to the database
        task = Task(taskTitle= task_title, taskDescription= task_description)
        database.session.add(task)
        database.session.commit()

        # returning the index.html page
        return redirect('/')

    # if the nature of web request is a get request
    else:

        # fetching all the tasks from the database
        allTasks = Task.query.all()

        # for task in allTasks:
        #     print(task.sno, task.taskTitle, task.taskDescription)

        # return render_template('index.html')
        return render_template('index.html', allTasks= allTasks)

# Second route: Contact us
@app.route('/contact')
def contact():
    
    # returning the response
    return render_template('contact.html')


# Third route: About us
@app.route('/about')
def about():
    
    # returning the response
    return render_template('about.html')

# fourth route: Delete a task from the table
@app.route('/delete')
def delete():

    # extracting the sno
    serial_number = request.args.get('sno')

    # fetching task with sno = sno
    task = Task.query.filter_by(sno= serial_number).first()

    # deleting the task
    database.session.delete(task)
    database.session.commit()

    # redirecting back to the index route
    return redirect("/")

# fifth route: Updating a task
@app.route("/update", methods = ["GET", "POST"])
def update():

    # getting the serial number of the task which is to be updated
    serial_number = request.args.get('sno')

    # fetching that task from database to check its existing value
    reqTask = Task.query.filter_by(sno= serial_number).first()

    # if this route get's a post request with updated values of title and description
    if request.method == "POST":
        
        # fetching the updated values
        updatedTitle = request.form.get('title')
        updatedDescription = request.form.get('description')

        # changing the value of the existing task
        reqTask.taskTitle = updatedTitle
        reqTask.taskDescription = updatedDescription

        # committing the changes to database
        database.session.add(reqTask)
        database.session.commit()

        # redirecting back to index page
        return redirect('/')
    
    # if we got a GET request
    else:

        return render_template('update.html', reqTask= reqTask)


# let's run the flask application
if __name__ == "__main__":
    app.run(debug=True)
# app.run(debug=True, host='0.0.0.0')

