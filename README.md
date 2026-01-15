# Polyglot Intrusion Detection System (IDS)

## Overview
This project is a full-stack, polyglot CYBER THREAT INTELLIGENCE project featuring:
- **FastAPI** backend (Python)
- **React (Vite + MUI)** frontend (JavaScript/TypeScript)
- **PostgreSQL** for user management
- **MongoDB** for incidents and indicators
- **Redis** for caching and JWT blacklist
- **Machine Learning** for real-time network threat detection

## Features
- **User Authentication:** JWT-based, with secure password hashing and token revocation (blacklist) using Redis.
- **Incident Prediction:** Upload network flow data (CSV), get real-time predictions ("safe" or "blocked") using a pre-trained ML model.
- **Explainability:** For blocked flows, the system generates and stores the most important features (indicators) that led to the decision.
- **Polyglot Data Storage:** Combines relational (PostgreSQL), document (MongoDB), and key-value (Redis) databases for optimal performance and flexibility.
- **Caching:** User incidents are cached in Redis for 30 seconds to improve performance.
- **Modern UI:** Responsive, user-friendly dashboard built with React and Material UI.

## Architecture
- **Backend:** FastAPI, SQLAlchemy, Pydantic, python-jose, Redis, PostgreSQL, MongoDB
- **Frontend:** React, Vite, Material UI
- **ML Model:** Pre-trained and loaded at startup for efficient predictions

## How It Works
1. **Register/Login:** Users register and authenticate via JWT.
2. **Prediction:** Users upload a CSV or input data; the backend predicts and stores the result as an incident.
3. **Indicators:** If the flow is blocked, the backend attaches explainable indicators (top features) to the incident.
4. **Caching:** User incidents are cached in Redis for fast retrieval; cache is invalidated on new incident.
5. **Logout:** JWT tokens are blacklisted in Redis until expiry for secure session management.

## Running the Project
1. **Backend:**
   - Install dependencies: `pip install -r requirements.txt`
   - Start FastAPI: `uvicorn app:app --reload`
2. **Frontend:**
   - Navigate to `frontend/`
   - Install dependencies: `npm install`
   - Start dev server: `npm run dev`
3. **Databases:**
   - Ensure PostgreSQL, MongoDB, and Redis are running and accessible.

## Configuration
- Edit database connection settings in the backend config files as needed.
- The ML model should be placed in `model/model.pkl`.

## Scripts
- **Generate random samples:** `python test.py` (creates random CSVs for testing)

## Notable Endpoints
- `POST /api/register` — Register a new user
- `POST /api/login` — Login and receive JWT
- `POST /api/predict` — Predict and log an incident
- `GET /api/incidents/me` — Get your incidents (cached)
- `POST /api/logout` — Logout and blacklist JWT

## STAR Features
- **Polyglot architecture:** Uses PostgreSQL, MongoDB, and Redis together
- **Explainable AI:** Each blocked prediction is explained with top features
- **Real-time cache invalidation:** Ensures users always see up-to-date incidents
- **Secure JWT revocation:** Blacklist with TTL matching token expiry

## Authors
- EL YADRI Med Amine & LAAFAR Othmane 

---
For more details and code: 
