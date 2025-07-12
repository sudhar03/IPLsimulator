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
