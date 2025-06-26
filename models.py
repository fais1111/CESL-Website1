from config import db
from flask_login import UserMixin
import os

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
            print("Firestore not available - fallback to static data")
            from data import get_all_projects
            return get_all_projects()
        try:
            projects_ref = db.collection('projects')
            docs = list(projects_ref.limit(100).stream())
            projects = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                projects.append(data)
            return projects or get_all_projects()
        except Exception as e:
            print(f"Firestore error: {e}")
            from data import get_all_projects
            return get_all_projects()
    
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
            print(f"Error deleting project: {e}")
            return False

class Admin(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

    @staticmethod
    def verify_password(username, password):
        admin_user = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_pass = os.environ.get('ADMIN_PASSWORD', 'admin123')
        if username == admin_user and password == admin_pass:
            return Admin(username)
        return None

    @staticmethod
    def get(username):
        if username == os.environ.get('ADMIN_USERNAME'):
            return Admin(username)
        return None
