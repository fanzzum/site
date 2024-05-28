from flask import Flask,render_template,request
import sqlite3

def renum_id(conn) :
    cursor = conn.cursor()
    cursor.execute ('''
       SELECT id FROM tasks ORDER BY id
                   ''')
    rows = cursor.fetchall()
    for index ,row in enumerate(rows,start=1) :
        cursor.execute('''
            UPDATE tasks SET id =? WHERE id = ?
                      ''',(index,row[0]))
    conn.commit()
    

app = Flask(__name__)
@app.route('/', methods=["GET","POST"])
def index():
    conn= sqlite3.connect('tasks.db')
    tasks =conn.cursor()
    tasks.execute('''
           CREATE table IF NOT EXISTS tasks
                 ( id INTEGER PRIMARY KEY,
                  task TEXT NOT NULL,
                  status TEXT NOT NULL )

                  ''')
    if 'add' in request.form :
       task = request.form.get("add")

       tasks.execute('''
            INSERT INTO tasks (task,status) VALUES (?,"incomplete")
                     ''',(task,))
       conn.commit()
       tasks.execute('''
           SELECT task FROM tasks WHERE status = "incomplete"
                                ''')
       comtasks = tasks.fetchall()
       tasks.close()
       conn.close()
       return render_template("index.html",comtasks=comtasks)
       
    elif 'remove' in request.form :
       rmv = request.form.get("remove")

       tasks.execute('''
            DELETE FROM tasks WHERE id = ?
                     ''',(rmv,))
       conn.commit()
       renum_id(conn)
       tasks.execute('''
           SELECT task FROM tasks WHERE status = "incomplete"
                                ''')
       comtasks = tasks.fetchall()
       tasks.close()
       conn.close()
       return render_template("index.html",comtasks=comtasks)

    else :
        return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True, threaded=False)

