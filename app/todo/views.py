from flask import render_template, request, redirect, url_for, flash, current_app
from .. import db
from .models import Task, Category
from . import todo_bp
from flask_login import login_required, current_user
from .form import Taskform, CategoryForm

@todo_bp.route('/task', methods=['GET'])
@login_required
def tasks():

    tasks_ = Task.query.order_by(Task.priority.desc(),
                                 Task.deadline.asc()
                                 ).all()   
    return render_template('task.html', tasks=tasks_)

@todo_bp.route('/task/create', methods=['GET', 'POST'])
@login_required
def task_create():
    form = Taskform()

    if form.validate_on_submit():

        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data
        category = form.category.data
        task_info = Task(title=title,
                         description=description,
                         deadline=deadline,
                         priority=priority,
                         progress=progress,
                         category_id=category,
                         owner_id=current_user.get_id())
        task_info.users.append(current_user)
        db.session.add(task_info)
        db.session.commit()

        flash(f"Task created!", category='success')
        return redirect(url_for("todo.task_create"))

    elif request.method == 'POST':
        flash("Validation failed!", category='warning')
        return redirect(url_for("todo.task_create"))
    
    return render_template('task_create.html', form=form)

@todo_bp.route('/task/<int:id>',methods=['GET', 'POST'])
@login_required
def task(id):
    task = Task.query.filter_by(id=id).first()
    task_detail = {
        'Title': task.title,
        'Description': task.description,
        'Created': task.created,
        'Modified': task.modified,
        'Deadline': task.deadline.date(),
        'Priority': task.priority,
        'Progress': task.progress
    }
    form = Taskform()

    return render_template('single_task.html', task_detail=task_detail,
                           id=task.id,
                           form=form,
                           assigned=task.users,
                           user=current_user)


@todo_bp.route('/task/<int:id>/update', methods=['GET', 'POST'])
@login_required
def task_update(id):
    
    form = Taskform()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        deadline = form.deadline.data
        priority = form.priority.data
        progress = form.progress.data

        task = Task.query.filter_by(id=id).first()
        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        task.progress = progress
        db.session.add(task)
        db.session.commit()

        flash(f"Task successfully updated", category='success')
        return redirect(url_for("to_do.task", id=id))

    elif request.method == 'POST':
        print(form.errors, form.description.data)
        flash("Validation failed!", category='warning')
        return redirect(url_for("to_do.task", id=id))

    return render_template('task_update.html', form=form, task_id=id)

@todo_bp.route('/task/<int:id>/delete', methods=['GET'])
@login_required
def task_delete(id):
    task_ = Task.query.get_or_404(id)
    
    try:
        db.session.delete(task_)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Task deleted", category='success')
        current_app.logger.info("Task deleted")
    
    return redirect(url_for('to_do.task'))

@todo_bp.route('/categories', methods=['GET'])
@login_required
def categories():
    categories_ = Category.query.all()
    return render_template('categories.html', categories=categories_)


@todo_bp.route('/category/create', methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryForm()
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            category = Category(name=form.name.data) 

            try:
                db.session.add(category)
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Category added", category='success')
        else:
            return redirect(url_for('account.login'))
  
    
    if request.method == 'POST':
        return redirect(url_for('todo.categories')) 
    
    return render_template('category_create.html', form=form)


@todo_bp.route('/category/<int:id>/update', methods=['GET', 'POST'])
@login_required
def category_update(id):
    category_ = Category.query.get_or_404(id)
    
    form = CategoryForm(name=category_.name)
    
    if form.validate_on_submit():
        if current_user.is_authenticated:
            try:
                category_.name = form.name.data
            except:
                db.session.rollback()
            else:
                db.session.commit()
                flash("Category updated", category='success')
                current_app.logger.info("Category updated")
        else:
            return redirect(url_for('account.login'))
  
    if request.method == 'POST':
        return redirect(url_for('to_do.categories', id=category_.id)) 
    
    return render_template('category_form.html', form=form)

@todo_bp.route('/categories/<int:id>/delete', methods=['GET'])
@login_required
def category_delete(id):
    category_ = Category.query.get_or_404(id)
    
    try:
        db.session.delete(category_)
    except:
        db.session.rollback()
    else:
        db.session.commit()
        flash("Category deleted", category='success')
        current_app.logger.info("Category deleted")
    
    return redirect(url_for('to_do.categories'))
