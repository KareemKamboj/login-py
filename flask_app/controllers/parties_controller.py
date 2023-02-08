from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.party_model import Party

@app.route("/parties/new")
def new_party_form():
    if 'user_id' not in session:
        return redirect('/')
    # logged_user = User.get_by_id({'id':session['user_id']})
    return render_template('parties_new.html')

@app.route("/parties/create", methods=['POST'])
def process_party():
    if 'user_id' not in session:
        return redirect('/')
    if not Party.validator(request.form):
        return redirect('/parties/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    id = Party.create(data)
    return redirect(f'/parties/{id}')

@app.route("/parties/<int:id>/delete")
def del_party(id):
    if 'user_id' not in session:
        return redirect('/')
    party = Party.get_by_id({'id':id})
    if not int(session['user_id']) == party.user_id:
            flash("Whoa there, thats not yours, hands off")
            return redirect('/welcome')
    Party.delete({'id':id})
    return redirect('/welcome')

@app.route("/parties/<int:id>/edit")
def edit_party(id):
    if 'user_id' not in session:
        return redirect('/')
    party = Party.get_by_id({'id':id})
    if not int(session['user_id']) == party.user_id:
        flash("Whoa there, thats not yours, hands off")
        return redirect('/welcome')
    party = Party.get_by_id({'id':id})
    return render_template("parties_edit.html", party=party)

@app.route("/parties/<int:id>/update", methods=['POST'])
def update_party(id):
    if 'user_id' not in session:
        return redirect('/')
    party = Party.get_by_id({'id':id})
    if not int(session['user_id']) == party.user_id:
        flash("Whoa there, thats not yours, hands off")
        return redirect('/welcome')
    if not Party.validator(request.form):
        return redirect(f'/parties/{id}/edit')
    data = {
        **request.form,
        'id':id
    }
    Party.update(data)
    return redirect("/welcome")

@app.route("/parties/<int:id>")
def show_party(id):
    party = Party.get_by_id({'id':id})
    return render_template("parties_one.html", party=party)

@app.route("/my_parties")
def my_parties():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    return render_template("my_parties.html", logged_user=user) 
