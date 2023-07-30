# imdb250top
This project crawls the IMDb top 250 movies website and collects data about the movies and the persons involved. It then creates a database named imdb250 with tables for movie, person, cast, crew, and genre_movie. It also uses the streamlit library to generate some charts and tables based on the data.

The project consists of three files:

•  crawl.py: This file crawls the IMDb top 250 movies website and saves the data in two json files: imdb_250_movies.json and imdb_persons_id.json.

•  database.ipynb: This file creates the imdb250 database and the tables using the data from the json files.

•  dashboard.py: This file uses the streamlit library to import the data from imdb_250_movies.json and create some visualizations using matplotlib and pandas.
