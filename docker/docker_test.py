import requests
import mysql.connector
from mysql.connector import errorcode
import queries

###################################################################################
###  VARIABLES  ###################################################################
###################################################################################

db_user = "pardus_admin"
db_password = "AvebsWcLaOYGHQr0qDbJ"
db_host = "entertainmenttracker.cgotjtwwrdst.us-east-1.rds.amazonaws.com"
db_name = "entertainmenttracker"
api_key = "90bbc5fa9615baa8ecc1550e7a30dcda"

print("Hello docker world!")

###################################################################################
###  Functions  ###################################################################
###################################################################################

def get_latest_episode_of(show_url_string) -> str:
    url = (
        f"https://api.themoviedb.org/3/tv/{show_url_string}?api_key={api_key}"
    )
    episodeJSON = requests.get(url).json()
    name = episodeJSON["name"]
    latest_episode = episodeJSON["last_episode_to_air"]
    season_number = latest_episode["season_number"]
    episode_number = latest_episode["episode_number"]
    return f"{name}: Season {season_number} Episode {episode_number}"

###################################################################################
###  MAIN  ########################################################################
###################################################################################

try:
    conn = mysql.connector.connect(username=db_user, password=db_password,
                                    host=db_host, database=db_name)
    cursor = conn.cursor()
    cursor.execute(queries.get_all_shows_query)
    shows = cursor.fetchall()
    conn.commit()

    for show in shows:
        resultEpisode = get_latest_episode_of(show[2])

        show_tuple = (show[0],)
        cursor.execute(queries.get_current_newest_episode_query, show_tuple)
        currentEpisode = cursor.fetchall()
        conn.commit()

        if len(currentEpisode) == 0:
            print(f"Adding new episode: {resultEpisode}")
            episode_tuple = (resultEpisode, show[0])
            cursor.execute(queries.insert_newest_episode_query, episode_tuple)
            conn.commit()
        elif currentEpisode[0][0] != resultEpisode:
            print(f"Updating {currentEpisode[0][0]} to {resultEpisode}")
            episode_tuple = (resultEpisode, show[0])
            cursor.execute(queries.update_newest_episode_query, episode_tuple)
            response = cursor.fetchall()
            conn.commit()

            episode_tuple = (show[0],)
            cursor.execute(queries.update_userlist_not_watched_query, episode_tuple)
            response = cursor.fetchall()
            conn.commit()

    conn.commit()
    cursor.close()
except mysql.connector.Error as err:
    print(err)
else:
    conn.close()