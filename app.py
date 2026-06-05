from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

JSON_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as f:
            json.dump([], f)

    with open(JSON_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(JSON_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


@app.route('/')
def home():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()

    next_id = 1
    if tasks:
        next_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": next_id,
        "title": request.form['title'],
        "description": request.form['description'],
        "status": "Pending"
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return redirect('/')


@app.route('/update/<int:id>')
def update_task(id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == id:
            if task["status"] == "Pending":
                task["status"] = "Completed"
            else:
                task["status"] = "Pending"

    save_tasks(tasks)
    return redirect('/')


@app.route('/delete/<int:id>')
def delete_task(id):
    tasks = load_tasks()

    tasks = [task for task in tasks if task["id"] != id]

    save_tasks(tasks)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)