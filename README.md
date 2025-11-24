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
## Creating User
![image alt](https://github.com/v-Abhishek02/Movies_Recommendation_System_Using_ML/blob/9fd61ccc11606f15b2d3d777e4eb910b4101e882/IMG-20250312-WA0016.jpg)
## Login User
![image alt](https://github.com/v-Abhishek02/Movies_Recommendation_System_Using_ML/blob/000d303652ca0c97911dd495e3e488425c3331ff/IMG-20250312-WA0017.jpg)
## Recommendation of movies 
![image alt](https://github.com/v-Abhishek02/Movies_Recommendation_System_Using_ML/blob/00bd9942dcb3eae99ae5289da8c8214231a9f6d6/IMG-20250312-WA0019.jpg)
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
