import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask_login import UserMixin
import bcrypt
from dotenv import load_dotenv


load_dotenv()
# Initialize Firebase Admin SDK
db = None
firebase_initialized = False

try:
    if not firebase_admin._apps:
        # Use project ID from environment variables
        project_id = os.environ.get('FIREBASE_PROJECT_ID')
        if project_id:
            # For Replit environment, use default credentials
            firebase_admin.initialize_app()
            print(f"Firebase initialized with project: {project_id}")
            firebase_initialized = True
        else:
            print("Warning: FIREBASE_PROJECT_ID not set, using static data fallback")
    
    # Initialize Firestore client only if Firebase is initialized
    if firebase_initialized:
        db = firestore.client()
        print("Firestore client initialized successfully")
        
except Exception as e:
    print(f"Firebase/Firestore initialization error: {e}")
    print("Continuing with static data fallback")
    db = None

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
        """Get all projects from Firestore or fallback to static data"""
        if db is None:
            # Fallback to static data if Firestore is not available
            from data import get_all_projects
            return get_all_projects()
        
        try:
            # Set a timeout for Firestore operations
            projects_ref = db.collection('projects')
            docs = list(projects_ref.limit(100).stream())
            
            projects = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                projects.append(data)
            
            # If no projects in Firestore, fallback to static data
            if not projects:
                print("No projects found in Firestore, using static data")
                from data import get_all_projects
                return get_all_projects()
                
            return projects
        except Exception as e:
            print(f"Error fetching projects from Firestore: {e}")
            # Fallback to static data
            from data import get_all_projects
            return get_all_projects()
    
    @staticmethod
    def get_by_id(project_id):
        """Get a specific project by ID from Firestore or fallback to static data"""
        if db is None:
            # Fallback to static data
            from data import get_project_by_id
            try:
                return get_project_by_id(int(project_id))
            except (ValueError, TypeError):
                return None
        
        try:
            doc_ref = db.collection('projects').document(project_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            
            # Try fallback to static data if not found in Firestore
            from data import get_project_by_id
            try:
                return get_project_by_id(int(project_id))
            except (ValueError, TypeError):
                return None
                
        except Exception as e:
            print(f"Error fetching project {project_id} from Firestore: {e}")
            # Fallback to static data
            from data import get_project_by_id
            try:
                return get_project_by_id(int(project_id))
            except (ValueError, TypeError):
                return None
    
    def save(self):
        """Save project to Firestore"""
        if db is None:
            print("Firestore not available - cannot save project")
            return None
            
        try:
            if hasattr(self, 'id') and self.id:
                # Update existing project
                doc_ref = db.collection('projects').document(self.id)
                doc_ref.update(self.to_dict())
                return self.id
            else:
                # Create new project
                doc_ref = db.collection('projects').add(self.to_dict())
                self.id = doc_ref[1].id
                return self.id
        except Exception as e:
            print(f"Error saving project: {e}")
            return None
    
    @staticmethod
    def delete(project_id):
        """Delete project from Firestore"""
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
        """Verify admin credentials"""
        # In production, store hashed passwords in environment variables
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if username == admin_username and password == admin_password:
            return Admin(username)
        return None
    
    @staticmethod
    def get(username):
        """Get admin user by username"""
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        if username == admin_username:
            return Admin(username)
        return None

# Migration function to move data from data.py to Firestore
def migrate_data_to_firestore():
    """Migrate sample data to Firestore (run once)"""
    from data import PROJECTS
    
    try:
        for project_data in PROJECTS:
            project = Project(project_data)
            project.save()
            print(f"Migrated project: {project.title}")
        print("Data migration completed successfully!")
    except Exception as e:
        print(f"Error during migration: {e}")