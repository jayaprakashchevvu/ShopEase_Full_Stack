# GitHub upload

Create a new empty repository on GitHub, for example:

`shopease-full-stack`

Do not add a README or .gitignore from GitHub because this project already contains them.

Then run these commands from the project root:

```bash
git init
git add .
git commit -m "Initial ShopEase full-stack project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shopease-full-stack.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Suggested repository description

`Full-stack e-commerce application built with Flutter, Python FastAPI, SQLAlchemy, JWT authentication and SQLite.`

## Suggested GitHub topics

`flutter` `dart` `python` `fastapi` `sqlalchemy` `rest-api` `jwt` `sqlite` `ecommerce` `mobile-app`

## Before pushing

Make sure `.env`, passwords, API secrets, local databases and uploaded profile images are not committed. The included `.gitignore` is set up for this.
