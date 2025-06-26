import os
from flask import (
    render_template, jsonify, request, redirect, url_for, flash
)
from flask_login import login_required, login_user, logout_user, current_user
from main import app
from models import Project, Admin

# --- Public Routes ---

@app.route('/')
def index():
    """Homepage showing map and all projects"""
    projects = Project.get_all()
    return render_template('index.html', projects=projects)

@app.route('/project/<project_id>')
def project_detail(project_id):
    """Project detail view"""
    project = Project.get_by_id(project_id)
    if not project:
        return render_template('404.html'), 404
    return render_template('project.html', project=project)

@app.route('/api/projects')
def api_projects():
    """API endpoint: All projects"""
    return jsonify(Project.get_all())

@app.route('/api/project/<project_id>')
def api_project(project_id):
    """API endpoint: Single project by ID"""
    project = Project.get_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project)

# --- Admin Authentication ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.verify_password(username, password)

        if admin:
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(request.args.get('next') or url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# --- Admin Dashboard & CRUD ---

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard with list of projects"""
    projects = Project.get_all()
    return render_template('admin/dashboard.html', projects=projects)

@app.route('/admin/project/new', methods=['GET', 'POST'])
@login_required
def admin_project_new():
    """Create a new project"""
    if request.method == 'POST':
        project_data = parse_project_form(request)
        project = Project(project_data)
        if project.save():
            flash('Project created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Failed to create project.', 'danger')

    return render_template('admin/project_form.html', project=None)

@app.route('/admin/project/<project_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_project_edit(project_id):
    """Edit a project"""
    project = Project.get_by_id(project_id)
    if not project:
        flash('Project not found', 'danger')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        updated_data = parse_project_form(request)
        updated_project = Project(updated_data, project_id)
        if updated_project.save():
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Failed to update project.', 'danger')

    return render_template('admin/project_form.html', project=project)

@app.route('/admin/project/<project_id>/delete', methods=['POST'])
@login_required
def admin_project_delete(project_id):
    """Delete a project"""
    if Project.delete(project_id):
        flash('Project deleted.', 'success')
    else:
        flash('Failed to delete project.', 'danger')

    return redirect(url_for('admin_dashboard'))

@app.route('/admin/migrate')
@login_required
def admin_migrate():
    """One-time migration of local data to Firestore"""
    try:
        from models import migrate_data_to_firestore
        migrate_data_to_firestore()
        flash('Data migration completed.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# --- Utility function ---

def parse_project_form(req):
    """Parse project form data into a dict safely"""
    def safe_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def safe_int(value, default=2024):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    # Defensive fetch of list form fields
    def safe_list(key):
        vals = req.form.getlist(key)
        return vals if vals else []

    return {
        'title': req.form.get('title', ''),
        'location': req.form.get('location', ''),
        'lat': safe_float(req.form.get('lat')),
        'lng': safe_float(req.form.get('lng')),
        'type': req.form.get('type', ''),
        'description': req.form.get('description', ''),
        'status': req.form.get('status', ''),
        'year': safe_int(req.form.get('year')),
        'details': {
            'duration': req.form.get('duration', ''),
            'team_size': req.form.get('team_size', ''),
            'area': req.form.get('area', ''),
            'findings': safe_list('findings[]'),
            'features': safe_list('features[]'),
            'techniques': safe_list('techniques[]')
        },
        'images': safe_list('images[]')
    }
