import os
from flask_login import UserMixin
from config import db
import bcrypt

class Project:
    def __init__(self, data=None, doc_id=None):
        if data:
            self.id = doc_id or data.get('id')
            self.title = data.get('title', '')
            self.location = data.get('location', '')
            self.lat = data.get('lat', 0.0)
            self.lng = data.get('lng', 0.0)
            self.type = data.get('type', '')
            self.description = data.get('description', '')
            self.details = data.get('details', {})
            self.images = data.get('images', [])
            self.status = data.get('status', '')
            self.year = data.get('year', 2024)

    def to_dict(self):
        return {
            'title': self.title,
            'location': self.location,
            'lat': self.lat,
            'lng': self.lng,
            'type': self.type,
            'description': self.description,
            'details': self.details,
            'images': self.images,
            'status': self.status,
            'year': self.year
        }

    @staticmethod
    def get_all():
        if db is None:
            from data import get_all_projects
            return get_all_projects()

        try:
            docs = list(db.collection('projects').limit(100).stream())
            projects = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                projects.append(data)
            if not projects:
                from data import get_all_projects
                return get_all_projects()
            return projects
        except Exception as e:
            print(f"Error fetching projects: {e}")
            from data import get_all_projects
            return get_all_projects()

    @staticmethod
    def get_by_id(project_id):
        if db is None:
            from data import get_project_by_id
            try:
                return get_project_by_id(int(project_id))
            except (ValueError, TypeError):
                return None

        try:
            doc = db.collection('projects').document(project_id).get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            from data import get_project_by_id
            return get_project_by_id(int(project_id))
        except Exception as e:
            print(f"Error getting project {project_id}: {e}")
            from data import get_project_by_id
            return get_project_by_id(int(project_id))

    def save(self):
        if db is None:
            print("Firestore not available - cannot save project")
            return None

        try:
            if self.id:
                db.collection('projects').document(self.id).update(self.to_dict())
                return self.id
            else:
                doc_ref = db.collection('projects').add(self.to_dict())
                self.id = doc_ref[1].id
                return self.id
        except Exception as e:
            print(f"Error saving project: {e}")
            return None

    @staticmethod
    def delete(project_id):
        if db is None:
            print("Firestore not available - cannot delete project")
            return False

        try:
            db.collection('projects').document(project_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting project {project_id}: {e}")
            return False

class Admin(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

    @staticmethod
    def verify_password(username, password):
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        if username == admin_username and password == admin_password:
            return Admin(username)
        return None

    @staticmethod
    def get(username):
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        if username == admin_username:
            return Admin(username)
        return None
