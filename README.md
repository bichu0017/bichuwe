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

## Deploy frontend to Vercel and API to Render

The Django app remains the backend and admin service on Render. Its `/health/` endpoint is reserved for Render health checks so API throttling does not cause false failures. Vercel builds a static copy of the portfolio page and assets from `templates/index.html` and `static/`.

1. In Render, create a Blueprint from this repository using `render.yaml`. Set `DATABASE_URL` to the PostgreSQL connection string for the production database. Render generates `DJANGO_SECRET_KEY`; the service detects its Render hostname automatically.
2. In Vercel, import the same GitHub repository. Keep the project root at the repository root and set the Framework Preset to **Other** in Vercel's project settings so it doesn't try to run Django. Do not set a `framework` property in `vercel.json`; Vercel does not accept `other` as a config value. `vercel.json` builds and publishes `dist/`.
3. After the Render service is live, add the environment variable `RENDER_API_URL` to the Vercel project, using the Render service origin (for example, `https://bichu-portfolio-api.onrender.com`), then redeploy.
4. Add the exact Vercel site origin (for example, `https://your-site.vercel.app`, without a trailing slash) as `CORS_ALLOWED_ORIGINS` in Render and redeploy the backend.

The Render service also serves Django admin and static assets. General uploaded media remains on the local filesystem; profile images are stored in Supabase Storage. To keep profile images across Render restarts, create a **public** bucket in Supabase Storage and configure these Render environment variables using the bucket's S3-compatible credentials from Supabase **Storage → S3 Connection**:

- `SUPABASE_URL`: `https://<project-ref>.supabase.co`
- `SUPABASE_STORAGE_ENDPOINT`: `https://<project-ref>.storage.supabase.co/storage/v1/s3`
- `SUPABASE_STORAGE_REGION`: the region shown in Supabase S3 Connection
- `SUPABASE_STORAGE_BUCKET`: the bucket name
- `SUPABASE_STORAGE_ACCESS_KEY` and `SUPABASE_STORAGE_SECRET_KEY`: the S3 access key pair (not the Supabase database password, anon key, or service-role key)

Set the URL, endpoint, bucket, and key pair; the region defaults to `us-east-1` if omitted. Then redeploy Render. Profile image URLs are public, so the bucket must be public. Re-upload profile photos that were previously stored on Render's temporary filesystem; those existing files are not copied automatically.

Run the automated test suite with `python manage.py test portfolio --settings=config.test_settings`; test settings use an isolated in-memory SQLite database and never modify the live Supabase database.
