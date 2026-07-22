# Mock Interactive Website

The production-ready Flask website for Mock Interactive, with home, about, contact, 404, robots, sitemap, and health-check routes.

## Start a new site

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and replace the placeholder values.
4. Run the site with `python app.py`.
5. Customize the studio copy, colors, and project inquiry flow while keeping the shared layout in `templates/base.html`.

The contact form validates input and displays a success message, but it intentionally does not send or store submissions. Connect an email provider, CRM, or database before launch.

Before production, set `FLASK_ENV=production`, use a unique long `FLASK_SECRET_KEY`, and replace the placeholder contact details. `SITE_URL` is optional on Render because the app automatically uses `RENDER_EXTERNAL_URL`.

## Deploy to Render

The repository includes `render.yaml`, so the deployment settings are versioned with the site.

1. Push this directory to a GitHub, GitLab, or Bitbucket repository.
2. In Render, choose **New > Blueprint** and connect that repository.
3. Confirm the `mock-interactive` web service and apply the Blueprint.
4. When prompted, enter the real `SITE_EMAIL` value.
5. After the first deploy, open the assigned `onrender.com` URL and confirm `/health` returns `{"status":"ok"}`.

Render will install `requirements.txt`, run Gunicorn on its assigned port, generate a production secret key, and redeploy when the linked branch changes. Python is pinned to the 3.11 release line in `.python-version`.

To use a custom domain later, add it in Render and set `SITE_URL` to the final `https://` address so canonical URLs and the sitemap use that domain.

## Image converter

`convert_to_webp.py` recursively converts JPG, PNG, HEIC, and HEIF images to WebP:

```powershell
python convert_to_webp.py static/images
python convert_to_webp.py static/images --output-folder static/images/converted
```

Use `--overwrite`, `--max-size`, and `--quality` to adjust conversion behavior.

## Checks

```powershell
python -m unittest discover -s tests
```
