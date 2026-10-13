
from app import create_app
from app.extensions import db
from app.models import Equipment

app = create_app()

sample_equipment = [
    {
        "name": "Raspberry Pi kits",
        "category": "Computing",
        "description": "For programming, embedded systems, and hardware experiments.",
    },
    {
        "name": "Arduino kits",
        "category": "Electronics",
        "description": "For programming, embedded systems, and hardware experiments.",
    },
    {
        "name": "Oscilloscopes",
        "category": "Electronics",
        "description": "For observing and analysing electrical signals.",
    },
    {
        "name": "VR headsets",
        "category": "Virtual Reality",
        "description": "For immersive computing and virtual-reality experiments.",
    },
    {
        "name": "3D printing equipment",
        "category": "Manufacturing",
        "description": "For producing three-dimensional prototypes and models.",
    },
]

with app.app_context():
    for item in sample_equipment:
        existing = Equipment.query.filter_by(name=item["name"]).first()

        if existing is None:
            db.session.add(Equipment(**item))

    db.session.commit()
    print("Sample equipment added successfully!")
