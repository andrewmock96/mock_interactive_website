# Flask Website Template

A polished Flask starting point for a web design studio, with home, about, contact, 404, robots, and sitemap routes.

## Start a new site

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and replace the placeholder values.
4. Run the site with `python app.py`.
5. Customize the studio copy, colors, and project inquiry flow while keeping the shared layout in `templates/base.html`.

The contact form validates input and displays a success message, but it intentionally does not send or store submissions. Connect an email provider, CRM, or database before launch.

Before production, set `FLASK_ENV=production`, use a unique long `FLASK_SECRET_KEY`, set the public `SITE_URL`, and replace all placeholder contact details.

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
