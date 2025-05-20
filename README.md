# Influencer Engagement & Sponsorship Coordination Platform

## 📌 Overview

This web application is a role-based platform designed to streamline interactions between **Influencers**, **Sponsors**, and **Admins**. The platform facilitates campaign creation, sponsorship management, and ad requests through a clean and efficient interface built with **Flask**, **Vue.js**, **Redis**, and **Celery**.

## 🔧 Tech Stack

* **Backend**: Flask, Flask-Security, Flask-SQLAlchemy, Flask-Migrate, Redis, Celery
* **Frontend**: Vue.js, TailwindCSS
* **Database**: SQLite (development), PostgreSQL (production-ready)
* **Task Queue**: Celery with Redis broker
* **Authentication**: Role-based access control using Flask-Security
* **Version Control**: Git & GitHub

## 🚀 Features

### 👤 Role-Based Access

* **Admin**: Manages user approvals, roles, and campaigns
* **Influencer**: Applies for campaigns, receives ad requests, manages profile
* **Sponsor**: Creates campaigns, sends ad requests, views influencer applications

### 📋 Functional Modules

* **User Authentication**: Registration, login, logout using Flask-Security
* **Campaign Management**: Sponsors create, update, and view campaigns
* **Ad Requests**: Sent by sponsors to influencers; influencers can accept or reject
* **Celery Tasks**: Handles background tasks like sending approval emails
* **Admin Approval System**: Sponsors need admin approval to access platform features


## 🎯 Achievements

* Successfully implemented a secure and scalable role-based platform
* Enabled asynchronous email workflows using Celery
* Followed clean software engineering practices with modular design

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
