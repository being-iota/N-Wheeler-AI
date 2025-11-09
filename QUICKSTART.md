# 🚀 Quick Start Guide

Get the Vehicle Maintenance AI System up and running in minutes!

## Prerequisites Check

Ensure you have installed:
- ✅ Node.js 18+
- ✅ Python 3.10+
- ✅ PostgreSQL (running)
- ✅ MongoDB (running)
- ✅ Redis (running)

## Quick Setup (5 minutes)

### 1. Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database
python init_db.py
```

### 2. Frontend Setup (1 minute)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
```

### 3. Start Services (2 minutes)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Access the Application

- 🌐 Frontend: http://localhost:3000
- 📡 API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## First Steps

1. **View Dashboard**: Open http://localhost:3000 and select a vehicle
2. **Check Telematics**: See real-time sensor data on the dashboard
3. **Try Chatbot**: Go to the Chatbot tab and ask questions
4. **Schedule Appointment**: Use the Scheduling tab to book maintenance
5. **View Alerts**: Check the Alerts tab for predictions and warnings

## Demo Vehicles

The system comes with 3 demo vehicles:
- **VEH001**: Healthy vehicle
- **VEH002**: Vehicle with low battery and brake issues
- **VEH003**: Healthy vehicle with low mileage

## Troubleshooting

### Backend won't start
- Check if PostgreSQL, MongoDB, and Redis are running
- Verify database credentials in `.env`
- Check if port 8000 is available

### Frontend won't start
- Check if port 3000 is available
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Run `npm install` again

### No data showing
- Check if backend is running on port 8000
- Verify WebSocket connection in browser console
- Check backend logs for errors

## Next Steps

- 📖 Read [SETUP.md](./SETUP.md) for detailed setup instructions
- 🏗️ Check [ARCHITECTURE.md](./ARCHITECTURE.md) for system architecture
- 🔧 Customize configuration in `.env` files
- 🤖 Add your OpenAI API key for full chatbot functionality

## Support

For issues or questions:
1. Check the [README.md](./README.md)
2. Review [SETUP.md](./SETUP.md)
3. Check backend/frontend logs
4. Verify all services are running

Happy coding! 🚗✨

