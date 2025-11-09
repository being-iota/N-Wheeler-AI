# 🚀 Setup Guide

## Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** 18+ and npm
- **Python** 3.10+
- **PostgreSQL** 12+
- **MongoDB** 4.4+
- **Redis** 6.0+

## Step 1: Database Setup

### PostgreSQL Setup

1. Create a database:
```bash
createdb vehicle_maintenance
```

2. Update `backend/.env` with your PostgreSQL credentials:
```
DATABASE_URL=postgresql://username:password@localhost:5432/vehicle_maintenance
```

### MongoDB Setup

1. Start MongoDB:
```bash
mongod
```

2. Update `backend/.env` with your MongoDB URL:
```
MONGODB_URL=mongodb://localhost:27017/telematics
```

### Redis Setup

1. Start Redis:
```bash
redis-server
```

2. Update `backend/.env` with your Redis URL:
```
REDIS_URL=redis://localhost:6379
```

## Step 2: Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

6. Update `.env` with your configuration:
   - Set `OPENAI_API_KEY` (optional, for chatbot functionality)
   - Update database URLs if needed
   - Set `JWT_SECRET` for authentication

7. Initialize the database:
```bash
python -c "from database.connection import init_db; import asyncio; asyncio.run(init_db())"
```

## Step 3: Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file from `.env.example`:
```bash
cp .env.example .env.local
```

4. Update `.env.local` with your API URL (default should work):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## Step 4: Running the Application

### Start Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Activate virtual environment (if not already active):
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Start Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Start the Next.js development server:
```bash
npm run dev
```

The frontend will be available at: http://localhost:3000

### Start Celery Worker (Optional)

For background tasks, start Celery worker:

1. Navigate to backend directory:
```bash
cd backend
```

2. Activate virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Start Celery worker:
```bash
celery -A tasks.celery_app worker --loglevel=info
```

## Step 5: Verify Installation

1. Check backend health:
```bash
curl http://localhost:8000/health
```

2. Check frontend:
   - Open http://localhost:3000 in your browser
   - You should see the Vehicle Maintenance AI System dashboard

3. Test API:
   - Visit http://localhost:8000/docs for interactive API documentation
   - Try the `/api/v1/vehicles` endpoint to see demo vehicles

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL, MongoDB, and Redis are running
- Check that database credentials in `.env` are correct
- Verify that databases exist (PostgreSQL database should be created manually)

### Port Already in Use

- Backend uses port 8000 by default
- Frontend uses port 3000 by default
- Change ports in configuration if needed

### OpenAI API Key

- The system works without OpenAI API key (uses fallback responses)
- For full chatbot functionality, add your OpenAI API key to `backend/.env`

### ML Models

- Models are created automatically on first run
- Model files are saved in `backend/models/` directory
- Models are trained on synthetic data for demonstration

## Next Steps

1. Explore the dashboard at http://localhost:3000
2. Try the chatbot interface
3. Schedule a maintenance appointment
4. View real-time telematics data
5. Check alerts and predictions

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Formatting

```bash
# Backend
cd backend
black .
isort .

# Frontend
cd frontend
npm run lint
```

## Production Deployment

For production deployment:

1. Set `NODE_ENV=production` for frontend
2. Use a production WSGI server for backend (e.g., Gunicorn)
3. Set up proper database backups
4. Configure environment variables securely
5. Enable HTTPS
6. Set up monitoring and logging

## Support

For issues or questions, please check the README.md or create an issue in the repository.

