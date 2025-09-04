# klantroef_secure_backend

A secure backend service built with FastAPI, SQLAlchemy, and JWT authentication.  
This project was developed as part of a simulation assessment.

---

# Features
- User registration and authentication (JWT-based)
- Secure media asset management (audio/video metadata storage)
- Expiring streaming link generation
- Stream validation and access logging
- SQLite database integration
- Interactive API documentation via Swagger UI (`/docs`)

---

# Tech Stack
- **Python 3.9+**
- **FastAPI**
- **SQLAlchemy**
- **JWT (python-jose)**
- **Passlib (bcrypt hashing)**
- **Pydantic**
- **Uvicorn**

---

# Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nithish-pb/klantroef_secure_backend.git
   cd klantroef_secure_backend

2. Create a virtual environment:

    python -m venv venv
    venv\Scripts\activate

3. Install dependencies:

    pip install -r requirements.txt


4. Create a .env file in the project root:

    SECRET_KEY=super-long-random-string-here
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    STREAM_LINK_EXPIRE_MINUTES=10
    DATABASE_URL=sqlite:///./app.db

5. Start the development server:

    uvicorn app.main:app --reload


    The app will be available at:

    http://127.0.0.1:8000


6. Swagger docs:

    http://127.0.0.1:8000/docs