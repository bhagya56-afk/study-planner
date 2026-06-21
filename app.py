from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file)


@app.route("/")
def home():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form["task"]

    tasks = load_tasks()

    if task_text.strip():
        tasks.append({
            "text": task_text,
            "completed": False
        })

    save_tasks(tasks)

    return redirect(url_for("home"))


@app.route("/delete/<int:index>")
def delete_task(index):

    tasks = load_tasks()

    if index < len(tasks):
        tasks.pop(index)

    save_tasks(tasks)

    return redirect(url_for("home"))


@app.route("/complete/<int:index>")
def complete_task(index):

    tasks = load_tasks()

    if index < len(tasks):
        tasks[index]["completed"] = not tasks[index]["completed"]

    save_tasks(tasks)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)