import streamlit as st
from pathlib import Path
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns 
import numpy as np

st.set_page_config(
    page_title='Quera BootCamp',
)
st.title("Advanced Python Exercise")

"""
*Farzaneh Soltanzadeh*

run streamlit app by running :
    ```
    python -m streamlit run dashboard.py
    ```

[Imdb250TopMovies](https://www.imdb.com/chart/top/?ref_=nv_mv_250) [Quera](quera.org)
"""


# get data
base_path = Path().absolute()

@st.cache_data
def read_dataframe(path:str) :
    return pd.read_json(path, dtype={'id': str, 'year': str, 'gross_us_canada': int})

df_movies = read_dataframe(base_path / "imdb_250_movies.json").set_index('id')



# -- Part 1.1
st.subheader('Part 1.1')
year_selected = st.slider(
    'Select a range of values',
    1900, 2030, (1990, 2022))
st.write(f'Top 250 imdb movies from **{year_selected[0]}** to **{year_selected[1]}**:')
# filter dataFrame by selected years
st.dataframe(df_movies.loc[(df_movies['year'].apply(lambda x: int(x)) >= year_selected[0]) & (df_movies['year'].apply(lambda x: int(x)) <= year_selected[1])].sort_values('year'))



# -- Part 1.2
st.subheader('Part 1.2')
runtime_start = st.number_input("start", min_value=0, value=60)
runtime_end = st.number_input("end", min_value=0, value=90)
if runtime_start > runtime_end : runtime_start, runtime_end = runtime_end, runtime_start
# filter dataFrame by runtime(minutes)
st.write(f'Top 250 imdb movies from **{runtime_start}** minutes to **{runtime_end}** minutes:')
st.dataframe(df_movies.loc[(df_movies['runtime'] >= runtime_start) & (df_movies['runtime'] <= runtime_end)].sort_values('runtime'))



# -- Part 1.3
st.subheader('Part 1.3')
# get stars name
stars = set()
for index, row in df_movies.loc[:, ['star']].iterrows():
        stars.update([name for name in row['star']])

stars_selected = st.multiselect("Select stars name:", sorted(list(stars)), default=['Leonardo DiCaprio', 'Zendaya'])
# filter dataFrame by stars name
st.dataframe(df_movies.loc[df_movies['star'].apply(lambda x: any(item in stars_selected for item in x))])



# -- Part 1.4
st.subheader('Part 1.4')
# get genres
genres = set()
for index, row in df_movies.loc[:, ['genre']].iterrows():
        genres.update([genre for genre in row['genre']])
# input for genre name
genre_selected_p1 = st.selectbox('Select genre', sorted(list(genres)), key='p1.4')
st.write(f'Top 250 imdb movies in **{genre_selected_p1}** genre:')
# filter movies with selected genre
st.dataframe(df_movies.loc[df_movies['genre'].apply(lambda x: any(item == genre_selected_p1 for item in x))])
'-----'



# -- Part 2.1
st.subheader('Part 2.1')
# sort dataFrame by gross_us_canada and get that column
top_guc = df_movies.sort_values('gross_us_canada', ascending=False).set_index('title')['gross_us_canada'][:10]

fig1, ax1 = plt.subplots(figsize=(20, 10), facecolor='white')
ax1.barh(top_guc.index[::-1], top_guc.values[::-1], align='center', color='#1e3d59')
ax1.set_xlabel('Gross US Canada', fontsize=18, weight='bold')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
plt.xticks(rotation=10, fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')

st.write("10 highest grossing films in the United States and Canada:")
st.pyplot(fig1)



# -- Part 2.2
st.subheader('Part 2.2')
# Actor name : Acted Movies Count
stars_presence = {name: 0 for name in stars}
for index, row in df_movies.loc[:, ['star']].iterrows():
        for name in row['star']:
                stars_presence[name] += 1
df_stars_presence = pd.Series(stars_presence).sort_values(ascending=False)[:5]

fig2, ax2 = plt.subplots(figsize=(9, 4), facecolor='white')
ax2.bar(df_stars_presence.index, df_stars_presence.values, align='center', width=0.5, color='#1e3d59')
ax2.set_ylabel('Presence Count', fontsize=18, weight='bold')
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.grid(axis='y', color='#327fa8', linestyle='dashed', linewidth=0.6, alpha=0.5)
plt.xticks(fontsize=10, weight='bold')
plt.yticks(range(0, df_stars_presence[0]+2),fontsize=10, weight='bold')

st.write("5 actors who've appeared in the most movies:")
st.pyplot(fig2)



# -- Part 2.3
st.subheader('Part 2.3')
# Genre : number of movies with this genre  
genres_count = {name: 0 for name in genres}
for index, row in df_movies.loc[:, ['genre']].iterrows():
        for name in row['genre']:
                genres_count[name] += 1
df_genre_count = pd.Series(genres_count).sort_values(ascending=False)
df_genre_count_sum = sum(df_genre_count)

fig3, ax3 = plt.subplots(figsize=(10, 7), facecolor='white')
ax3.pie(df_genre_count.values, wedgeprops ={ 'linewidth': 1.5, 'edgecolor': 'white' }, colors=sns.color_palette('tab20b'))
ax3.set_position([0.1, 0.1, 1.0, 1.0])
plt.legend(
    loc='upper left',
    labels=[f"{gname} {round(gcount / df_genre_count_sum * 100, 2)}%" for gname, gcount in df_genre_count.items()],
    prop={'size': 13, 'weight': 'bold'},
    bbox_to_anchor=(0.0, 1),
    bbox_transform=fig3.transFigure)

st.write("Pie chart for genres:")
st.pyplot(fig3)



# -- Part 2.4
st.subheader('Part 2.4')
# get parental guides 
parental_guides = df_movies['parental_guide'].unique()
# parental_guide : count
parental_guide_count = {pg: 0 for pg in parental_guides}
for index, row in df_movies.loc[:, ['parental_guide']].iterrows():
        parental_guide_count[row['parental_guide']] += 1
df_parental_guide_count = pd.Series(parental_guide_count).sort_values(ascending=False)
parental_guide_count_sum = sum(df_parental_guide_count)

fig4, ax4 = plt.subplots(figsize=(9, 6), facecolor='white')
ax4.pie(df_parental_guide_count.values, wedgeprops ={ 'linewidth': 1.5, 'edgecolor': 'white' }, colors=sns.color_palette('tab20b'))
ax4.set_position([0.1, 0.1, 1.0, 1.0])
plt.legend(
    loc='upper left',
    labels=[f"{pgname} {round(pgcount / parental_guide_count_sum * 100, 2)}%" for pgname, pgcount in df_parental_guide_count.items()],
    prop={'size': 13, 'weight': 'bold'},
    bbox_to_anchor=(0.0, 1),
    bbox_transform=fig4.transFigure)

st.write("Pie chart for parental guide:")
st.pyplot(fig4)



# -- Part 2.5
st.subheader('Part 2.5')
# index=genres columns=parental_guides values=0
pg_gnr_table = pd.DataFrame(data=np.zeros(shape=(len(genres),(len(parental_guides))), dtype=int), index=list(genres), columns=list(parental_guides))
# fill dataFrame
for index, row in df_movies.loc[:, ['genre', 'parental_guide']].iterrows():
        for genre_name in row['genre']:
                pg_gnr_table.loc[genre_name, row['parental_guide']] += 1

st.bar_chart(pg_gnr_table)
'''----'''


# -- Part 3.1
st.subheader('Part 3.1')
# get genre name from user
genre_selected_p3 = st.selectbox('Select genre:', sorted(list(genres)), key='p3.1')
# filter data by selected genre and sort by gross_us_canada
top_guc_bygenre = df_movies.loc[df_movies['genre'].apply(lambda x: any(item == genre_selected_p3 for item in x))].set_index('title')['gross_us_canada'].sort_values(ascending=False)[:10]

fig5, ax5 = plt.subplots(figsize=(20, 10), facecolor='white')
ax5.barh(top_guc_bygenre.index[::-1], top_guc_bygenre.values[::-1], align='center', color= '#476930')
ax5.set_xlabel('Gross US Canada', fontsize=18, weight='bold')
ax5.spines['right'].set_visible(False)
ax5.spines['top'].set_visible(False)
plt.xticks(fontsize=12, weight='bold')
plt.yticks(fontsize=12, weight='bold')

st.write(f"highest grossing films in the United States and Canada (**{genre_selected_p3}** genre):")
st.pyplot(fig5)