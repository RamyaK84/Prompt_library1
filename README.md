# 🎓 Student & HR Prompt Library

A full-featured AI Prompt Library for students and HR professionals, built with Python Flask.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

### 3. Open in Browser
```
http://localhost:5000
```

---

## 🔐 Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| 👑 Admin/Owner | admin@demo.com | admin123 |
| 👨‍🎓 Student | student@demo.com | student123 |

---

## ✨ Features

- 📋 **25 curated prompts** across 8 categories
- 🔍 **Keyword Search** & **Smart AI Semantic Search**
- ⭐ **5-star rating system** with reviews
- ❤️ **Favourites** for logged-in users
- 🌐 **English / Tamil** language switching
- 👤 **Profile personalization** (auto-fills {{name}}, {{department}}, {{year}}, {{college}})
- ✨ **Prompt Generator** - describe your need, get the best match
- 👑 **Admin Dashboard** with analytics and review moderation
- 🔒 Guest users: 5 free copies, Login for unlimited

## 📁 Project Structure

```
prompt_library/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions
├── requirements.txt
├── data/
│   └── prompts.json    # 25 curated prompts
├── models/             # SQLAlchemy models
├── routes/             # Flask route blueprints
├── services/           # Business logic layer
├── utils/              # Utility modules
├── templates/          # Jinja2 HTML templates
└── static/             # CSS, JS assets
```

## 🏗️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Search**: Keyword + Sentence Transformers (all-MiniLM-L6-v2)
- **Auth**: Flask-Login + Bcrypt
- **Frontend**: HTML, CSS, JavaScript (no framework)
- **Languages**: English + Tamil (JS translations)
