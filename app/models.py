from . import db

class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.String(128), nullable=False)
    rule_level = db.Column(db.Integer, nullable=False)
    rule_description = db.Column(db.Text, nullable=False)
    remediation = db.Column(db.Text)
    significant_findings = db.Column(db.Text)
    mitre_ids = db.relationship('MitreID', backref='play', lazy='dynamic')
    mitre_tactics = db.relationship('MitreTactic', backref='play', lazy='dynamic')
    mitre_techniques = db.relationship('MitreTechnique', backref='play', lazy='dynamic')

class MitreID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), nullable=False)
    play_id = db.Column(db.Integer, db.ForeignKey('play.id'), nullable=False)

class MitreTactic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), nullable=False)
    play_id = db.Column(db.Integer, db.ForeignKey('play.id'), nullable=False)

class MitreTechnique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), nullable=False)
    play_id = db.Column(db.Integer, db.ForeignKey('play.id'), nullable=False)
