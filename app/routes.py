from app import app
from app import render_template, request, redirect, url_for


@app.route("/")
def home():
    return render_template("home.html", active_page="home")


@app.route("/new-play", methods=['GET', 'POST'])
def new_play():
    if request.method == 'POST':
        mitre_ids = request.form.getlist('mitre.id[]')
        print(mitre_ids)
    return render_template("new_play.html", active_page="new_play")


@app.route("/update-play")
def update_play():
    return render_template("update_play.html", active_page="update_play")


@app.route("/playbook")
def playbook():
    return render_template("playbook.html", active_page="playbook")