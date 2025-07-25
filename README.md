# 🔗 YaCut — URL Shortener

## Description

Want to share a link to an interesting resource with your friends? Use our URL shortener — everything that’s not lost can be found!

## Technology Stack

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/-Flask-464646?style=flat&logo=Flask&logoColor=white&color=000000)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&logo=SQLAlchemy&logoColor=red&color=800000)](https://www.sqlalchemy.org/)

## Installation

Clone the repository and navigate into it from the command line:

```bash
git clone 
```

```bash
cd yacut
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
```

* On **Linux/macOS**:

```bash
source venv/bin/activate
```

* On **Windows**:

```bash
source venv/scripts/activate
```

Install the dependencies from `requirements.txt`:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

---

## Usage

Initialize the database with:

```bash
flask db upgrade
```

Then run the project:

```bash
flask run
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser and start shortening links!

---

## API Endpoints

* `POST /api/id/` expects a JSON body like:

  ```json
  { 
    "url": "the-url-you-want-to-shorten", 
    "short_id": "your-custom-short-id" 
  }
  ```

* `GET /api/id/<short_id>/` returns the original URL in the format:

  ```json
  { 
    "url": "the-original-url" 
  }
  ```
