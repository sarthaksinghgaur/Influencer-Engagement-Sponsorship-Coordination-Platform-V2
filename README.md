# EcoConnect 🌱

**EcoConnect** is a sustainability-focused web platform developed during the Hacksprint Hackathon (Jan–Feb 2025) under the theme **"Tech for Social Good."** The project connects users with local recycling centers, verified eco-friendly businesses, and environmental community initiatives, promoting a greener lifestyle through actionable insights and community engagement.

## 🏆 Achievements

* Placed **7th overall** among all participating teams
* Recognized for **technical robustness** and **social impact**

---

## 🌟 Features

* 🔐 **User Authentication**: Secure login/signup using Flask-Security with role-based access control (users, businesses, admins)
* ♻️ **Waste Tracking System**: Users can log, categorize, and filter waste entries by type and date
* 🏪 **Eco-Business Directory**: Search and discover verified eco-friendly businesses
* 🧾 **Business Verification Workflow**: Admins can verify businesses, and users can leave reviews
* ⚡ **Fast REST API**: Modular, well-documented, and scalable Flask-based RESTful API
* 📃 **Community Initiative Management**: Create and join environmental activities in local communities
* ✅ **Data Validation & Error Handling**: Marshmallow schemas for structured validation and clean error responses

---

## ⚙️ Tech Stack

### Backend

* **Flask** (Python web framework)
* **SQLite** (lightweight relational database)
* **Flask-Security** (user auth & roles)
* **SQLAlchemy** (ORM)
* **Postman** (API testing)

### Frontend (Collaborative Integration)

* Vue.js interface (handled by frontend developers)
* Axios (for API calls)
* Integrated via RESTful endpoints

### Tools & Practices

* GitHub Projects (Agile task management)
* Modular codebase & scalable design
* Deployment-ready documentation & scripts

---

## 🚀 How to Run the Project

## for the app to running front-end 
    1> create a virtual env into root directry 
    2> run # python3 init_app.python3 //reset the database and add admin
    3> run # python3 app.py //will start the backend server

## for the app to running back-end
    1> cd to frontend
    2> run #npm install   // to load node module
    3> run # npm run serve   // start the front end

## starting Redis Server for daily and monthly reminder
    sudo redis-server start
    redis-server

# ## stopping redis -server
    sudo service redis-server stop

# ## check if redis-server active
    redis-cli ping 
    respone should be "PONG"

## start celery worker
    celery -A app.celery_app worker --loglevel=INFO

## start celery beat
    celery -A app.celery_app beat --loglevel=INFO

---

## 👨‍💼 Author

**Sarthak Singh Gaur**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> “Small acts, when multiplied by millions of people, can transform the world.” — Howard Zinn
