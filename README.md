# ShopEase – Full-Stack E-Commerce Application

ShopEase is a full-stack e-commerce application built as a personal software development project.

The application uses **Flutter/Dart** for the mobile frontend and **Python/FastAPI** for the REST backend. It includes user authentication, product browsing, category filtering, cart management, profile management and profile image upload.

## Technology Stack

### Frontend
- Flutter
- Dart
- HTTP REST API integration
- Shared Preferences
- File Picker

### Backend
- Python
- FastAPI
- SQLAlchemy ORM
- Pydantic
- JWT authentication
- Password hashing with Argon2
- SQLite

## Project Structure

```text
ShopEase/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── modules.py
│   ├── pyd.py
│   ├── security.py
│   ├── email_service.py
│   ├── seed_data.py
│   ├── requirements.txt
│   └── routers/
│       ├── users.py
│       ├── products.py
│       ├── categories.py
│       ├── cart.py
│       └── home.py
│
├── frontend/
│   ├── lib/
│   │   ├── models/
│   │   ├── services/
│   │   ├── screens/
│   │   └── widgets/
│   ├── pubspec.yaml
│   └── README.md
│
└── README.md
```

## Backend Setup

Open a terminal in `backend`:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Seed sample products and categories:

```bash
python seed_data.py
```

Start the API:

```bash
uvicorn main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

The SQLite database is created automatically when the application starts.

## Frontend Setup

Open another terminal:

```bash
cd frontend
flutter pub get
flutter run
```

The API address is configured in:

```text
frontend/lib/services/api_service.dart
```

For an Android emulator the default is:

```text
http://10.0.2.2:8000
```

For a physical Android phone, replace it with the local IP address of the computer running FastAPI.

## Application Flow

```text
Flutter App
    |
    | HTTP / JSON
    v
FastAPI REST API
    |
    v
SQLAlchemy ORM
    |
    v
SQLite Database
```

Authentication uses JWT bearer tokens. Passwords are hashed before being stored.

## API Areas

- `POST /users/register`
- `POST /users/login`
- `GET /users/me`
- `POST /users/profile-image`
- `GET /categories/`
- `GET /products/`
- `GET /products/{id}`
- `POST /cart/`
- `GET /cart/`
- `PUT /cart/{cart_id}`
- `DELETE /cart/{cart_id}`

Admin-only product/category operations are also implemented in the backend.

## Notes

- `.env` and local databases are intentionally excluded from Git.
- The repository contains sample data instead of personal credentials.
- Email-based password reset requires SMTP credentials in a local `.env` file.
- This is a portfolio/learning project and is not presented as a production commerce platform.

## Author

Jaya Prakash Reddy Chevvu

Computer Science and Engineering graduate  
Python | FastAPI | Flutter | SQL
