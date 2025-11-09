# 🚗 N-Wheeler AI

**Intelligent Vehicle Maintenance System with Multi-Agent AI**

A comprehensive AI-powered system that predicts vehicle failures, engages with customers, and automates maintenance scheduling using a multi-agent architecture.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Chatbot  │  │Schedule  │  │  Alerts  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ WebSocket/REST API
┌───────────────────────────┴─────────────────────────────────┐
│              Backend (FastAPI) - Master Agent                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │  │
│  │  │   Data     │  │ Diagnosis  │  │  Customer  │    │  │
│  │  │  Analysis  │  │   Agent    │  │   Agent    │    │  │
│  │  └────────────┘  └────────────┘  └────────────┘    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │  │
│  │  │ Scheduling │  │  Feedback  │  │    UEBA    │    │  │
│  │  │   Agent    │  │   Agent    │  │  Security  │    │  │
│  │  └────────────┘  └────────────┘  └────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│              AI/ML Layer + Data Storage                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Anomaly   │  │Failure   │  │PostgreSQL│  │ MongoDB  │   │
│  │Detection │  │Prediction│  │          │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Features

- **Real-time Telematics Monitoring**: Live vehicle sensor data streaming
- **Predictive Failure Detection**: ML models predict component failures before they occur
- **Multi-Agent AI System**: Coordinated agents handle different aspects of the system
- **Customer Engagement**: Chatbot and voice interface for customer interaction
- **Auto-Scheduling**: Automatic maintenance appointment scheduling
- **Manufacturing Feedback**: Service feedback sent to manufacturing
- **UEBA Security**: User and Entity Behavior Analytics for threat detection

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework
- **TailwindCSS** - Styling
- **ShadCN UI** - UI components
- **Socket.io** - Real-time updates

### Backend
- **FastAPI** - REST API framework
- **LangChain/CrewAI** - Multi-agent orchestration
- **PostgreSQL** - Primary database
- **MongoDB** - Telematics data storage
- **Redis** - Caching and task queue
- **Celery** - Background tasks

### AI/ML
- **Scikit-learn** - ML models
- **PyTorch** - Deep learning (optional)
- **Isolation Forest** - Anomaly detection
- **XGBoost** - Failure prediction

### Communication
- **OpenAI GPT** - Chatbot
- **gTTS** - Text-to-speech
- **WebSocket** - Real-time communication

### Security
- **JWT** - Authentication
- **UEBA ML Model** - Anomaly detection for security

## 📦 Installation

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL
- MongoDB
- Redis

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Environment Variables

Create `.env` files in both `backend` and `frontend` directories:

**backend/.env**
```
DATABASE_URL=postgresql://user:password@localhost:5432/vehicle_maintenance
MONGODB_URL=mongodb://localhost:27017/telematics
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your_openai_api_key
JWT_SECRET=your_jwt_secret
UEBA_MODEL_PATH=./models/ueba_model.pkl
```

**frontend/.env.local**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 🚀 Running the Application

### Start Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Start Redis (for Celery)
```bash
redis-server
```

### Start Celery Worker
```bash
cd backend
celery -A tasks.celery_app worker --loglevel=info
```

## 📁 Project Structure

```
automobile/
├── frontend/                 # Next.js frontend
│   ├── app/                 # Next.js app directory
│   ├── components/          # React components
│   ├── lib/                 # Utilities
│   └── public/              # Static assets
├── backend/                 # FastAPI backend
│   ├── agents/              # Multi-agent system
│   ├── models/              # ML models
│   ├── api/                 # API routes
│   ├── database/            # Database models
│   ├── services/            # Business logic
│   └── ueba/                # UEBA security
├── data/                    # Data files
├── models/                  # Trained ML models
└── docs/                    # Documentation
```

## 🔐 Security

The system includes UEBA (User and Entity Behavior Analytics) to detect:
- Unusual agent behavior
- Unauthorized access attempts
- Anomalous data patterns
- Security threats

## 🤖 Agents

1. **Master Agent**: Orchestrates all other agents
2. **Data Analysis Agent**: Processes telematics data
3. **Diagnosis Agent**: Runs ML models for failure prediction
4. **Customer Agent**: Handles customer interactions
5. **Scheduling Agent**: Manages appointments
6. **Feedback Agent**: Collects and processes feedback

## 📊 API Documentation

Once the backend is running, visit:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📝 License

MIT License

## 👥 Contributors

Your Name

