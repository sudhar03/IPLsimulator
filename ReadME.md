# 🏏 IPL Auction Simulator

A realistic, multi-team IPL auction simulator built with Django, Celery, and Redis. Supports dynamic bidding by users and AI-controlled teams, with real-time auction logic, player data, and purse management.

---

## 🚀 Features

- ✅ Realistic IPL-style auction flow
- 🤖 AI-controlled bidding teams with personalities (Aggressive, Underdog, Superstar, etc.)
- 💰 Purse tracking and deduction logic
- 🧠 Player evaluation with batting/bowling stats and performance % logic
- ⏱️ Time-based auction rounds (AI bidding every few seconds)
- 📦 Celery + Redis-based background tasks for AI logic
- 🧾 Finalize sold/unsold players automatically

---

## 🛠️ Tech Stack

| Layer         | Tech                             |
|---------------|----------------------------------|
| Backend       | Django 4.x                       |
| Worker Tasks  | Celery                           |
| Message Broker| Redis                            |
| ORM & DB      | Django ORM + PostgreSQL/SQLite   |
| Caching       | Django Cache (Redis backend)     |

---


---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/sudhar03/IPLsimulator.git
   cd IPLsimulator

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file and add your environment variables

5. **Run migrations**
   ```bash
   python manage.py migrate

6. **Run the development server**
   ```bash
   python manage.py runserver

7. **Run Celery worker**
   ```bash
   celery -A iplsimulator worker -l info

8. **Run Celery beat**
   ```bash
    celery -A iplsimulator beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info