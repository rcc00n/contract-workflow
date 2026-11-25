# Contract workflow development guide

## Local configuration

Use an empty local PostgreSQL database and your own local role. Configuration names
are documented in [`.env.example`](../.env.example) and read by
[`car_rental/settings.py`](../car_rental/settings.py). Generate a new
`DJANGO_SECRET_KEY` and set your own database connection; do not reuse inherited
environment values from a checkout.

The host settings read process environment values directly. A `.env` file alone
is not automatically loaded by `manage.py`; export values before starting Django:

```bash
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
export DJANGO_DEBUG=true
export DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
export DATABASE_URL='postgresql://USERNAME:PASSWORD@localhost:5432/contract_workflow'
```

Replace the database placeholders with your local role and password. Keep local
configuration and customer uploads out of Git. The existing settings can also
construct a connection from separate `POSTGRES_*` variables; use one intentional
local configuration.

The repository's [Dockerfile](../Dockerfile) uses Python 3.11 and lists native
libraries needed by PDF/image processing. For a host environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Set the environment before running Django. Commands were checked against the
repository configuration; no application database, container or production service
was started during this documentation refresh. The existing Compose file includes
public web/proxy port mappings, so review it for the intended host before using it.

## Rental data and pricing

Create fleet and customer records before creating a rental. The guided workflow
records the rental period, driver information, delivery, equipment and payments.
[`pricing.py`](../rentals/services/pricing.py) applies configured seasonal and
duration bands, delivery/night fees, equipment and discounts.

Business defaults live in the `BusinessSettings` model. Review changes to these
values alongside generated document totals; they are business configuration, not
decorative interface settings.

Create synthetic import files locally when testing. Customer exports and business
documents are intentionally excluded from the source repository. Imports and
deletions change database records.

## Contract templates

`ContractTemplate` supports an uploaded file or HTML body and exposes placeholder
help. [`contract_renderer.py`](../rentals/services/contract_renderer.py) builds values
from the rental, fleet and customer data, then renders the selected document format.

Business contract templates are intentionally not distributed. Create private
templates for the intended business and review their wording, placeholders, fonts,
layout and totals before use. Tests construct minimal synthetic document fixtures
in memory; they are not legal templates. The application does not establish legal
validity.

## Optional driving-licence OCR

The implementation under [`rentals/ocr/`](../rentals/ocr/) combines image processing,
OCR and field parsing. Some configurations use optional anchor/keypoint models.
Review `OCR_USE_ANCHORS`, `OCR_USE_KEYPOINTS`, `OCR_KEYPOINT_MODEL_PATH` and the related
settings before enabling those paths. Model availability and extraction quality
depend on the local runtime and source image.

When upload retention is enabled, use intentional private storage and retention
settings. The existing cleanup command is:

```bash
python manage.py ocr_cleanup_uploads
```

This command can delete retained OCR uploads according to configured rules; it is
not a setup or presentation-validation step. Extracted identity fields need human
review before they become saved customer data or contract text.

## Existing tests and contribution

[`rentals/tests/`](../rentals/tests/) contains document rendering, customer search,
OCR endpoint and parser regression scenarios. No test-suite pass is claimed by this
documentation refresh. When changing behavior, run the relevant existing cases in
an isolated environment and add coverage for new business rules.

Keep uploaded identity documents, customer data, private environment files, generated
contracts and service credentials outside version control. Preserve third-party
licence notices; no new licence is selected by this documentation change.
