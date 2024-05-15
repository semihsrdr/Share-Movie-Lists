from flask import Flask, render_template, redirect, url_for, request, session,flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests,datetime,random,smtplib
from my_movie import MyMovie



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0shgf88'
Bootstrap5(app)

api_key="84bc20f65328a210ea788f7fcd266869"
api_token="eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NGJjMjBmNjUzMjhhMjEwZWE3ODhmN2ZjZDI2Njg2OSIsInN1YiI6IjY2MmY5YWUwMDI4ZjE0MDEyNTY5NTRhYSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.yj9vGc7oBGwKw_b6qhgtbzcMRXNZnetX-muuZJ2ObaI"

def send_mail(user_mail,msg,name,surname):
    my_mail = "semihserdarsahin@gmail.com"
    my_receiver_mail="relaxingambience52@gmail.com"
    password = "kgumezrjsjnysscv"

    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=my_mail,password=password)
        connection.sendmail(from_addr=my_mail,
                            to_addrs=my_receiver_mail,
                            msg=f"Subject:YummyFood Feedback\n\n"
                                f"{msg}\n\n"
                                f"{name} {surname}\n"
                                f"{user_mail}")
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///my-movie-library.db"
db=SQLAlchemy(model_class=Base)
db.init_app(app)

class Lists(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str]=mapped_column(String,nullable=False)
    list_id:Mapped[int] = mapped_column(Integer,nullable=False)
    description:Mapped[str]=mapped_column(String)
    created_at:Mapped[str] = mapped_column(String)

class Movie(db.Model):
    id:Mapped[int]=mapped_column(Integer,nullable=False,primary_key=True)
    movie_id:Mapped[int]=mapped_column(Integer,nullable=False,unique=True)
    original_title:Mapped[str]=mapped_column(String,nullable=False)
    release_date:Mapped[int]=mapped_column(Integer,nullable=True)
    overview:Mapped[str]=mapped_column(String,nullable=True)
    vote_average:Mapped[float]=mapped_column(Float,nullable=True)
    tagline:Mapped[str]=mapped_column(String,nullable=True)
    poster_path:Mapped[str]=mapped_column(String,nullable=True)

class ListMovie(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    list_id:Mapped[int] = mapped_column(db.Integer, db.ForeignKey('lists.list_id'), nullable=False,unique=True)
    movie_id1:Mapped[int] = mapped_column(db.Integer, nullable=False)
    movie_id2: Mapped[int] = mapped_column(db.Integer, nullable=True)
    movie_id3: Mapped[int] = mapped_column(db.Integer, nullable=True)
    movie_id4: Mapped[int] = mapped_column(db.Integer, nullable=True)
    movie_id5: Mapped[int] = mapped_column(db.Integer, nullable=True)
    movie_id6: Mapped[int] = mapped_column(db.Integer, nullable=True)
    movie_id7: Mapped[int] = mapped_column(db.Integer, nullable=True)
    movie_id8: Mapped[int] = mapped_column(db.Integer, nullable=True)
    movie_id9: Mapped[int] = mapped_column(db.Integer, nullable=True)
    movie_id10: Mapped[int] = mapped_column(db.Integer, nullable=True)

class List_Ratings(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    list_id:Mapped[int] = mapped_column(db.Integer, db.ForeignKey('lists.list_id'), nullable=False)
    movie_rating1:Mapped[int] = mapped_column(db.Integer, nullable=False)
    movie_rating2: Mapped[int] = mapped_column(db.Integer, nullable=False)
    movie_rating3: Mapped[int] = mapped_column(db.Integer,nullable=False)
    movie_rating4: Mapped[int] = mapped_column(db.Integer, nullable=False)
    movie_rating5: Mapped[int] = mapped_column(db.Integer, nullable=False)
    movie_rating6: Mapped[int] = mapped_column(db.Integer, nullable=False)
    movie_rating7: Mapped[int] = mapped_column(db.Integer, nullable=False)
    movie_rating8: Mapped[int] = mapped_column(db.Integer,nullable=False)
    movie_rating9: Mapped[int] = mapped_column(db.Integer, nullable=False)
    movie_rating10: Mapped[int] = mapped_column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

class ListForm(FlaskForm):
    title=StringField('Title of Your List',validators=[DataRequired()],render_kw={"placeholder": "eg. Most Dramatic Movies"})
    description = StringField('Description',render_kw={"placeholder": "Your Opinions"})
    submit=SubmitField("Create",id="dark-button")
class SearchForm(FlaskForm):
    title=StringField('Name of Movie',validators=[DataRequired()],render_kw={"placeholder": "eg. Matrix"})
    submit=SubmitField("Search",id="dark-button")

def id_generator():
    id=""
    for i in range(10):
        id+=str(random.randint(0,10))
    return int(id)

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

@app.route("/start",methods=["POST","GET"])
def start():
    form=ListForm()
    if form.validate_on_submit():
        title=form.title.data
        description=form.description.data
        list_id=id_generator()
        date = datetime.datetime.now()
        my_list=Lists(title=title,description=description,list_id=list_id,created_at=str(date))

        db.session.add(my_list)
        db.session.commit()
        return redirect(url_for('search',list_id=list_id))
    return render_template("start.html",form=form)

@app.route("/search/<int:list_id>",methods=["POST","GET"])
def search(list_id):
    form=SearchForm()
    id_counter=0
    try:
        if "movie_id" not in session:
            session['movie_id'] = []
            session['movie_title'] = []
        movie_ids = session['movie_id']
        movie_names = session["movie_title"]
        id_counter=len(movie_ids)
        print("length movie ids : ",id_counter)
        print("Movie names: ", movie_names)
    except Exception as e:
        pass
    if form.validate_on_submit():
        if id_counter <=9:
            title=form.title.data
            return redirect(url_for('choose_movie', title=title, list_id=list_id))
        else:
            new_list_movie = ListMovie(list_id=list_id,
                                       movie_id1=movie_ids[0],
                                       movie_id2=movie_ids[1],
                                       movie_id3=movie_ids[2],
                                       movie_id4=movie_ids[3],
                                       movie_id5=movie_ids[4],
                                       movie_id6=movie_ids[5],
                                       movie_id7=movie_ids[6],
                                       movie_id8=movie_ids[7],
                                       movie_id9=movie_ids[8],
                                       movie_id10=movie_ids[9],
                                       )
            db.session.add(new_list_movie)
            db.session.commit()
            return redirect(url_for('share_part',list_id=list_id))
    return render_template("search_movie.html",form=form,movies=movie_names,list_id=list_id)

@app.route("/choose_movie/<int:list_id>/<path:title>",methods=["POST","GET"])
def choose_movie(title,list_id):
    if 'movie_id' not in session:
        session['movie_id'] = []

    if request.method=="GET":
        url = "https://api.themoviedb.org/3/search/movie?"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_token}",
        }
        params = {
            "query": title.lower()
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()["results"]
        return render_template("choose_movie.html",movies=data,list_id=list_id)


@app.route("/choose_movie/<int:list_id>/<int:movie_id>/<path:movie_title>")
def add_movie(list_id,movie_id,movie_title):
    if 'movie_title' not in session:
        session['movie_title'] = []
    if movie_id not in session["movie_id"] and movie_title not in session["movie_title"]:
        flash("You have been added successfully your movie!")
        session["movie_title"].append(movie_title)
        session.modified = True
        session["movie_id"].append(movie_id)
        session.modified = True
    else:
        flash("You couldn't add your movie!")
    return redirect(url_for('search',list_id=list_id))

@app.route("/<int:list_id>")
def show_movies(list_id):
    selected_list=db.session.execute(db.select(ListMovie).where(ListMovie.list_id==list_id)).scalar()
    list_info=db.session.execute(db.select(Lists).where(Lists.list_id==list_id)).scalar()
    title=list_info.title
    description=list_info.description
    columns=vars(selected_list).items()
    ids=[]
    base_url = "https://image.tmdb.org/t/p/original/"
    movie_datas=[]
    for i,j in columns:
        if i !="list_id" and i!="id" and "_sa_instance_state" not in i:
            ids.append(j)

    for id in ids:
        if id!=None:
            selected_movie = db.session.execute(db.select(Movie).where(Movie.movie_id == id)).scalar()
            if selected_movie:
                film = MyMovie(selected_movie.original_title, selected_movie.release_date, selected_movie.overview,
                            selected_movie.vote_average, selected_movie.tagline, selected_movie.poster_path)
                movie_datas.append(film)

                print("Bulundu. Databaseden veriler alınıyor...")
            else:
                print("Bulunamadı. Api'den bakılıyor...")
                base_url = "https://image.tmdb.org/t/p/original/"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {api_token}"
                }
                response = requests.get(url=f"https://api.themoviedb.org/3/movie/{id}", headers=headers)
                data = response.json()
                to_database_movie=Movie(movie_id=id,
                                        original_title=data["original_title"],
                                        release_date=data["release_date"],
                                        overview=data["overview"],
                                        vote_average=data["vote_average"],
                                        tagline=data["tagline"],
                                        poster_path=data["poster_path"])
                db.session.add(to_database_movie)
                db.session.commit()
                selected_movie=db.session.execute(db.select(Movie).where(Movie.movie_id==id)).scalar()
                film = MyMovie(selected_movie.original_title, selected_movie.release_date, selected_movie.overview,
                               selected_movie.vote_average,
                               selected_movie.tagline,
                               selected_movie.poster_path)
                movie_datas.append(film)
    sorted_movie_datas = sorted(movie_datas,key=lambda x:x.vote_average,reverse=True)

    return render_template("show_movies.html",movies=sorted_movie_datas,base_url=base_url,title=title,description=description)

@app.route("/share/<int:list_id>")
def share_part(list_id):
    url_ready=f"http://127.0.0.1:5000/{list_id}"
    return render_template("share_part.html",url=url_ready)

@app.route("/create_list<int:list_id>")
def create_list(list_id):
    movie_ids=session["movie_id"]
    full_movie_ids = movie_ids + [None] * (10 - len(movie_ids))
    new_list_movie = ListMovie(
        list_id=list_id,
        movie_id1=full_movie_ids[0],
        movie_id2=full_movie_ids[1],
        movie_id3=full_movie_ids[2],
        movie_id4=full_movie_ids[3],
        movie_id5=full_movie_ids[4],
        movie_id6=full_movie_ids[5],
        movie_id7=full_movie_ids[6],
        movie_id8=full_movie_ids[7],
        movie_id9=full_movie_ids[8],
        movie_id10=full_movie_ids[9],
    )
    db.session.add(new_list_movie)
    db.session.commit()
    return redirect(url_for('share_part', list_id=list_id))

@app.route("/contact",methods=["POST","GET"])
def contact_page():
    if request.method == 'POST':
        user_address = request.form["email"]
        msg = request.form["comments"]
        name = request.form["firstName"]
        surname = request.form["lastName"]
        send_mail(user_address, msg, name, surname)
        flash("You have been sent successfully!")
        return render_template("contact_page.html")
    return render_template("contact_page.html")

if __name__=="__main__":
    app.run(debug=True)