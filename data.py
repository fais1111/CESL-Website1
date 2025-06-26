# Project data structure
# In a real application, this would come from a database

PROJECTS = [
    {
        'id': 1,
        'title': 'Ancient Roman Villa Excavation',
        'location': 'Rome, Italy',
        'lat': 41.9028,
        'lng': 12.4964,
        'type': 'Archaeology',
        'description': 'Comprehensive archaeological excavation of a 2nd-century Roman villa discovered during urban development. The project involved careful documentation of mosaics, frescoes, and structural remains.',
        'details': {
            'duration': '18 months',
            'team_size': '12 archaeologists',
            'area': '2,500 sq meters',
            'findings': [
                'Well-preserved mosaic floors',
                'Ancient heating system (hypocaust)',
                'Ceramic artifacts dating to 150-200 CE',
                'Coin collection from Marcus Aurelius era'
            ],
            'techniques': [
                'Stratigraphic excavation',
                '3D photogrammetry',
                'Ground-penetrating radar',
                'Artifact conservation'
            ]
        },
        'images': [
            'https://images.unsplash.com/photo-1539650116574-75c0c6d73d0e?w=800',
            'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
            'https://images.unsplash.com/photo-1544963950-c3db7e463bb2?w=800'
        ],
        'status': 'Completed',
        'year': 2023
    },
    {
        'id': 2,
        'title': 'Sustainable Office Complex',
        'location': 'Berlin, Germany',
        'lat': 52.5200,
        'lng': 13.4050,
        'type': 'Construction',
        'description': 'Modern 15-story office complex featuring sustainable design principles, renewable energy systems, and green building certification.',
        'details': {
            'duration': '24 months',
            'team_size': '45 construction workers',
            'area': '25,000 sq meters',
            'features': [
                'LEED Platinum certification',
                'Solar panel installation',
                'Rainwater harvesting system',
                'Green roof gardens'
            ],
            'techniques': [
                'Prefabricated construction',
                'BIM modeling',
                'Sustainable materials',
                'Energy-efficient systems'
            ]
        },
        'images': [
            'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800',
            'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800',
            'https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800'
        ],
        'status': 'Completed',
        'year': 2024
    },
    {
        'id': 3,
        'title': 'Medieval Castle Restoration',
        'location': 'Edinburgh, Scotland',
        'lat': 55.9533,
        'lng': -3.1883,
        'type': 'Construction',
        'description': 'Restoration of a 13th-century castle including structural reinforcement, historical preservation, and visitor facility development.',
        'details': {
            'duration': '36 months',
            'team_size': '25 specialists',
            'area': '5,000 sq meters',
            'features': [
                'Stone masonry restoration',
                'Medieval timber reconstruction',
                'Museum facility integration',
                'Accessibility improvements'
            ],
            'techniques': [
                'Traditional stonework',
                'Lime mortar applications',
                'Historical documentation',
                'Structural engineering'
            ]
        },
        'images': [
            'https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=800',
            'https://images.unsplash.com/photo-1520637836862-4d197d17c35a?w=800',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'
        ],
        'status': 'In Progress',
        'year': 2024
    },
    {
        'id': 4,
        'title': 'Prehistoric Settlement Site',
        'location': 'Stonehenge, England',
        'lat': 51.1789,
        'lng': -1.8262,
        'type': 'Archaeology',
        'description': 'Excavation of a Neolithic settlement site near Stonehenge, revealing insights into prehistoric life and ritual practices.',
        'details': {
            'duration': '12 months',
            'team_size': '15 archaeologists',
            'area': '1,200 sq meters',
            'findings': [
                'Neolithic pottery fragments',
                'Stone tool assemblages',
                'Post-hole evidence of structures',
                'Burial remains with grave goods'
            ],
            'techniques': [
                'Single context recording',
                'Environmental sampling',
                'Radiocarbon dating',
                'Specialist analysis'
            ]
        },
        'images': [
            'https://images.unsplash.com/photo-1599662875272-64de8289f6d5?w=800',
            'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=800',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800'
        ],
        'status': 'Completed',
        'year': 2023
    },
    {
        'id': 5,
        'title': 'Residential Tower Complex',
        'location': 'Dubai, UAE',
        'lat': 25.2048,
        'lng': 55.2708,
        'type': 'Construction',
        'description': 'Luxury residential towers with innovative design, smart home technology, and sustainable features in the heart of Dubai.',
        'details': {
            'duration': '30 months',
            'team_size': '60 construction workers',
            'area': '40,000 sq meters',
            'features': [
                'Smart home automation',
                'Infinity pool systems',
                'High-speed elevators',
                'Panoramic city views'
            ],
            'techniques': [
                'High-rise construction',
                'Curtain wall installation',
                'MEP systems integration',
                'Quality control testing'
            ]
        },
        'images': [
            'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800',
            'https://images.unsplash.com/photo-1577495508048-b635879837f1?w=800',
            'https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=800'
        ],
        'status': 'In Progress',
        'year': 2024
    },
    {
        'id': 6,
        'title': 'Ancient Temple Complex',
        'location': 'Athens, Greece',
        'lat': 37.9755,
        'lng': 23.7348,
        'type': 'Archaeology',
        'description': 'Excavation and study of a classical Greek temple complex with associated structures and artifacts from the 5th century BCE.',
        'details': {
            'duration': '24 months',
            'team_size': '20 archaeologists',
            'area': '3,000 sq meters',
            'findings': [
                'Marble architectural elements',
                'Votive offerings and sculptures',
                'Inscribed stone tablets',
                'Classical pottery assemblages'
            ],
            'techniques': [
                'Architectural recording',
                'Epigraphic analysis',
                'Ceramic typology',
                'Conservation treatments'
            ]
        },
        'images': [
            'https://images.unsplash.com/photo-1555993539-1732b0258235?w=800',
            'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
            'https://images.unsplash.com/photo-1544963950-c3db7e463bb2?w=800'
        ],
        'status': 'Completed',
        'year': 2023
    }
]

def get_all_projects():
    """Return all projects"""
    return PROJECTS

def get_project_by_id(project_id):
    """Return a specific project by ID"""
    for project in PROJECTS:
        if project['id'] == project_id:
            return project
    return None

def get_projects_by_type(project_type):
    """Return projects filtered by type"""
    return [project for project in PROJECTS if project['type'].lower() == project_type.lower()]
