# Spotify-like Music Streaming Backend

A production-ready FastAPI backend with PostgreSQL, SQLAlchemy 2.0, Pydantic, and role-based authorization.

## Features

- Artist and Song CRUD
- PostgreSQL synchronous database connection
- Role-based access via `x-user-role` and `x-user-id`
- Admin-only endpoints
- Pagination and search with PostgreSQL ILIKE
- Swagger / OpenAPI support with Authorize button for `x-user-role`
- Standard response format:

```json
{
  "success": true,
  "data": ..., 
  "message": "optional"
}
```

## 📊 Architecture & Flow Diagrams

See **[DIAGRAMS.md](DIAGRAMS.md)** for comprehensive flow diagrams including:
- Application Request Flow
- Architecture Layers
- Database Relationships
- Complete Request Sequence
- Authorization Flow

## Setup

1. Create and activate virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Copy the example env file and update the database URL

```powershell
copy .env.example .env
```

4. Start the app

```powershell

.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
or

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
uvicorn app.main:app --reload
```

## Access the Application

Once the server is running, access it at:

- **API Base URL:** http://127.0.0.1:8000
- **Swagger UI (Interactive Docs):** http://127.0.0.1:8000/docs
- **ReDoc (Alternative Docs):** http://127.0.0.1:8000/redoc
- **Health Check:** http://127.0.0.1:8000/

## Environment

Set `DATABASE_URL` to a PostgreSQL connection string.

Example:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/spotify_db
```

The application will normalize this to use the async driver automatically.

## API Endpoints

### Public

- `GET /artists`
- `GET /artists/{id}`
- `GET /artists/search?name=`
- `GET /artists/{id}/songs`
- `GET /songs`
- `GET /songs/{id}`
- `GET /songs/search?title=`
- `GET /songs/{id}/stream`

### Admin Only

- `POST /artists`
- `PUT /artists/{id}`
- `DELETE /artists/{id}`
- `POST /songs`
- `PUT /songs/{id}`
- `DELETE /songs/{id}`
- `GET /songs/admin/songs`

## Authorization

Use header `x-user-role` for Swagger and route authorization.
- `admin` → full access
- otherwise → read-only

## Sample Requests

### List artists

```powershell
curl "http://127.0.0.1:8000/artists?limit=10&offset=0" -H "x-user-role: user"
```

### Create an artist (admin)

```powershell
curl -X POST "http://127.0.0.1:8000/artists" -H "Content-Type: application/json" -H "x-user-role: admin" -d "{\"name\": \"Ariana Grande\"}"
```

### Search songs

```powershell
curl "http://127.0.0.1:8000/songs/search?title=love" -H "x-user-role: user"
```

### Play a song stream

```powershell
curl "http://127.0.0.1:8000/songs/1/stream" -H "x-user-role: user"
```

### Protected admin route

```powershell
curl "http://127.0.0.1:8000/songs/admin/songs" -H "x-user-role: admin"
```
