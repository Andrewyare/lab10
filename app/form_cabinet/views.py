import logging
from flask import  render_template, request, redirect, session, url_for, flash

from app.account.form import ContactForm
from .. import db
from .models import Contacts
from . import form_bp

@form_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    main = logging.getLogger('main')
    main.setLevel(logging.DEBUG)
    handler = logging.FileHandler('log')
    format = logging.Formatter('%(asctime)s  %(name)s %(levelname)s: %(message)s')
    handler.setFormatter(format)
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        save_to_db(form)
        flash("Data sent successfully: " + session.get('username') + ' ' + session.get('email'), category = 'success')
        return redirect(url_for("form.contact"))

    elif request.method == 'POST':
        flash("Validation failed", category = 'warning')
        main.addHandler(handler)
        main.error(form.name.data + " " + form.email.data + " " + form.phone.data + " " + form.subject.data + " " + form.message.data)

    if(session.get('username') == None):
        return render_template('contact.html', form=form, username="Guest")
    else :
        form.name.data = session.get('username')
        form.email.data = session.get('email')
        return render_template('contact.html', form=form, username=session.get('username'))

@form_bp.route('/database')
def database() :
    contacts = Contacts.query.all()
    return render_template('database.html', contacts=contacts)

@form_bp.route('/database/delete/<id>')
def delete_by_id(id):
    data = Contacts.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("form.database"))


def save_to_db(form) :
    contact = Contacts(
        name = form.name.data,
        email = form.email.data,
        phone = form.phone.data,
        subject = form.subject.data,
        message = form.message.data
    )
    try:
        db.session.add(contact)
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()