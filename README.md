# 🚀 Startup Backend – – Backoffice Tool for Tourism Agencies (API)

A high-performance Django REST Framework (DRF) backend powering the **Startup Client** backoffice tool. Designed for Destination Management Companies (DMCs), this API handles customer data, itinerary management, confirmations, and financial operations with secure, scalable endpoints.

---

## 🎯 Purpose

This project demonstrates my ability to architect a **production-ready backend** with:
- RESTful API design
- Authentication/authorization flows
- Database optimization
- Third-party integrations (e.g., payment gateways, email services)

---

## 🛠 Tech Stack

| Category           | Technologies                                                              |
|--------------------|---------------------------------------------------------------------------|
| **Core**           | Django 4.2+, Django REST Framework                                        |
| **Database**       | PostgreSQL (production), SQLite (development)                             |
| **Auth**           | JWT (SimpleJWT), OAuth2 (planned)                                         |
| **Infrastructure** | Docker (planned)                                                          |

---

## 💡 Key Features

### ✅ Implemented
- **Customer API**: CRUD operations with search/filter
- **Itinerary Management**: Nested serializers for complex trip structures
- **Confirmation System**
  - Status tracking (Done/In Progress/Cancelled)
  - Priority levels (High/Medium/Low)
  - Deposit amount validation
- **Action Plan Engine**
  - Nested entries with date/time ordering
  - Status tracking (Pending/Confirmed/Issued)
  - Supplier and rate management
- **Accommodation Management**
  - Check-in/out date validation
  - Cancellation policy storage
- **Advanced Features**
  - Custom URL endpoints for relationship-based deletion
  - Query parameter filtering (`?confirmation_id=X`)
  - Comprehensive error logging


### 🔜 Planned
- **JWT Authentication**: Secure token-based auth
- **Financial Integration**: Invoice generation, payments, and reporting
- **Document Storage**: File uploads to S3
- **Webhooks**: For third-party integrations
- **WebSocket Support**: Real-time notifications


---

## 📁 Project Structure

```plaintext
startup-backend/
├── backend/                # Core Django config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Split settings recommended
│   └── urls.py            # Router configurations
│
├── confirmations/          # Main app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py          # All data models
│   ├── serializers.py     # Custom validators
│   ├── urls.py           # ViewSet routes
│   └── views.py          # Business logic
│
├── venv/
├── .gitignore
├── db.sqlite3
├── manage.py
└── README.md
