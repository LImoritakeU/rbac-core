from flask import Flask, render_template, redirect, url_for

from tests.testbase import prep_db
from rbac.models import *

app = Flask(__name__, static_folder='../static')


@app.before_first_request
def setup():
    if db.engine.dialect.has_table(db.engine, 'user'):
        db.drop_all()
    db.create_all()
    prep_db(db)


@app.route('/')
def index():
    roles = db.sess.query(Role).all()
    for role in roles:
        if role.name == "admin":
            admin = role
        if role.name == "general":
            general = role
        if role.name == "manager":
            manager = role
    permissions = db.sess.query(Permission).all()

    return render_template(
        'index.html', admin=admin, general=general, manager=manager,
        permissions=permissions
    )


@app.route('/user/<name>')
def user(name):
    user = db.sess.query(User).filter_by(name=name).first()
    permissions = db.sess.query(Permission).all()

    return render_template(
        'user.html', user=user, permissions=permissions)


@app.route('/user/<name>/activate')
def activate(name):
    user = db.sess.query(User).filter_by(name=name).first()

    user.activate_role(user.roles[0])

    return redirect(url_for('user', name=user.name))


@app.route('/user/<name>/deactivate')
def deactivate(name):
    user = db.sess.query(User).filter_by(name=name).first()

    user.deactivate_role(user.roles[0])

    return redirect(url_for('user', name=user.name))


if __name__ == '__main__':
    app.run(debug=True)