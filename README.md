# Court Document PII Redactor

This Gradio application runs on Hugging Face Spaces and removes personally identifiable information (PII) from court documents using large language models hosted by OpenRouter and Cerebras. It provides a 2×2 workspace:

1. Paste the original text containing PII.
2. Automatically redact sensitive spans into placeholders like `<PII_PERSON_1>` with color-coded highlighting.
3. Edit the redacted text while preserving the placeholders.
4. Restore the original PII into the edited text.

## Features

- Integrates with `nvidia/nemotron-nano-9b-v2:free` via OpenRouter and the Cerebras API.
- Splits text into ~400-character chunks at sentence/word boundaries for stable inference.
- Generates deterministic PII tags per category and maintains reversible mappings.
- **Color-coded PII highlighting**: Different types of PII are displayed with distinct colors in the redacted output.
- **Download functionality**: Export redacted and restored text as timestamped files.
- **Enhanced validation**: Real-time validation with warnings about missing or problematic PII tags.
- **Detailed statistics**: Shows count of each PII type detected for audit purposes.
- Provides a queue-enabled Gradio UI ideal for Hugging Face Spaces deployment.

## Environment Variables

Create a `.env` file (or configure Secrets in your Hugging Face Space) using the template in `env.example`:

- `OPENROUTER_API_KEY`: API key from https://openrouter.ai.
- `OPENROUTER_SITE_URL` (optional): URL of the hosting Space, used for OpenRouter attribution.
- `OPENROUTER_APP_NAME` (optional): Display name for OpenRouter analytics.
- `CEREBRAS_API_KEY`: API key from https://inference.cerebras.ai/.
- `CEREBRAS_MODEL` (optional): Defaults to `llama3.1-8b-instruct`.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' env.example | xargs)  # or place keys in .env
python app.py
```

Visit http://localhost:7860/ to use the interface.

## Sample Court Document

Try this sample text to test the application:

```
UNITED STATES DISTRICT COURT
SOUTHERN DISTRICT OF NEW YORK

Case No. 1:21-cv-12345

John Smith, residing at 123 Main Street, Anytown, NY 10001,
appearing by and through his attorney Jane Doe of the law firm
Doe & Associates, PLLC, with offices at 456 Park Avenue,
New York, NY 10022, moves this Court for an order granting
summary judgment in his favor.

The defendant, Acme Corporation, has failed to respond to
discovery requests served on March 15, 2024. Plaintiff requests
that the Court order sanctions against the defendant's counsel,
Robert Johnson, Esq., who can be reached at rjohnson@acme.com
or (555) 123-4567.

Additionally, plaintiff seeks to introduce into evidence the
medical records of Jane Smith (DOB: 05/15/1980) and the
financial statements showing the bank's account number
12345678901234.

Dated: November 2, 2025
Respectfully submitted,

Jane Doe, Esq.
Attorney for Plaintiff
New York Bar No. 1234567
Phone: (555) 987-6543
Email: jdoe@doelaw.com
```

## Deploying to Hugging Face Spaces

1. Create a new Gradio Space.
2. Upload `app.py`, `api_client.py`, `utils.py`, `requirements.txt`, `env.example`, and `README.md`.
3. In the Space **Settings → Secrets**, add `OPENROUTER_API_KEY` and `CEREBRAS_API_KEY` (and any optional variables).
4. Commit and wait for the Space to build. The app launches automatically.

## Usage Tips

- **Highlighting**: Redacted PII is color-coded by type (red for persons, blue for addresses, etc.). Hover over tags to see the original value.
- **Downloading**: Use the download buttons to save your redacted or restored documents with timestamps.
- **Validation**: Click "Validate PII Tags" to check if your edited text still contains all necessary tags for restoration.
- **Editing**: Box 3 allows you to edit the redacted text. Keep `<PII_*>` tags intact for successful restoration.
- **API Switching**: Switch between OpenRouter and Cerebras from the dropdown to compare redaction coverage or balance rate limits.
- **Error Handling**: The application provides detailed feedback for missing tags, duplicate detections, and API errors.

## PII Types Detected

- **PERSON**: Names of individuals (defendants, witnesses, attorneys, judges)
- **ADDRESS**: Physical addresses, mailing addresses  
- **EMAIL**: Email addresses
- **PHONE***: Phone numbers
- **SSN****: Social Security numbers
- **DRIVERS_LICENSE***: Driver's license numbers
- **PASSPORT***: Passport numbers
- **CASE_NUMBER***: Court case identifiers
- **DOCKET_NUMBER***: Docket numbers
- **DOB***: Dates of birth and other sensitive dates
- **FINANCIAL_ACCOUNT****: Bank account numbers, payment card numbers
- **MEDICAL_RECORD****: Medical record identifiers
- **ORGANIZATION***: Law firms, courts, organizations relevant to identity
