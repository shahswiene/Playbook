from . import app, db
from flask import render_template, request, redirect, url_for, jsonify
from .models import Play, MitreID, MitreTactic, MitreTechnique


@app.route("/")
def home():
    return render_template("home.html", active_page="home")


@app.route("/new-play", methods=['GET', 'POST'])
def new_play():
    if request.method == 'POST':
        # Get form data
        rule_id = request.form.get('rule.id')
        rule_level = request.form.get('rule.level')
        rule_description = request.form.get('rule.description')
        remediation = request.form.get('remediation')
        significant_finding = request.form.get('significantFinding')  # Updated field name

        # Create a new Play object
        new_play = Play(
            rule_id=rule_id,
            rule_level=rule_level,
            rule_description=rule_description,
            remediation=remediation,
            significant_findings=significant_finding  # Updated field name
        )

        # Create MitreID, MitreTactic, and MitreTechnique objects and associate them with the Play
        mitre_ids = request.form.getlist('mitre.id[]')
        mitre_tactics = request.form.getlist('mitre.tactic[]')
        mitre_techniques = request.form.getlist('mitre.technique[]')

        for mitre_id_value in mitre_ids:
            mitre_id = MitreID(value=mitre_id_value)
            new_play.mitre_ids.append(mitre_id)

        for mitre_tactic_value in mitre_tactics:
            mitre_tactic = MitreTactic(value=mitre_tactic_value)
            new_play.mitre_tactics.append(mitre_tactic)

        for mitre_technique_value in mitre_techniques:
            mitre_technique = MitreTechnique(value=mitre_technique_value)
            new_play.mitre_techniques.append(mitre_technique)

        # Add the Play and related objects to the database
        db.session.add(new_play)
        db.session.commit()

        # Redirect to a success page or any other page as needed
        return redirect(url_for('home'))

    return render_template("new_play.html", active_page="new_play")


@app.route("/playbook")
def playbook():
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    plays = Play.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("playbook.html", active_page="playbook", plays=plays.items, total_pages=plays.pages, current_page=plays.page)


@app.route("/edit-play/<int:play_id>", methods=['POST'])
def edit_play(play_id):
    play = Play.query.get_or_404(play_id)
    
    play.rule_id = request.json['rule_id']
    play.rule_level = request.json['rule_level']
    play.rule_description = request.json['rule_description']
    play.remediation = request.json['remediation']
    play.significant_findings = request.json['significant_findings']

    # Update MitreIDs, MitreTactics, and MitreTechniques
    # Remove existing relations
    MitreID.query.filter_by(play_id=play_id).delete()
    MitreTactic.query.filter_by(play_id=play_id).delete()
    MitreTechnique.query.filter_by(play_id=play_id).delete()

    # Add new relations
    for mitre_id_value in request.json['mitre_ids']:
        mitre_id = MitreID(value=mitre_id_value, play_id=play_id)
        db.session.add(mitre_id)

    for mitre_tactic_value in request.json['mitre_tactics']:
        mitre_tactic = MitreTactic(value=mitre_tactic_value, play_id=play_id)
        db.session.add(mitre_tactic)

    for mitre_technique_value in request.json['mitre_techniques']:
        mitre_technique = MitreTechnique(value=mitre_technique_value, play_id=play_id)
        db.session.add(mitre_technique)

    db.session.commit()
    return jsonify({'message': 'Play updated successfully'})


@app.route('/get-play/<int:play_id>')
def get_play(play_id):
    play = Play.query.get_or_404(play_id)
    play_data = {
        'rule_id': play.rule_id,
        'rule_level': play.rule_level,
        'rule_description': play.rule_description,
        'remediation': play.remediation,
        'significant_findings': play.significant_findings,
        'mitre_ids': [mitre_id.value for mitre_id in play.mitre_ids],
        'mitre_tactics': [mitre_tactic.value for mitre_tactic in play.mitre_tactics],
        'mitre_techniques': [mitre_technique.value for mitre_technique in play.mitre_techniques]
    }
    return jsonify(play_data)

@app.route("/delete-play/<int:play_id>", methods=['POST'])
def delete_play(play_id):
    ## Delete the play and related objects
    Play.query.filter_by(id=play_id).delete()
    MitreID.query.filter_by(play_id=play_id).delete()
    MitreTactic.query.filter_by(play_id=play_id).delete()
    MitreTechnique.query.filter_by(play_id=play_id).delete()
    db.session.commit()
    return jsonify({'message': 'Play deleted successfully'})


