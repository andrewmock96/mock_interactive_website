from datetime import datetime, timezone
import os
from xml.etree import ElementTree

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFError, CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
IS_PRODUCTION = os.environ.get("FLASK_ENV") == "production"
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "change-me-in-production")

if IS_PRODUCTION and SECRET_KEY == "change-me-in-production":
    raise RuntimeError("Set a unique FLASK_SECRET_KEY before running in production.")

app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = IS_PRODUCTION
csrf = CSRFProtect(app)


def site_url():
    return (
        os.environ.get("SITE_URL")
        or os.environ.get("RENDER_EXTERNAL_URL")
        or "http://localhost:5000"
    ).rstrip("/")


@app.context_processor
def inject_site_metadata():
    return {
        "site_title": os.environ.get("SITE_TITLE", "Mock Interactive"),
        "site_description": os.environ.get(
        "SITE_DESCRIPTION",
            "Atmospheric games, meaningful systems, and unforgettable interactive worlds.",
        ),
        "site_phone": os.environ.get("SITE_PHONE", "+1 (555) 123-4567"),
        "site_email": os.environ.get("SITE_EMAIL", "hello@mockinteractive.com"),
        "site_url": site_url(),
        "fileforge_download_url": os.environ.get(
            "FILEFORGE_DOWNLOAD_URL",
            "https://github.com/andrewmock96/FileForge/releases/latest/download/fileforge-1.0-windows-x64.zip",
        ),
        "fileforge_repo_url": os.environ.get(
            "FILEFORGE_REPO_URL",
            "https://github.com/andrewmock96/FileForge",
        ),
        "fileforge_virustotal_url": os.environ.get(
            "FILEFORGE_VIRUSTOTAL_URL",
            "https://www.virustotal.com/gui/file/c5a51af9905fb5c8827691f8b2417c3233f10c4d53ee5085d86005b3d7dcc98f/detection",
        ),
        "support_url": os.environ.get(
            "SUPPORT_URL", "https://ko-fi.com/mockinteractive"
        ).strip(),
        "cloudflare_analytics_token": os.environ.get(
            "CLOUDFLARE_WEB_ANALYTICS_TOKEN", ""
        ).strip(),
        "canonical_url": f"{site_url()}{request.path}",
        "current_year": datetime.now(timezone.utc).year,
    }


@app.route("/")
def home():
    return render_template("tools.html")


# Preserved for a future games-focused launch.
# @app.route("/worlds")
def worlds():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "ok"}


# @app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tools")
def tools():
    return redirect(url_for("home"), code=302)


@app.route("/robots.txt")
def robots():
    body = f"User-agent: *\nAllow: /\n\nSitemap: {site_url()}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ElementTree.register_namespace("", namespace)
    urlset = ElementTree.Element(f"{{{namespace}}}urlset")

    for endpoint in ("home",):
        url_element = ElementTree.SubElement(urlset, f"{{{namespace}}}url")
        location = ElementTree.SubElement(url_element, f"{{{namespace}}}loc")
        location.text = f"{site_url()}{url_for(endpoint)}"

    xml = ElementTree.tostring(urlset, encoding="utf-8", xml_declaration=True)
    return Response(xml, mimetype="application/xml")


# @app.route("/contact", methods=["GET", "POST"])
def contact():
    form_data = {"name": "", "email": "", "message": ""}

    if request.method == "POST":
        form_data = {
            "name": (request.form.get("name") or "").strip()[:100],
            "email": (request.form.get("email") or "").strip()[:254],
            "message": (request.form.get("message") or "").strip()[:5000],
        }

        if not all(form_data.values()):
            flash("Please complete all required fields.", "error")
            return render_template("contact.html", form_data=form_data), 400

        if "@" not in form_data["email"] or "." not in form_data["email"].rsplit("@", 1)[-1]:
            flash("Please enter a valid email address.", "error")
            return render_template("contact.html", form_data=form_data), 400

        # Replace this success path with an email provider, CRM, or database integration.
        flash("Thanks for reaching out. We will get back to you soon.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", form_data=form_data)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(CSRFError)
def csrf_error(_error):
    flash("Your form session expired. Please try again.", "error")
    return redirect(url_for("home"))


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault(
        "Permissions-Policy", "camera=(), geolocation=(), microphone=()"
    )
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
