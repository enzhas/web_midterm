# Tour Operator API

Base URL: `http://localhost:8001`. JSON requests and responses. No authentication is required for this local coursework demo. Use trailing slashes. Lists return JSON arrays, without pagination. Decimal prices are returned as strings in USD. Dates use `YYYY-MM-DD`; timestamps use UTC ISO 8601.

| Method | Endpoint | Result |
| --- | --- | --- |
| GET | `/` | API name and links (200) |
| GET | `/api/` | Resource links (200) |
| GET | `/api/health/` | Database connectivity: 200 or 503 |
| GET | `/api/tours/` | List tours (200) |
| POST | `/api/tours/` | Create tour (201) |
| GET | `/api/tours/{id}/` | Retrieve tour (200) |
| PUT | `/api/tours/{id}/` | Replace tour (200) |
| PATCH | `/api/tours/{id}/` | Update supplied fields (200) |
| DELETE | `/api/tours/{id}/` | Delete unreferenced tour (204) |
| GET | `/api/bookings/` | List bookings (200) |
| POST | `/api/bookings/` | Create booking (201) |
| GET | `/api/bookings/{id}/` | Retrieve booking (200) |
| PUT | `/api/bookings/{id}/` | Replace booking (200) |
| PATCH | `/api/bookings/{id}/` | Update supplied fields (200) |
| DELETE | `/api/bookings/{id}/` | Delete booking (204) |

## Tour fields

`id`: generated, read only. Required: `title` (nonblank, max 160), `destination` (nonblank, max 120), `price` (nonnegative decimal, 10 digits total and 2 decimal places), `start_date`, `end_date` (on or after start), `max_guests` (positive integer). Optional: `description` (default empty string), `is_active` (default true).

Example POST or PUT body:

```json
{
  "title": "Charyn Canyon Adventure",
  "destination": "Kazakhstan, Charyn Canyon",
  "description": "Guided canyon walk with transport from Almaty.",
  "price": "149.00",
  "start_date": "2027-06-10",
  "end_date": "2027-06-12",
  "max_guests": 12,
  "is_active": true
}
```

## Booking fields

`id` and `created_at` are generated, read only. Required: `tour` (existing tour ID), `customer_name` (nonblank, max 120), `customer_email` (valid email, max 254), `guests` (positive integer). Optional: `status` (`pending`, `confirmed`, `cancelled`; default `pending`), `notes` (default empty string).

Example POST or PUT body:

```json
{"tour": 1, "customer_name": "Aida Karimova", "customer_email": "aida@example.com", "guests": 2, "status": "pending", "notes": "Vegetarian lunch please."}
```

Create returns the supplied data with generated fields. GET/PUT/PATCH return the same resource shape. PATCH can send a single field, for example `{"status":"confirmed"}`. PUT requires all required fields; optional omitted fields follow Django REST Framework update behavior and retain existing values. DELETE returns no body.

## Errors and business rules

- 400: invalid fields, malformed JSON, missing required fields, or nonexistent tour reference. Example: `{"guests":["Ensure this value is greater than or equal to 1."]}`.
- 404: resource does not exist, with `{"detail":"No Tour matches the given query."}` for a missing tour.
- 409: tour has bookings: `{"detail":"Delete this tour's bookings before deleting the tour."}`. Cancelled bookings also protect a tour.
- 405: unsupported HTTP method. 415: unsupported content type.
- 503: health check cannot reach PostgreSQL: `{"status":"unavailable"}`.

`max_guests` describes a tour group; this demo records booking requests and does not allocate inventory or enforce total booked capacity. Inactive tours and past dates can still be referenced. There are no payments, login, or automatic price calculations.
