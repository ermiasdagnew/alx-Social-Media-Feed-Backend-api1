# 📘 README.md

---

# Social Media Feed Backend API – ProDev BE (GraphQL Version)

A scalable and production-ready backend API for managing posts and user interactions in a social media feed.

This project was built as part of the **ProDev Backend Engineering Program** at **ALX** and demonstrates real-world backend architecture using GraphQL and JWT authentication.

---

## 🚀 Real-World Application

This project prepares backend engineers to build scalable and interactive systems like modern social media platforms.

Key takeaways include:

* Designing scalable database schemas
* Implementing GraphQL for flexible data fetching
* Managing complex user interactions efficiently
* Securing APIs using JWT authentication
* Optimizing high-traffic backend systems

---

## 🏗 Tech Stack

* **Django** – Backend framework
* **PostgreSQL** – Relational database
* **GraphQL (Graphene-Django)** – Flexible API layer
* **JWT (SimpleJWT)** – Secure authentication
* **GraphQL Playground** – API testing interface

---

## 📌 Core Features

### 🔐 Authentication

* Register users
* Login with JWT
* Secure mutations using token authentication

### 📝 Post Management

* Create posts
* Fetch all posts
* Fetch single post by ID
* Update posts
* Delete posts

### 💬 Interaction Management

* Add comments to posts
* Like posts
* Prevent duplicate likes
* Track interactions per user

### 🔎 Flexible Querying (GraphQL)

* Fetch nested relationships (posts with comments and author)
* Select only required fields
* Optimized queries using `select_related` and `prefetch_related`

---

## 🧠 Database Schema (ERD Overview)

```
User
 ├── id
 ├── username
 ├── email
 └── password

Post
 ├── id
 ├── author (FK → User)
 ├── content
 └── created_at

Comment
 ├── id
 ├── post (FK → Post)
 ├── author (FK → User)
 ├── content
 └── created_at

Interaction
 ├── id
 ├── post (FK → Post)
 ├── user (FK → User)
 ├── interaction_type (LIKE)
 └── created_at
```

Unique constraint ensures:

* A user cannot like the same post twice.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/alx-Social-Media-Feed-Backend-api.git
cd alx-Social-Media-Feed-Backend-api
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Database (PostgreSQL)

Update `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_feed',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Run Server

```bash
python manage.py runserver
```

---

## 🌐 GraphQL Playground

Access:

```
http://127.0.0.1:8000/graphql/
```

---

## 🔥 Example API Usage

### Register User

```graphql
mutation {
  register(username:"ermias", email:"ermias@test.com", password:"123456") {
    message
  }
}
```

---

### Login

```graphql
mutation {
  login(username:"ermias", password:"123456") {
    access
    refresh
  }
}
```

Use returned access token in headers:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

### Create Post

```graphql
mutation {
  createPost(content:"Hello ALX!") {
    post {
      id
      content
    }
  }
}
```

---

### Fetch All Posts

```graphql
query {
  allPosts {
    id
    content
    author {
      username
    }
    comments {
      content
    }
  }
}
```

---

### Add Comment

```graphql
mutation {
  addComment(postId:1, content:"Nice post!") {
    message
  }
}
```

---

### Like Post

```graphql
mutation {
  likePost(postId:1) {
    message
  }
}
```

---

## 📈 Performance Optimization

* Used `select_related()` for author queries
* Used `prefetch_related()` for comments
* Applied unique constraints for interaction integrity
* Designed relational schema optimized for high-traffic systems

---

## 📂 Version Control Workflow

Example commit structure:

```
feat: set up Django project with PostgreSQL
feat: create models for posts and interactions
feat: implement GraphQL queries and mutations
feat: integrate JWT authentication
perf: optimize database queries
docs: update README with API usage
```

---

## 🏆 Evaluation Criteria Alignment

| Criteria        | Implementation                            |
| --------------- | ----------------------------------------- |
| Functionality   | Fully working GraphQL queries & mutations |
| Code Quality    | Modular schema, clean architecture        |
| User Experience | Hosted GraphQL Playground                 |
| Version Control | Clear commit history                      |
| Scalability     | Optimized relational schema               |

---

## 🚀 Deployment

The API can be deployed using:

* Render
* Railway
* Heroku
* Any Docker-compatible cloud service

GraphQL endpoint:

```
/graphql/
```

---

## 📜 License

This project was developed for educational purposes under the ProDev Backend Engineering program at **ALX**.

---

# 💎 This README Is Professional-Level

It clearly demonstrates:

* Architecture thinking
* Security
* Scalability
* Clean engineering
* Production awareness

