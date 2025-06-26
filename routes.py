import os
from flask import render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import login_required, login_user, logout_user, current_user
from app import app
from models import Project, Admin

@app.route('/')
def index():
    """Homepage with OpenStreetMap and project markers"""
    projects = Project.get_all()
    return render_template('index.html', projects=projects)

@app.route('/project/<project_id>')
def project_detail(project_id):
    """Project detail page with OpenStreetMap integration"""
    project = Project.get_by_id(project_id)
    if not project:
        return render_template('404.html'), 404
    return render_template('project.html', project=project)

@app.route('/api/projects')
def api_projects():
    """API endpoint for project data (for JavaScript consumption)"""
    projects = Project.get_all()
    return jsonify(projects)

@app.route('/api/project/<project_id>')
def api_project(project_id):
    """API endpoint for single project data"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project)

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.verify_password(username, password)
        if admin:
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    projects = Project.get_all()
    return render_template('admin/dashboard.html', projects=projects)

@app.route('/admin/project/new', methods=['GET', 'POST'])
@login_required
def admin_project_new():
    """Create new project"""
    if request.method == 'POST':
        project_data = {
            'title': request.form.get('title'),
            'location': request.form.get('location'),
            'lat': float(request.form.get('lat', 0)),
            'lng': float(request.form.get('lng', 0)),
            'type': request.form.get('type'),
            'description': request.form.get('description'),
            'status': request.form.get('status'),
            'year': int(request.form.get('year', 2024)),
            'details': {
                'duration': request.form.get('duration'),
                'team_size': request.form.get('team_size'),
                'area': request.form.get('area'),
                'findings': request.form.getlist('findings[]'),
                'features': request.form.getlist('features[]'),
                'techniques': request.form.getlist('techniques[]')
            },
            'images': request.form.getlist('images[]')
        }
        
        project = Project(project_data)
        project_id = project.save()
        
        if project_id:
            flash('Project created successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Error creating project', 'error')
    
    return render_template('admin/project_form.html', project=None)

@app.route('/admin/project/<project_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_project_edit(project_id):
    """Edit existing project"""
    project = Project.get_by_id(project_id)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        project_data = {
            'title': request.form.get('title'),
            'location': request.form.get('location'),
            'lat': float(request.form.get('lat', 0)),
            'lng': float(request.form.get('lng', 0)),
            'type': request.form.get('type'),
            'description': request.form.get('description'),
            'status': request.form.get('status'),
            'year': int(request.form.get('year', 2024)),
            'details': {
                'duration': request.form.get('duration'),
                'team_size': request.form.get('team_size'),
                'area': request.form.get('area'),
                'findings': request.form.getlist('findings[]'),
                'features': request.form.getlist('features[]'),
                'techniques': request.form.getlist('techniques[]')
            },
            'images': request.form.getlist('images[]')
        }
        
        updated_project = Project(project_data, project_id)
        if updated_project.save():
            flash('Project updated successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Error updating project', 'error')
    
    return render_template('admin/project_form.html', project=project)

@app.route('/admin/project/<project_id>/delete', methods=['POST'])
@login_required
def admin_project_delete(project_id):
    """Delete project"""
    if Project.delete(project_id):
        flash('Project deleted successfully', 'success')
    else:
        flash('Error deleting project', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/migrate')
@login_required
def admin_migrate():
    """Migrate data from data.py to Firestore (one-time operation)"""
    try:
        from models import migrate_data_to_firestore
        migrate_data_to_firestore()
        flash('Data migration completed successfully', 'success')
    except Exception as e:
        flash(f'Migration error: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))
