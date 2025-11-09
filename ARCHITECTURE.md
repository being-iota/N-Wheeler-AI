# 🏗️ System Architecture

## Overview

The Vehicle Maintenance AI System is a multi-agent AI system that predicts vehicle failures, engages with customers, and automates maintenance scheduling.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Dashboard   │  │   Chatbot    │  │  Scheduling  │         │
│  │   (React)    │  │   (React)    │  │   (React)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API / WebSocket
┌───────────────────────────┴─────────────────────────────────────┐
│                      Backend Layer (FastAPI)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Master Agent                          │  │
│  │  (Orchestrates all other agents)                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │  │
│  │     Data     │  │  Diagnosis   │  │   Customer   │        │  │
│  │   Analysis   │  │    Agent     │  │    Agent     │        │  │
│  │    Agent     │  │              │  │              │        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘        │  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │  │
│  │  Scheduling  │  │   Feedback   │  │     UEBA     │        │  │
│  │    Agent     │  │    Agent     │  │   Security   │        │  │
│  └──────────────┘  └──────────────┘  └──────────────┘        │  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                    AI/ML & Data Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Anomaly    │  │   Failure    │  │  Telematics  │         │
│  │  Detection   │  │  Prediction  │  │   Simulator  │         │
│  │   (Isolation │  │   (XGBoost)  │  │              │         │
│  │    Forest)   │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                      Data Storage Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ PostgreSQL   │  │   MongoDB    │  │    Redis     │         │
│  │  (Users,     │  │ (Telematics, │  │   (Cache,    │         │
│  │ Appointments,│  │  Predictions)│  │   Queue)     │         │
│  │  Feedback)   │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend (Next.js)

**Purpose**: User interface for dashboard, chatbot, and scheduling

**Technologies**:
- Next.js 14 (React framework)
- TailwindCSS (styling)
- Socket.io Client (real-time updates)
- Axios (HTTP client)

**Components**:
- `Dashboard.tsx`: Real-time vehicle metrics and health scores
- `Chatbot.tsx`: Customer interaction interface
- `Scheduling.tsx`: Maintenance appointment scheduling
- `AlertPanel.tsx`: Alerts and notifications

### 2. Backend (FastAPI)

**Purpose**: API server and agent orchestration

**Technologies**:
- FastAPI (REST API framework)
- WebSocket (real-time communication)
- Python 3.10+

**API Endpoints**:
- `POST /api/v1/telematics`: Receive telematics data
- `GET /api/v1/vehicles/{vehicle_id}/status`: Get vehicle status
- `POST /api/v1/chat`: Chat with customer
- `POST /api/v1/schedule`: Schedule maintenance
- `POST /api/v1/feedback`: Submit feedback
- `GET /api/v1/ueba/activity`: Get UEBA activity summary

**WebSocket Endpoints**:
- `/ws/telematics/{vehicle_id}`: Real-time telematics data
- `/ws/chat/{session_id}`: Real-time chat

### 3. Multi-Agent System

#### Master Agent
- **Purpose**: Orchestrates all other agents
- **Responsibilities**:
  - Coordinates workflow between agents
  - Manages agent communication
  - Handles error recovery

#### Data Analysis Agent
- **Purpose**: Analyzes telematics data
- **Responsibilities**:
  - Processes sensor data
  - Detects anomalies
  - Calculates health scores
  - Stores data in MongoDB

#### Diagnosis Agent
- **Purpose**: Predicts component failures
- **Responsibilities**:
  - Runs ML models for failure prediction
  - Determines criticality of issues
  - Generates recommendations
  - Triggers alerts when needed

#### Customer Agent
- **Purpose**: Handles customer interactions
- **Responsibilities**:
  - Processes customer messages
  - Generates responses using OpenAI GPT
  - Sends alerts to customers
  - Maintains conversation history

#### Scheduling Agent
- **Purpose**: Manages maintenance appointments
- **Responsibilities**:
  - Schedules appointments
  - Finds available time slots
  - Auto-schedules critical issues
  - Manages appointment cancellation

#### Feedback Agent
- **Purpose**: Processes service feedback
- **Responsibilities**:
  - Collects feedback from customers
  - Analyzes feedback for manufacturing
  - Sends insights to manufacturing system
  - Maintains feedback history

### 4. AI/ML Models

#### Anomaly Detection (Isolation Forest)
- **Purpose**: Detect anomalous sensor readings
- **Input**: Sensor data (battery, engine temp, oil pressure, etc.)
- **Output**: List of detected anomalies
- **Model**: Isolation Forest (Scikit-learn)

#### Failure Prediction (XGBoost)
- **Purpose**: Predict component failure probabilities
- **Input**: Sensor metrics and health scores
- **Output**: Failure probabilities for each component
- **Model**: XGBoost Regressor

### 5. Data Storage

#### PostgreSQL
- **Purpose**: Relational data storage
- **Tables**:
  - `vehicles`: Vehicle information
  - `appointments`: Maintenance appointments
  - `feedback`: Service feedback
  - `alerts`: System alerts
  - `conversations`: Chat conversations

#### MongoDB
- **Purpose**: Time-series and document storage
- **Collections**:
  - `telematics_data`: Sensor data and analysis
  - `predictions`: Failure predictions
  - `manufacturing_feedback`: Feedback insights

#### Redis
- **Purpose**: Caching and task queue
- **Usage**:
  - Cache latest telematics data
  - Cache predictions
  - Task queue for Celery

### 6. UEBA Security

**Purpose**: Monitor agent behavior and detect anomalies

**Features**:
- Rate limiting per agent
- Unauthorized action detection
- ML-based anomaly detection
- Security logging

**Monitoring**:
- Agent activity logging
- Anomaly detection
- Security alerts
- Activity summaries

## Data Flow

### Telematics Data Flow

1. **Data Collection**: Telematics simulator generates sensor data
2. **Data Reception**: Backend receives data via API
3. **Data Analysis**: Data Analysis Agent processes data
4. **Anomaly Detection**: Anomaly detection model runs
5. **Failure Prediction**: Diagnosis Agent predicts failures
6. **Alert Generation**: Critical alerts trigger customer notifications
7. **Auto-Scheduling**: Critical issues auto-schedule appointments
8. **Data Storage**: Data stored in MongoDB and PostgreSQL

### Customer Interaction Flow

1. **Customer Message**: Customer sends message via chatbot
2. **Message Processing**: Customer Agent processes message
3. **Context Retrieval**: System retrieves vehicle context
4. **Response Generation**: OpenAI GPT generates response
5. **Response Delivery**: Response sent to customer
6. **History Storage**: Conversation stored in database

### Scheduling Flow

1. **Service Request**: Customer or system requests service
2. **Slot Availability**: Scheduling Agent checks available slots
3. **Appointment Creation**: Appointment created in database
4. **Confirmation**: Customer receives confirmation
5. **Reminder**: System sends reminder before appointment

## Security

### Authentication
- JWT tokens for API authentication
- OAuth2 for user authentication (optional)

### Authorization
- Role-based access control
- Agent permission system

### UEBA
- Agent behavior monitoring
- Anomaly detection
- Security logging
- Threat detection

## Scalability

### Horizontal Scaling
- Stateless API servers
- Load balancing
- Database replication
- Redis cluster

### Vertical Scaling
- Database optimization
- Caching strategies
- Model optimization
- Resource allocation

## Monitoring

### Metrics
- API response times
- Agent activity rates
- Prediction accuracy
- System health

### Logging
- Application logs
- Agent activity logs
- Security logs
- Error logs

### Alerts
- System alerts
- Security alerts
- Performance alerts
- Error alerts

## Future Enhancements

1. **Voice Interface**: Add voice bot support
2. **Mobile App**: Develop mobile application
3. **Advanced ML**: Implement deep learning models
4. **IoT Integration**: Connect to real IoT devices
5. **Blockchain**: Add blockchain for data integrity
6. **Edge Computing**: Deploy edge computing for real-time processing

