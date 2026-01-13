# 🛒 Django E-Commerce / POS System

An **E-Commerce / Point of Sale (POS)** system built with **Django**, supporting **cash payments** and **M-Pesa (STK Push)**.  
The application demonstrates core backend CRUD operations, payment integration, transactional integrity, and clean Django architecture.

---

## 🚀 Features

- Product catalog with categories
- Multiple images per product
- Stock management
- Shopping cart (auto-created per user)
- Checkout flow
- Cash payments
- M-Pesa STK Push (Sandbox)
- Order lifecycle management
- Graceful handling of stock shortages
- HTML + Bootstrap frontend
- User authentication (create & update accounts)
- Product search and pagination

---

## 🧱 Tech Stack

- **Backend:** Django
- **Frontend:** HTML, Bootstrap
- **Database:** SQLite (default)
- **Payments:** Safaricom M-Pesa STK Push (Sandbox)
- **Tunneling:** ngrok

---

## 📦 Project Structure (Simplified)
```
pos_system/
├── cart/
├── orders/
├── payments/
├── products/
├── users/
├── templates/
├── static/
├── media/
└── manage.py
```
---

## ⚙️ Setup Instructions

### Clone the Repository and setup environment

```
git clone git@github.com:Script-Savant/ecommerce-pos.git
cd ecommerce-pos/pos_system


python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Environment variables

```
SECRET_KEY=your-secret-key
DEBUG=True

MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_ENV=sandbox
MPESA_CALLBACK_URL=https://your-ngrok-url.ngrok-free.dev/payments/mpesa/callback/
```

### Apply Migrations

```
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```
python manage.py createsuperuser
```


### Run the Development Server

```
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "<ngrok-url>"]

ngrok http 8000 -> Exanple output 'https://tristful-unbailed-marquerite.ngrok-free.dev'

MPESA_CALLBACK_URL=https://<ngrok-url>/payments/mpesa/callback/

python manage.py runserver


Visit:

http://127.0.0.1:8000
```























