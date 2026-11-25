# Contract workflow

A Django workspace for car-rental operations. Contract workflow connects fleet and
customer records with rental pricing, agreement templates and document generation,
so the information entered for a rental can carry through to its contract.

## Capabilities

- **Fleet and customer records:** vehicles, customer profiles, tags, notes,
  document fields, search and import/export workflows.
- **Rental workflow:** a guided rental form, second-driver information, rental
  dates, equipment, prepayments and outstanding balances.
- **Pricing:** seasonal rate bands, rental duration, delivery locations, night
  fees, equipment and configured discounts.
- **Contracts:** reusable templates and placeholder substitution for HTML,
  DOCX and PDF output.
- **Business settings:** seasonal boundaries, equipment prices, delivery fees
  and operational defaults.
- **Optional OCR:** a driving-licence extraction pipeline with parsing and image
  preprocessing. Extracted information still needs human review.

## Architecture

```mermaid
flowchart LR
  Staff[Signed-in rental workspace] --> Django[Django views and forms]
  Django --> Records[Fleet, customers and rentals]
  Records --> DB[(PostgreSQL)]
  Django --> Pricing[Rental pricing service]
  Django --> Renderer[Template and document renderer]
  Renderer --> Files[HTML, DOCX and PDF]
  Django --> OCR[Optional licence OCR]
```

| Layer | Implementation |
| --- | --- |
| Application | Python, Django 5, server-rendered templates |
| Persistence | PostgreSQL, Django ORM and migrations |
| Documents | python-docx, pypdf, xhtml2pdf, ReportLab |
| Import and OCR | openpyxl/xlrd, OpenCV, PaddleOCR |
| Runtime | Gunicorn, WhiteNoise, Docker tooling |

## Local development

Use a fresh checkout, a Python environment compatible with
[`requirements.txt`](requirements.txt), and an empty local PostgreSQL database.
The Docker build uses Python 3.11 and lists native dependencies for PDF and OCR.
Configure your own local values before running Django; see
[the development guide](docs/DEVELOPMENT.md).

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Set your local DJANGO_* and database configuration first.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Start with your own local administrator and empty data. The commands correspond to
the source entry points; they are not a claim that a new database, OCR model or
document-rendering environment was verified during the documentation refresh.

## Source map

| Area | Code and examples |
| --- | --- |
| Settings and application routes | [car_rental/](car_rental/) |
| Rental data model | [rentals/models.py](rentals/models.py) |
| Forms and guided workflow | [rentals/forms.py](rentals/forms.py) · [views](rentals/views.py) |
| Pricing rules | [rentals/services/pricing.py](rentals/services/pricing.py) |
| Contract generation | [rentals/services/contract_renderer.py](rentals/services/contract_renderer.py) |
| OCR pipeline | [rentals/ocr/](rentals/ocr/) |
| Existing regressions | [rentals/tests/](rentals/tests/) |
| Privacy and publication boundaries | [Privacy](docs/PRIVACY.md) |
| Setup and document boundaries | [Development](docs/DEVELOPMENT.md) |

## Scope and limitations

OCR can misread identity information; inspect extracted values before saving or
generating a contract. Templates and pricing settings must match the intended
business rules. Generated documents are application output, not a guarantee of
legal suitability.

Local startup requires configured environment values and PDF/OCR dependencies.
Use dedicated local data and review the intended storage and access rules before
processing customer documents. No CI result, coverage percentage or new licence
grant is asserted here; existing third-party asset notices remain intact.
