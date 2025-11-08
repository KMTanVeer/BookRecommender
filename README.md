# 📚 Book Recommender System — Collaborative Filtering Based

A fully functional **Book Recommendation Web App** built using **Flask** and **Collaborative Filtering**.  
It recommends books similar to a user’s favorite and also displays top-rated books from the dataset.

🌐 **Live Demo:** [Book Recommender on Render](https://bookrecommender-s80k.onrender.com)

---

## 🚀 Features

- 🔍 **Personalized Book Suggestions** based on similarity between users and books  
- ⭐ **Top-Rated Books Section** showing the most popular titles  
- 📖 **Modern, Clean Web Interface** built with Bootstrap & custom CSS  
- 💾 **Preprocessed Data (.pkl)** for instant predictions  
- 🌐 **Deployed on Render.com** (Free cloud hosting)  
- 🔒 **Automatic HTTPS Conversion** for all book cover URLs  

---

## 🧠 How It Works

1. The dataset (Kaggle) is cleaned and processed using Python.  
2. A **user-book interaction matrix (pt.pkl)** and a **similarity matrix (similarity_scores.pkl)** are created.  
3. The app finds the top similar books using **Collaborative Filtering** (cosine similarity).  
4. Flask renders the result dynamically — displaying book covers, titles, and authors.  

---

## 🧩 Tech Stack

| Category | Tools / Technologies |
|-----------|----------------------|
| Language | Python |
| Framework | Flask |
| Libraries | Pandas, NumPy, Scikit-learn |
| Frontend | HTML, CSS, Bootstrap |
| Deployment | Render.com (Gunicorn) |
| IDE | PyCharm / VS Code |
| Data Format | Pickle (`.pkl`) Files |

---

## 🛠️ Installation & Setup (Run Locally)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/KMTanVeer/BookRecommender.git
cd BookRecommender
