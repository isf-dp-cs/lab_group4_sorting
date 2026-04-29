# to run the server: 
# # flask --app app.py --debug run

from flask import Flask, request, render_template, url_for, redirect, request
from models import db, Student  # Import from your other file
import secrets
from forms import StudentForm, GenerateGroupsForm
from helpers import *
from sqlalchemy import text


app = Flask(__name__, static_url_path=f'/')
app.secret_key = secrets.token_hex(32)  # Required for CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"

# Link the db to this specific app
db.init_app(app)

# Create the tables if it does not exisit, ignore if it exists 
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/groups", methods=['GET'])
def groups():
    students = db.session.execute(text("Select * from student order by group_num"))

    max_groups = len(db.session.execute(text("Select group_num from student group by group_num")).fetchall())
    max_groups = db.session.execute(text("Select COUNT(DISTINCT group_num) as count from student")).fetchone()[0]

    # print('MAX', max_groups.fetchone()[0])

    students_ordered = []
    for i in range(max_groups):
        empty_group_list = []
        students_ordered.append(empty_group_list)

    for student in students:
        students_ordered[student.group_num].append(student)
        

    group_metrics = {} # Stores {Group_ID: Score}

    group_metrics = {} # Stores {Group_ID: Score}

    for i in range(len(students_ordered)):
        group = students_ordered[i]

        sciences_present = {}
        
        for student in group:
            for trait in ['science1', 'science2', 'science3']:
                val = getattr(student, trait)
                # print(val)
                if val and val != "None":  # Only add if it's not None or empty
                    if val in sciences_present:
                        sciences_present[val] += 1
                    else:
                        sciences_present[val] = 1
                    
        group_metrics[i] = {
            "sciences": sciences_present # Sorted alphabetically for the UI
        }
    return render_template(
        'groups.html', 
        students = students,
        students_ordered=students_ordered,
        metrics=group_metrics)



@app.route(f"/groups/edit", methods=['GET', 'POST'])
def groups_edit():
    # students = Student.query.order_by(Student.group_num).all()

    students = db.session.execute(text("Select * from student order by group_num"))

    max_groups = len(db.session.execute(text("Select group_num from student group by group_num")).fetchall())
    max_groups = db.session.execute(text("Select COUNT(DISTINCT group_num) as count from student")).fetchone()[0]

    # print('MAX', max_groups.fetchone()[0])

    students_ordered = []
    for i in range(max_groups):
        empty_group_list = []
        students_ordered.append(empty_group_list)

    for student in students:
        students_ordered[student.group_num].append(student)
        

    group_metrics = {} # Stores {Group_ID: Score}

    for i in range(len(students_ordered)):
        group = students_ordered[i]

        sciences_present = {}
        
        for student in group:
            for trait in ['science1', 'science2', 'science3']:
                val = getattr(student, trait)
                # print(val)
                if val and val != "None":  # Only add if it's not None or empty
                    if val in sciences_present:
                        sciences_present[val] += 1
                    else:
                        sciences_present[val] = 1
                    
        group_metrics[i] = {
            "sciences": sciences_present # Sorted alphabetically for the UI
        }

    if request.method == 'POST':
        if request.form: 
            data = request.form
            
            for key, val in data.items():
                student = db.session.get(Student, key)
                student.group_num = val

                db.session.commit()
            
            return redirect(url_for('groups_edit'))


    return render_template(
            'groups_edit.html', 
            students = students,
            students_ordered=students_ordered,
            metrics=group_metrics
            )


@app.route(f"/add_student", methods=['GET', 'POST'])
def form_add_student():
    form = StudentForm()

    if request.method == 'POST':
        if form.validate_on_submit(): 
            data = form.data       
           
            new_student = Student(
                name=data['name'], 
                science1=data['science1'], 
                science2=data['science2'], 
                science3=data['science3'])
            
            db.session.add(new_student)
            db.session.commit()

            return redirect(url_for('index'))


    return render_template(
            'form_add.html', 
            form = form)

@app.route(f"/groups/generate", methods=['GET', 'POST'])
def groups_generate():
    form = GenerateGroupsForm()


    if request.method == 'POST':
    
        if form.validate_on_submit(): 
            if form.submit.data:
                return redirect(url_for('groups'))    
            
            if form.generate.data:
                data = form.data       
                students = Student.query.all()

                optimized_groups_list = assign_to_groups(students, data['num_groups'])


                group_metrics = {} # Stores {Group_ID: Score}

                for i in range(len(optimized_groups_list)):
                    group = optimized_groups_list[i]

                    sciences_present = {}
                    

                    for student in group:
                        student.group_num = i

                        for trait in ['science1', 'science2', 'science3']:
                            val = getattr(student, trait)
                            # print(val)
                            if val and val != "None":  # Only add if it's not None or empty
                                if val in sciences_present:
                                    sciences_present[val] += 1
                                else:
                                    sciences_present[val] = 1
                                
                    group_metrics[i] = {
                        "sciences": sciences_present # Sorted alphabetically for the UI
                    }

                    db.session.commit()


                return render_template(
                    'groups_generate.html', 
                    form = form,
                    metrics=group_metrics,
                    optimized_groups_list=optimized_groups_list, 
                )
            
        

    return render_template(
            'groups_generate.html', 
            form = form)


if __name__ == '__main__': 
    app.run(debug=True, port=5000)

    
