import csv
from datetime import datetime
from app import app, db
from models import Episode, Guest, Appearance

def parse_raw_date(raw_date):
    """Convert dates like '1/11/99' to '1999-01-11'"""
    month, day, year = raw_date.split('/')
    year = f"19{year}" if int(year) > 50 else f"20{year}"
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Track seen guests to avoid duplicates
        seen_guests = {}
        guest_id = 1
        episode_id = 1

        # Process raw data
        with open('raw_guests.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Create episode
                episode = Episode(
                    id=episode_id,
                    date=parse_raw_date(row['Raw_Guest_List']),
                    number=int(row['YEAR'])
                )
                db.session.add(episode)

                # Create guest if not seen before
                guest_name = row['Raw_Guest_List']
                if guest_name not in seen_guests:
                    guest = Guest(
                        id=guest_id,
                        name=guest_name,
                        occupation=row['GoogleKnowlege_OccupationShow'],
                        group=row['Group']
                    )
                    seen_guests[guest_name] = guest_id
                    db.session.add(guest)
                    guest_id += 1

                # Create appearance
                appearance = Appearance(
                    id=episode_id,
                    rating=3,  # Default rating
                    episode_id=episode_id,
                    guest_id=seen_guests[guest_name]
                )
                episode_id += 1

        db.session.commit()
        print("Database seeded successfully with raw data!")

if __name__ == "__main__":
    seed_database()

