# Portfolio Website - Construction & Archaeology Projects

## Overview

This is a Flask web application that showcases construction and archaeology projects on an interactive map interface. The application displays project locations using both Google Maps and OpenStreetMap (via Leaflet.js), allowing users to explore projects geographically and view detailed information about each one.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask
- **CSS Framework**: Bootstrap 5 with dark theme
- **JavaScript Libraries**: 
  - Google Maps API for main map interface
  - Leaflet.js for detailed project pages with OpenStreetMap
  - Font Awesome for icons
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **WSGI Server**: Gunicorn for production deployment
- **Data Layer**: Static data structure (in `data.py`) - designed to be easily replaced with database
- **Session Management**: Flask sessions with configurable secret key

### Data Storage
- **Current**: Static Python data structures in `data.py`
- **Designed for**: Database integration (PostgreSQL packages installed)
- **Structure**: Projects with geographical coordinates, metadata, and image galleries

## Key Components

### Core Application Files
- `main.py`: Application entry point
- `app.py`: Flask app initialization and configuration
- `routes.py`: URL routing and view functions
- `data.py`: Data layer with project information

### Frontend Components
- `templates/base.html`: Base template with navigation and common elements
- `templates/index.html`: Main page with map and project sidebar
- `templates/project.html`: Detailed project view page
- `static/js/maps.js`: Google Maps integration
- `static/js/leaflet-maps.js`: OpenStreetMap/Leaflet integration
- `static/css/style.css`: Custom styling

### API Endpoints
- `/api/projects`: JSON endpoint for all projects
- `/api/project/<id>`: JSON endpoint for individual project data

## Data Flow

1. **Homepage Load**: 
   - Flask renders `index.html` with project data
   - Google Maps initializes and places markers for each project
   - Sidebar displays filterable project list

2. **Project Interaction**:
   - Users can filter projects by type (Construction/Archaeology)
   - Clicking projects in sidebar highlights map markers
   - Map markers show popup windows with project previews

3. **Project Details**:
   - Individual project pages use Leaflet.js for detailed mapping
   - OpenStreetMap provides detailed local context
   - Full project information including image galleries and specifications

## External Dependencies

### Map Services
- **Google Maps API**: Primary map interface (API key configurable)
- **OpenStreetMap**: Secondary mapping via Leaflet.js (no API key required)
- **Unsplash**: Image hosting for project galleries

### Python Packages
- `Flask`: Web framework
- `Gunicorn`: WSGI HTTP server
- `psycopg2-binary`: PostgreSQL adapter (for future database integration)
- `email-validator`: Email validation utilities
- `werkzeug`: WSGI utilities and middleware

### CDN Resources
- Bootstrap 5 CSS/JS
- Font Awesome icons
- Leaflet.js mapping library

## Deployment Strategy

### Development
- Flask development server with debug mode
- Auto-reload on code changes
- Environment variables for configuration

### Production
- Gunicorn WSGI server with autoscale deployment
- ProxyFix middleware for proper header handling
- Configurable session secrets via environment variables

### Infrastructure
- **Platform**: Replit with Nix package management
- **Database Ready**: PostgreSQL packages pre-installed
- **Scalability**: Autoscale deployment target configured

## Recent Changes
- June 25, 2025: Converted from Google Maps to OpenStreetMap using Leaflet.js
- June 25, 2025: Integrated Firestore database for dynamic project management
- June 25, 2025: Added complete admin panel with authentication
- June 25, 2025: Implemented security configurations and deployment setup
- June 25, 2025: Created comprehensive deployment guide with security best practices

## Admin Panel Features
- Secure login system with Flask-Login
- Full CRUD operations for projects
- Data migration from static files to Firestore
- Project filtering and management interface
- Responsive admin dashboard

## Security Implementation
- Environment-based configuration management
- Secure session handling with configurable cookies
- Security headers for production deployment
- Admin authentication with customizable credentials
- HTTPS-ready configuration for production

## Database Architecture
- **Firestore Collections**:
  - `projects`: Stores all project data with geographic coordinates, metadata, and images
- **Models**: Project and Admin classes with full CRUD operations
- **Migration**: Utility to migrate sample data to Firestore

## Deployment Ready
- Production-ready configuration with Gunicorn
- Environment variable management
- Security headers and HTTPS support
- Comprehensive deployment guide for both Replit and VPS hosting

## User Preferences

Preferred communication style: Simple, everyday language.
User wants: Firestore database integration, admin panel for project management, secure hosting setup.