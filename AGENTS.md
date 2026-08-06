# Repository Guidelines

## Project Structure & Module Organization

This repository is intended to become a small Django site for a private Project Zomboid roleplay community. Keep the four-app layout defined in `prompt.md`: `core/` for the home page and site settings, `accounts/` for profiles and authentication, `news/` for articles, and `marketplace/` for listings. Place project configuration in `config/`, shared HTML in `templates/`, CSS and browser assets in `static/`, uploads in `media/`, and app-specific tests in each app's `tests.py` or `tests/` package. Avoid extra service layers or additional apps unless they remove real duplication.

## Build, Test, and Development Commands

From the repository root, use a virtual environment and the standard Django workflow:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Run `python manage.py test` before submitting changes. Use `python manage.py check` for a quick configuration and model validation. When models change, create migrations with `python manage.py makemigrations`, inspect them, then apply them.

## Coding Style & Naming Conventions

Use four-space indentation and conventional Python/Django naming: `snake_case` for functions and variables, `PascalCase` for models and forms, and descriptive template names such as `news/article_detail.html`. Keep views, forms, and permission checks straightforward and beginner-readable. Use Django templates, plain CSS, and minimal vanilla JavaScript; do not introduce frontend frameworks. Prefer Django ORM and built-in authentication features over custom abstractions.

## Testing Guidelines

Use Django's `TestCase` and test client. Name tests `test_<expected_behavior>`, emphasizing access control: hidden news must not appear in lists, direct URLs, or HTML; users may modify only their own listings; staff-only pages must reject survivors. Add focused regression tests for every permission or visibility change. Complete coverage is not required.

## Commit & Pull Request Guidelines

No Git history exists yet, so use short imperative commit subjects, for example `Add news visibility checks`. Keep commits focused. Pull requests should summarize behavior, list migrations and test commands, link relevant issues, and include screenshots for template or CSS changes. Call out permission changes explicitly.

## Security & Configuration

Keep secrets in environment variables and document placeholders in `.env.example`. Never commit credentials, uploaded media, or a production database. Require CSRF protection, validate image type and size, enforce permissions in backend views, and keep `DEBUG=False` in production.
