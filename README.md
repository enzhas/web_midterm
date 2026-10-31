# Tour Operator API

A containerized Django REST Framework application for managing tours and customer bookings, with PostgreSQL. Based on the architecture of the reference practical project, using a tourism domain.

## Start

Install Docker Desktop with Docker Compose, start Docker, then run from this directory:

```sh
docker compose up --build
```

The provided `.env` contains working local demo settings. If cloning from GitHub (where `.env` is intentionally ignored), first run `cp .env.example .env`. After the first build, `docker compose up` is sufficient. Open http://localhost:8001/ and import `postman/tour_operator.postman_collection.json` into Postman. The database starts empty; the collection creates its own demo data.

Port 8001 avoids conflict with the reference project on port 8000. Change `API_PORT` in `.env` and Postman's `base_url` collection variable if needed.

## Architecture

```text
Postman → localhost:8001 → web:8000 (Django + Gunicorn)
                               ↓ Compose DNS: db:5432
                          db (PostgreSQL 16)
                               ↓
                      postgres_data named volume
```

Compose creates a private default bridge network shared by both services. `db` is the database hostname inside the network; `localhost` inside the backend would refer to the backend container itself. PostgreSQL is not published to the host. Backend port 8000 is published only on host loopback port 8001.

The custom Dockerfile installs pinned dependencies, copies the application, and runs Gunicorn as an unprivileged user. `.dockerignore` excludes environment secrets and development files. Compose waits for PostgreSQL health; the entrypoint verifies authenticated connectivity and applies committed migrations before starting Gunicorn. The web health check also queries the database.

## API and Postman

See [complete endpoint documentation](docs/API.md). Both `/api/tours/` and `/api/bookings/` implement list, get by ID, create, PUT, PATCH, and delete. Foreign keys protect tours that have booking records. Field validation and database constraints protect core numeric and date rules.

Import the collection in Postman and use **Run collection**, preserving the request order. The default `base_url` is `http://localhost:8001`. Create requests automatically save `tour_id` and `booking_id`; later requests use those values. Assertions check response codes. The collection demonstrates both update methods, validation errors, protected deletion, and successful deletion, then cleans up its records. For a manual defense, send requests sequentially and inspect each response.

## Configuration

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret; replace demo value for deployment |
| `DJANGO_DEBUG` | Debug responses; defaults to false |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated accepted hosts |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database role |
| `POSTGRES_PASSWORD` | Database password |
| `API_PORT` | Host port, default 8001 |

Compose sets `POSTGRES_HOST=db` and `POSTGRES_PORT=5432` for the backend. This is an unauthenticated local assignment application; do not expose it publicly with real customer data. PostgreSQL initialization variables apply when its volume is first created; changing credentials in `.env` does not change existing database credentials.

## Verify and operate

```sh
docker compose ps
docker compose exec web python manage.py test
docker compose exec web python manage.py makemigrations --check --dry-run
docker compose logs web db
docker compose down
docker compose up -d
```

`down` removes containers and the network while retaining the named database volume. Records survive container recreation. `docker compose down -v` deletes database storage permanently; use only to intentionally reset demo data.

After modifying Python code, run `docker compose up --build -d` because source files are copied into the image. After modifying models, generate a migration and commit it before rebuilding. To generate inside this container setup: `docker compose exec web python manage.py makemigrations tours`, then copy the new file with `docker compose cp web:/app/tours/migrations/<filename> tours/migrations/<filename>` and rebuild. See [defense notes](docs/DEFENSE.md).

## Repository structure

- `config/`: Django settings and URL configuration.
- `tours/`: models, serializers, views, routes, migrations, tests, database wait command.
- `Dockerfile`, `entrypoint.sh`, `compose.yaml`: container runtime and orchestration.
- `docs/`: API contract and defense preparation.
- `postman/`: importable collection with automated assertions.
- `.env.example`: shareable configuration template; `.env`: local working configuration, excluded from Git.

## Submission

Publish these source files to your public GitHub repository, then submit the repository URL and a ZIP including `.env`. A `submission.zip` is provided locally and excluded from Git and the Docker build. Upload your work and press **Turn in** before your assignment deadline. GitHub publication and LMS submission require your account.

## Filtering

Tour lists support `destination`, `is_active`, `min_price`, `max_price`, and `ordering`. Booking lists support `tour` and `status`. Combine query parameters with `&`; see [API documentation](docs/API.md#list-filters-and-sorting) and the filter requests in Postman.
