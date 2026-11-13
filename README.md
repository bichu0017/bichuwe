# Bichu Biju — Portfolio

A responsive portfolio inspired by the supplied reference, with a minimalist white layout and `#005C5F` teal accents. It includes a Django REST API and Django's authenticated admin for managing portfolio content.

## Run locally

1. Install Python 3.10 or later and create a virtual environment.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Copy `.env.example` to `.env`; set a private `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=True`.
4. Put your Supabase PostgreSQL connection URL in `.env` as `DATABASE_URL`, including `?sslmode=require`. URL-encode special characters in the database password.
5. Apply migrations to the connected database: `python manage.py migrate`
6. Create an administrator: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`

Open `http://127.0.0.1:8000/` for the portfolio (start it with `python manage.py runserver`; Live Server on port 5500 does not serve Django templates or APIs). Use the underlined **Admin Dashboard** link in the footer to sign in and open the profile editor. It lets an administrator change name, title, email, phone, location, biography, up to three profile photos, and social links. Profile photos rotate automatically every three seconds. Manage the public certificate gallery from **Certificates** in the admin dashboard; each certificate can include an image or PDF/Word file (PDF, DOC, or DOCX, up to 10 MB), title, organization, description, issue date, and credential link. Only staff/admin accounts can edit or upload content. Create the first admin with `python manage.py createsuperuser`.

The Django admin sections **Profiles** and **Resumes** manage profile/contact details and the active resume. **Portfolio documents** is for additional PDF, Word, spreadsheet, presentation, text, and ZIP files (up to 20 MB). Resume uploads accept PDF and Word files (up to 10 MB). Public API endpoints are available under `/api/`; anonymous visitors can read published projects and submit messages/questions, while changes require staff authentication.

## Database

The app is connected to Supabase PostgreSQL when `DATABASE_URL` is set in the private `.env` file. `.env.example` shows the expected URL format. Keep the database password in `.env`, URL-encode special characters (for example `@` and `#`), and require SSL. In production, set `DJANGO_DEBUG=False`, a strong `DJANGO_SECRET_KEY`, and the correct `DJANGO_ALLOWED_HOSTS`. Never place credentials in browser code or commit `.env`.

## Media and production

Uploaded media is stored locally in `media/` during development. File download links send files as attachments; the configured document type and file-size checks apply to uploads. For production, configure private server-side object storage and backups before accepting uploads. Run `python manage.py collectstatic` and deploy with a production WSGI/ASGI server over HTTPS. Use Django admin to edit profile and site content; keep public/private API permissions in place.

The contact form submits to the API and stores messages for review in Django admin. Replace the included portrait illustration with an authorized profile photo in `static/images/`.

Run the automated test suite with `python manage.py test portfolio --settings=config.test_settings`; test settings use an isolated in-memory SQLite database and never modify the live Supabase database.
