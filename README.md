# MCP Chat API

A FastAPI-based chat API with a well-organized, scalable structure.

## Project Structure

```
app/
├── __init__.py              # Package initialization
├── main.py                  # FastAPI application entry point
├── api/                     # API layer
│   ├── __init__.py
│   ├── dependencies.py      # Dependency injection
│   └── routes/              # API route handlers
│       ├── __init__.py      # Route aggregation
│       └── chat.py          # Chat endpoints
├── core/                    # Core configuration
│   ├── __init__.py
│   └── config.py            # Application settings
├── db/                      # Database configuration
│   └── __init__.py
├── models/                  # Database models (ORM)
│   └── __init__.py
├── schemas/                 # Pydantic schemas
│   ├── __init__.py
│   └── chat.py              # Chat-related schemas
├── services/                # Business logic
│   ├── __init__.py
│   └── chat_service.py      # Chat service implementation
├── middleware/              # Custom middleware
│   └── __init__.py
└── utils/                   # Utility functions
    ├── __init__.py
    └── logger.py            # Logging configuration
```

## Getting Started

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file (optional):
```bash
# Copy from example if it exists, or create manually
APP_NAME=MCP Chat API
DEBUG=False
ALLOWED_ORIGINS=http://localhost:5173
```

### Running the Application

Development mode with auto-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Production mode:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Chat Endpoints (v1)
- `POST /api/v1/chat/` - Send a chat message
- `POST /api/v1/chat/sessions` - Create a new chat session
- `GET /api/v1/chat/sessions` - List all sessions
- `GET /api/v1/chat/sessions/{session_id}` - Get a specific session
- `DELETE /api/v1/chat/sessions/{session_id}` - Delete a session
- `GET /api/v1/chat/sessions/{session_id}/messages` - Get session messages

## Development

### Architecture

The application follows a layered architecture:

1. **API Layer** (`app/api/`): HTTP endpoints and request/response handling
2. **Service Layer** (`app/services/`): Business logic and orchestration
3. **Data Layer** (`app/models/`, `app/db/`): Data models and database access
4. **Schema Layer** (`app/schemas/`): Request/response validation with Pydantic

### Adding New Endpoints

1. Create a schema in `app/schemas/`
2. Add business logic in `app/services/`
3. Create route handler in `app/api/routes/`
4. Register the router in `app/api/routes/__init__.py`

### Configuration

Application settings are managed through `app/core/config.py` using `pydantic-settings`.
Settings can be overridden via environment variables or a `.env` file.

### Database Integration

To add database support:

1. Uncomment database settings in `app/core/config.py`
2. Add SQLAlchemy models in `app/models/`
3. Configure database connection in `app/db/__init__.py`
4. Update services to use database instead of in-memory storage

## Testing

Run tests with pytest:
```bash
pytest
```

Create tests in a `tests/` directory following the same structure as `app/`.

## Next Steps

- [ ] Integrate with actual AI/MCP backend
- [ ] Add authentication and authorization
- [ ] Implement database persistence
- [ ] Add rate limiting
- [ ] Set up logging and monitoring
- [ ] Add comprehensive tests
- [ ] Configure deployment (Docker, etc.)

## License

[Your License Here]


