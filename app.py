from flask import Flask, render_template, request,redirect,url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import pickle
import requests
from dotenv import load_dotenv
import os

# i loaded the env
load_dotenv() 


app = Flask(__name__)

#secret key
app.secret_key = os.getenv("SECRET_KEY")

#connecting to database
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

mysql = MySQL(app)
login_manage = LoginManager()
login_manage.init_app(app)
bcrypt=Bcrypt(app)

#loading the user funtion
@login_manage.user_loader
def load_user(user_id):
    return User.get(user_id) # type: ignore

class User(UserMixin):
    def __init__(self,user_id,name,email):
        self.id=user_id
        self.name=name
        self.email=email
        
        
    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT name,email from users where id =%s',(user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(user_id, result[0],result[1])
        
        
# Loading the models and data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    api_key = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500"


def fetch_movie_details(movie_id):
    api_key = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    details = {
        "title": data.get("title", "N/A"),
        "release_date": data.get("release_date", "N/A"),
        "rating": data.get("vote_average", "N/A"),
        "overview": data.get("overview", "N/A"),
    }
    return details


def fetch_trailer(movie_id):
    api_key = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    videos = data.get('results', [])
    for video in videos:
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None


def recommend(movie):
    """
    Recommends movies based on the input movie.
    """
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_details = []  # To hold additional details
    recommended_movie_trailers = []  # To hold trailer links

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_details.append(fetch_movie_details(movie_id))  # Fetch details
        recommended_movie_trailers.append(fetch_trailer(movie_id))  # Fetch trailer

    return recommended_movie_names, recommended_movie_posters, recommended_movie_details, recommended_movie_trailers


#creating Registraion pagae

@app.route('/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (name,email,password) values(%s,%s,%s)',(name,email,hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))
        
    return render_template('register.html')

#creating Login page 

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT id,name,email,password from users where email = %s',(email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and bcrypt.check_password_hash(user_data[3],password):
            user = User(user_data[0],user_data[1],user_data[2])
            login_user(user)
        return redirect(url_for('home'))
    
    return render_template('login.html')

#creating final home page 
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    recommended_movies = []
    posters = []
    details = []
    trailers = []
    selected_movie = None

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        if selected_movie:
            recommended_movies, posters, details, trailers = recommend(selected_movie)

 # Storing  watch history
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO watch_history (user_id, movie_name) VALUES (%s, %s)", 
                (current_user.id, selected_movie)
            )
            mysql.connection.commit()
            cursor.close()
#storing liked movie 
    movie_name = request.form.get('movie_name')  
    
    if movie_name:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO liked_movies (user_id, movie_name) VALUES (%s, %s)", 
            (current_user.id, movie_name)
        )
        mysql.connection.commit()
        cursor.close()

    movie_list = movies['title'].values
    return render_template(
        'home.html', 
        movie_list=movie_list, 
        selected_movie=selected_movie, 
        recommended_movies=recommended_movies, 
        posters=posters, 
        details=details,  # Pass details to the template
        trailers=trailers,  # Pass trailers to the template
        zip=zip
    )

#creating watch movies  route 
@app.route('/history')
@login_required
def history():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT movie_name FROM watch_history WHERE user_id = %s ORDER BY timestamp DESC", (current_user.id,))
    watch_history = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return render_template('watch.html', watch_history=watch_history)

#creating liked movies route 
@app.route('/liked_movies', methods=['POST','GET'])
@login_required
def liked_movies():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT movie_name FROM liked_movies WHERE user_id = %s", (current_user.id,))
    liked_movies = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return render_template('liked.html', liked_movies=liked_movies)


@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    rating = request.form['rating']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO feedback (name, email, message, rating) VALUES (%s, %s, %s, %s)", (name, email, message, rating))
    mysql.connection.commit()
    cursor.close()

    print("Feedback submitted successfully!", "success")
    return redirect(url_for('account'))

# About Page (Display Feedback)
@app.route('/account')
@login_required
def about():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, email, message, rating FROM feedback ORDER BY timestamp DESC LIMIT 5")
    feedbacks = cursor.fetchall()
    cursor.close()
    return render_template("account.html", feedbacks=feedbacks)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)


#creating logout route 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)