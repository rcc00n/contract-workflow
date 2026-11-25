# Synthetic case: one rental, one consistent document

The engineering problem is to keep customer, vehicle, period and pricing data
consistent as staff move from a rental form into a generated document. The public
repository demonstrates that plumbing without distributing a client's contract
wording, identity documents or customer records.

## Walk through the boundary

1. **Input:** an in-memory synthetic customer and vehicle are attached to a rental.
   The renderer fixtures are deliberately generated in code; no customer database
   or filled agreement is checked in.
2. **Decision:** `rentals/services/pricing.py` owns day boundaries, seasonal bands,
   fees and rounding. The synthetic boundary tests exercise same-day returns,
   a later return time and a high season that crosses New Year. Business defaults
   remain configurable and must be reviewed for the intended operator.
3. **Projection:** `build_placeholder_values` maps the rental into named document
   values. DOCX placeholders may span text runs; rendering must preserve formatting
   instead of replacing the entire paragraph blindly.
4. **Evidence:** `test_contract_renderer.py` creates a minimal DOCX in memory,
   renders it and checks resulting values, second-driver handling and layout.
   These fragments are test fixtures, not legal templates.
5. **Human review:** optional OCR produces confidence/missing-field states.
   Explicit text dates retain their written year; a separate Latin transcription
   does not contaminate the Cyrillic issuing authority. Real extraction quality
   still requires a separately configured inference runtime and human verification.

Run `python scripts/test_offline.py` after installing `ci/requirements.txt`.
For a short review, read the renderer tests, pricing boundary tests and public-source
tests before opening the larger views module. The network-blocked runner ensures
that a passing parser test cannot silently depend on a downloaded model or provider.

## Privacy is part of the interface

Production records and template text are private inputs. The checked-in workflow
contains application logic, migrations and synthetic tests only. The history check
rejects prohibited document/export formats and known secret patterns, while the
source tests prevent a tracked `.env` from returning. This is not a guarantee that
all arbitrary prose is anonymous; changed content still needs human review.

See [publication boundaries](PRIVACY.md) and [local development](DEVELOPMENT.md).
