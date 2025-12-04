# 🛰️ Field Ops Asset Tracking System

A Django-based web application for tracking field assets using **QR codes**, **geolocation**, and a **check-in/check-out workflow**.

🔗 **Live Demo:**  
https://fieldops-2.onrender.com/assets/login/

---

## 🚀 Overview
This system digitizes asset tracking by enabling QR scanning, real-time GPS updates, asset history logs, and a dashboard for monitoring asset status and movements.

---

## ⭐ Features
- Add Asset 
- Auto **QR Code Generation** for assets  
- **QR Scanning** using mobile camera  
- **Check-In / Check-Out** workflow  
- **Geo-Tagging** (captures GPS location)  
- **Dashboard & Analytics**  
- **Asset Detail Page** with map  
- **Asset History Tracking**  
- **CSV Export**  
- **User Authentication & Admin Panel**

---

## 🛠 Tech Stack
**Backend:** Django, Django REST Framework  
**Frontend:** HTML, CSS, Bootstrap, JavaScript  
**Database:** SQLite  
**Libraries:** python-qrcode, html5-qrcode, Leaflet.js  
**Deployment:** Render  

---
## Screenshot:
<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/becd1b84-60c9-461c-adce-44ac3302c25c" />
<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/3ffbe9b2-3da7-4759-b8f1-ad65d798ab03" />

## ▶️ Installation
```bash
git clone <your-repo-link>
cd field-ops-asset-tracking

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


