# Online defense guide

1. Share your screen and open this source folder in your editor.
2. Run `docker compose up --build`; show both healthy services with `docker compose ps`.
3. Open Postman and run the collection in order. Explain 201, 200, 204, 400, 404, and 409.
4. Show `Tour`, `Booking`, their foreign key, serializer validation, and ModelViewSet CRUD behavior.
5. Create a record, run `docker compose down` then `docker compose up -d`, and GET the record again to demonstrate persistent storage. Delete the demo record afterward.

## Theory

- Image: a packaged read-only filesystem and runtime metadata. Dockerfile instructions build image layers; unchanged dependency layers can be cached.
- Container: a running isolated process based on an image, with a disposable writable layer.
- Dockerfile: defines base image, dependencies, source, user, entrypoint, and command. ENTRYPOINT runs migrations; CMD supplies the Gunicorn server command.
- Compose: declares services, configuration, dependencies, networks, ports, and volumes as one application.
- Network: services discover each other through Compose DNS. The backend connects to `db:5432`.
- Ports: host 8001 forwards to backend 8000. EXPOSE documents a port; the Compose `ports` mapping publishes it.
- Volume: `postgres_data` lives independently of container lifecycles. `down -v` removes it.
- Environment: runtime configuration avoids hard-coded database credentials. `.env` supplies Compose interpolation; the `environment` section passes values into containers.
- Health checks: dependency readiness is different from merely starting a container. Backend health tests database access too.
- Migration: version-controlled schema changes, applied before serving traffic.

## Live modification exercise

Change the API title in `tours/views.py`, rebuild with `docker compose up --build -d`, and GET `/`. Explain why rebuilding is necessary without a source bind mount. For a validation exercise, adjust the date error text in `tours/serializers.py`, rebuild, and send invalid dates.

## Troubleshooting

- Port occupied: change `API_PORT` and Postman `base_url`.
- Database unavailable: inspect `docker compose logs db web`, `.env`, and service health.
- Password changed after first run: existing volumes retain original credentials. Restore the original password or intentionally reset disposable data with `down -v`.
- Stale code: rebuild the backend image.
- Missing trailing slash: use the documented slash on write endpoints to avoid redirects.
- Tour deletion returns 409: delete its bookings first, including cancelled bookings.
