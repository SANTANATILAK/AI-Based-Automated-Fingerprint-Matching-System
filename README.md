# AI-Based-Automated-Fingerprint-Matching-System
This project implements an AI-based fingerprint matching system that simulates rapid crime-scene identification. It uses convolutional neural networks and feature extraction techniques to match fingerprints against a database and provide similarity scores instantly, reducing investigation time

## Structure

- `fingerprint_model.py` – image preprocessing and model-building utilities.
- `app.py` – Flask application providing upload form and prediction endpoint.
- `fingerprint_matcher.html` – HTML form for uploading a fingerprint image.

## Setup

1. Create a Python virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Train or save a model using `fingerprint_model.build_and_save_model()` or
   provide a pre-trained `fingerprint_model.h5` in the workspace root.

3. Run the Flask app:

```bash
python app.py
```

4. Open `http://localhost:5000` in a browser and use the upload form.

## Security Considerations

- User authentication with hashed passwords (Flask-Login).
- SQLAlchemy ORM protects against SQL injection.
- Uploads are restricted by extension and size (max 16 MB).
- Filenames are sanitized with `werkzeug.utils.secure_filename`.
- After saving, images are validated with `imghdr` before use.
- CSRF tokens are available via Flask-WTF templates.
- Use HTTPS in production, configure a strong `SECRET_KEY`, and store it
  outside version control.

## Fingerprint Matching Flow

1. Investigator logs in and uploads a crime-scene fingerprint image.
2. The system preprocesses the image (grayscale, resize to 128×128, normalize).
3. A CNN extracts a 128‑dimensional feature vector.
4. The vector is compared against the database using cosine similarity.
5. Top matches are shown with ID, similarity score, and dummy address.
6. Match events are recorded in `match_history` for auditing.

## Database Schema

- **users** – authentication accounts with roles (admin flag).
- **fingerprints** – stored records with name, address, image path, and
  raw feature vector.
- **match_history** – logs each search with timestamp and score.

SQLite is used by default; switch to MySQL/MongoDB by adjusting
`DATABASE_URL`.

## Model Details

The CNN used for feature extraction is defined in `fingerprint_model.py`:

```
Conv2D(32, (3,3), relu)
MaxPooling2D
Conv2D(64, (3,3), relu)
MaxPooling2D
Flatten
Dense(128, relu)    # feature vector layer
Dense(10, softmax)  # classifier (optional)
```

Only the penultimate dense layer is used for matching, yielding a 128‑dim
vector. Input images are 128×128 grayscale.

## Admin Dashboard

Admins can:

- Upload new fingerprints (with metadata).
- View and delete existing records.
- Later: view match history and statistics.

## Performance & Scalability

- Matching is a linear scan over stored vectors; for 500–1000 fingerprints the
  response time should be well under 3 seconds on modern hardware.
- Consider approximate nearest‑neighbor libraries (Faiss, Annoy) when scaling
  further.

## Extending the Project

Additional ideas:

- Role‑based access control and audit logging.
- Fingerprint quality/score calculations using OpenCV.
- REST API for headless integration.
- Mobile‑responsive UI with Bootstrap (already included).

## Getting Started

(keep earlier setup instructions)
