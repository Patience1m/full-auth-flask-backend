from faker import Faker
from app import create_app
from extension import db
from models.note import Note
from models.user import User

fake = Faker()
Faker.seed(42)

USERNAMES = ["wanjiru", "otieno", "amina"]
PASSWORD = "password123"
NOTES_PER_USER = 8

app = create_app("development")

with app.app_context():
    print("Clearing existing data...")
    Note.query.delete()
    User.query.delete()
    db.session.commit()
    print("Seeding users...")
    users = []
    for username in USERNAMES:
        user = User(username=username)
        user.set_password(PASSWORD)
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    print("Seeding notes...")
    for user in users:
        for _ in range(NOTES_PER_USER):
            db.session.add(Note(
                title=fake.sentence(nb_words=4).rstrip("."),
                content=fake.paragraph(nb_sentences=3),
                user_id=user.id,
            ))
    db.session.commit()

    print(
        f"Done: {User.query.count()} users, {Note.query.count()} notes. "
        f"Every seeded user has the password: {PASSWORD}"
    )
