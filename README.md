# 🎬 Movies Recommendation System using Machine Learning

A content-based **Movie Recommendation System** built with **Python, Flask, and Machine Learning**.  
It recommends movies similar to a user-selected movie using **cosine similarity** and displays movie details, ratings, and YouTube trailers.

---

## 🚀 **Features**
- **Movie Recommendation** based on content similarity.
- **Cosine Similarity** model trained on movie metadata.
- **TMDB API Integration** for movie posters, details, and trailers.
- **User Authentication** (Login & Signup) using MySQL.
- **Personalized Dashboard** with user history and liked movies.
- **Feedback System** for users to share suggestions.
- **Watchlist** feature to save favorite movies.

---

## 🛠 **Tech Stack**
- **Frontend:** HTML, CSS, JavaScript, Bootstrap/Tailwind
- **Backend:** Python, Flask
- **Database:** MySQL
- **Machine Learning:** Scikit-learn, Pandas, Numpy
- **API:** TMDB API for movie posters and trailers

---

## 📂 **Project Structure**
```
Movies_Recommendation_System_Using_ML/
│-- app.py                # Flask app
│-- model/                # ML models and similarity data
│-- static/               # CSS, JS, images
│-- templates/            # HTML templates
│-- requirements.txt      # Project dependencies
│-- README.md             # Project documentation
```

---

## ⚙️ **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/v-Abhishek02/Movies_Recommendation_System_Using_ML.git
cd Movies_Recommendation_System_Using_ML
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run the Flask App**
```bash
python app.py
```
Now, open your browser at `http://127.0.0.1:5000/`.

---

## 📷 **Screenshots**
*(Add screenshots of your app here)*

---

## 📝 **Future Enhancements**
- Add **Collaborative Filtering** for better recommendations.
- Improve search with **fuzzy matching**.
- Deploy on **Render/Heroku** with database integration.

---

## 🤝 **Contributing**
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 **License**
This project is licensed under the MIT License.
