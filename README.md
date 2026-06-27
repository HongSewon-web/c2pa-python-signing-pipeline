# c2pa-python-signing-pipeline

A C2PA content signing pipeline using [c2pa-python](https://github.com/contentauth/c2pa-python) SDK.

Supports signing and verification of:
- JPEG (`.jpg`)
- RAW (`.dng`)
- Video (`.mp4`)
- PDF (converted to per-page signed JPEGs)

## Background

Built during C2PA Generator Product conformance certification process with SSL.com.
Solves two key nonconformities that `c2patool` cannot handle via static JSON:
1. `assertion.action.ingredientMismatch` — fixed by dynamically referencing ingredient `instance_id`
2. `c2pa.actions` placed in `gathered_assertions` — fixed by setting `"created": True` in manifest

## Requirements

```bash
pip install c2pa-python pymupdf
```

## Setup

You need a signing certificate and private key in PEM format.
For testing, generate a self-signed chain:

```bash
python make_test_cert.py
```

## Usage

```bash
# Sign
python sign_jpg.py
python sign_dng.py
python sign_mp4.py
python sign_pdf.py  # converts PDF pages to signed JPEGs

# Verify
python verify.py <file_path> <mime_type>
python verify.py output_signed.jpg image/jpeg
```

## Notes

- `signingCredential.untrusted` will appear when using test certificates
- Replace `test_cert_chain.pem` / `test_key_chain.pem` with a CA-signed certificate for production use
- PDF signing is a workaround (c2pa-rs does not yet support native PDF signing)

## Author

Sewon Hong  
POSTECH Semiconductor Engineering  
[Timelimit Inc.](https://tlimit.co.kr)
