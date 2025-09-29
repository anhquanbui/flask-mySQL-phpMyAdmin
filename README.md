# MyApp – Flask + MySQL + phpMyAdmin (Docker Compose)

This project contains a simple web application using **Flask** with a **MySQL** database and **phpMyAdmin** interface, all managed via Docker Compose.

---

## 📦 Requirements
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Setup

Clone the repository:
```bash
git clone https://github.com/anhquanbui/flask-mySQL-phpMyAdmin
cd myapp
```

Create an `.env` file in the project root with your secrets:
```env
MYSQL_ROOT_PASSWORD=RootPass123!
MYSQL_DATABASE=mydb
MYSQL_USER=appuser
MYSQL_PASSWORD=AppPass123!
APP_USER=admin
APP_PASSWORD=superStrongPass123
```

---

## ▶️ Run

Build and start all services:
```bash
docker compose up -d --build
```

---

## 🌐 Access

- Flask app → [http://localhost:5000](http://localhost:5000)  
- phpMyAdmin → [http://localhost:8080](http://localhost:8080)  

---

## 🛑 Stop
```bash
docker compose down
```

If you also want to delete volumes (⚠️ this removes the database data):
```bash
docker compose down -v
```

---

## 📂 Project Structure
```
myapp/
│── docker-compose.yml
│── .env
│── web/
│    ├── app.py
│    └── requirements.txt
│── pma-proxy/
│    ├── nginx.conf
│    └── .htpasswd
```

---

## Notes
- Database data is stored in Docker volume `db_data` so it persists across container restarts.
- Change `.env` credentials before using in production.
