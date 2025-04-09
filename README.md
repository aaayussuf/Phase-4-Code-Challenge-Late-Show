# Late Show API

A Flask REST API for managing episodes, guests, and appearances on a late night talk show.

## Features
- CRUD operations for episodes, guests, and appearances
- Relationships between episodes and guests through appearances
- Rating system for guest appearances (1-5 scale)
- Database migrations using Flask-Migrate

## Setup

### Prerequisites
- Python 3.8+
- pip
- SQLite (for development)

### Installation
1. Clone the repository  git@github.com:aaayussuf/Phase-4-Code-Challenge-Late-Show.git
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize and seed the database:
   ```bash
   flask db upgrade  # Run migrations
   python seed.py    # Seed sample data
   ```
5. Run the application:
   ```bash
   python app.py
   ```

## API Documentation

### Base URL
`http://localhost:5000`

### Endpoints

#### Episodes
- `GET /episodes` - List all episodes
- `GET /episodes/:id` - Get specific episode with appearances
- `POST /episodes` - Create new episode
- `PATCH /episodes/:id` - Update episode
- `DELETE /episodes/:id` - Delete episode

#### Guests
- `GET /guests` - List all guests
- `GET /guests/:id` - Get specific guest with appearances
- `POST /guests` - Create new guest
- `PATCH /guests/:id` - Update guest
- `DELETE /guests/:id` - Delete guest

#### Appearances
- `GET /appearances` - List all appearances
- `GET /appearances/:id` - Get specific appearance
- `POST /appearances` - Create new appearance
- `PATCH /appearances/:id` - Update appearance
- `DELETE /appearances/:id` - Delete appearance

### Example Requests

#### Get Episode with Appearances
```bash
GET /episodes/1
```

Response:
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "guest_id": 1,
      "episode_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

#### Create Appearance
```bash
POST /appearances
Content-Type: application/json

{
  "rating": 5,
  "episode_id": 1,
  "guest_id": 1
}
```

Response:
```json
{
  "id": 1,
  "rating": 5,
  "guest_id": 1,
  "episode_id": 1,
  "episode": {
    "date": "1/11/99",
    "id": 1,
    "number": 1
  },
  "guest": {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  }
}
```

## Database Schema

### Tables
- **episodes**
  - id (Integer, PK)
  - date (String)
  - number (Integer)

- **guests**
  - id (Integer, PK)
  - name (String)
  - occupation (String)

- **appearances**
  - id (Integer, PK)
  - rating (Integer, 1-5)
  - episode_id (Integer, FK to episodes.id)
  - guest_id (Integer, FK to guests.id)

## Development

### Running Tests
```bash
python -m pytest
```

### Database Migrations
To create a new migration after model changes:
```bash
flask db migrate -m "description of changes"
flask db upgrade
```

### Seeding Data
Edit `seed.py` to modify sample data, then run:
```bash
python seed.py
```

## License
MIT
