# ShopEase Flutter App

The mobile frontend for the ShopEase full-stack e-commerce project.

## Main features

- User registration and login
- JWT token storage with `shared_preferences`
- Product listing and search
- Category filtering
- Product details
- Add, update and remove cart items
- User profile
- Profile image upload
- REST API integration with FastAPI

## Setup

1. Install Flutter.
2. Run:

```bash
flutter pub get
flutter run
```

3. Start the FastAPI backend from the repository's `backend` folder.

### API URL

The default URL in `lib/services/api_service.dart` is:

```text
http://10.0.2.2:8000
```

This is for an Android emulator. For a physical Android phone, replace it with your computer's local IP address, for example `http://192.168.1.5:8000`.

For an iOS simulator or desktop, `http://127.0.0.1:8000` can be used.
