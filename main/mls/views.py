from django.shortcuts import render
import requests
import urllib.parse
from .models import Movie

OMDB_API_KEY = "4e8e495e"
YOUTUBE_API_KEY = "AIzaSyCRG_J64TRdb1EEHW0G07e9FfhwcLFsLlA"

OMDB_API_URL = "https://www.omdbapi.com/?apikey={}&t={}"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={}%20trailer&key={}"

def admin(request):
    movie_data = None

    if request.method=='POST':
        title = request.POST.get('title',)

        #Fetch movie data from OMDB
        omdb_response = requests.get(OMDB_API_URL.format(OMDB_API_KEY, urllib.parse.quote(title)))
        omdb_data = omdb_response.json()

        if omdb_data.get("Response") =="True":
            movie_title = omdb_data.get("Title")
            description = omdb_data.get("Plot")
            poster_url = omdb_data.get("Poster")
            

            #Fetch trailer from youtube
            youtube_response = requests.get(YOUTUBE_SEARCH_URL.format(urllib.parse.quote(title),YOUTUBE_API_KEY))
            youtube_data = youtube_response.json()

            if youtube_data.get("items"):
                trailer_id = youtube_data["items"][0]["id"]["videoId"]
                trailer_url = f"https://www.youtube.com/watch?v={trailer_id}"
            else:
                trailer_url = ""

            #save movie to database
            movie, created= Movie.objects.get_or_create(
                title=movie_title,
                defaults={"description":description, "poster":poster_url, "trailer_url":trailer_url}
            )

            movie_data= {
                "title": movie.title,
                "description":description,
                "poster":poster_url,
                "trailer_url":trailer_url
            }

    return render(request,'admin_panel.html', {"movie_data": movie_data})
                                                                      

def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {"movies": movies})

