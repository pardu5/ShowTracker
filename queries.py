database = "entertainmenttracker"

###################################################################################
###  CREATE  ######################################################################
###################################################################################

create_db_query = f"CREATE DATABASE IF NOT EXISTS {database}"

use_db_query = f"use {database}"

create_shows_table_query = """
CREATE TABLE IF NOT EXISTS shows(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) UNIQUE,
    link VARCHAR(100),
    watch_link VARCHAR(255)
)
"""

create_newest_episodes_table_query = """
CREATE TABLE IF NOT EXISTS newest_episodes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    episode VARCHAR(100),
    show_id INT UNIQUE,
    FOREIGN KEY(show_id) REFERENCES shows(id) ON DELETE CASCADE
)
"""

create_users_table_query = """
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY
)
"""

create_userList_table_query = """
CREATE TABLE IF NOT EXISTS userList(
    user_id INT,
    show_id INT,
    watched BOOLEAN,
    FOREIGN KEY(show_id) REFERENCES shows(id),
    PRIMARY KEY(user_id, show_id)
)
"""

###################################################################################
###  SELECT  ######################################################################
###################################################################################

get_shows_titles_query = """
SELECT id, title, watch_link
FROM shows JOIN userList
ON shows.id = userList.show_id
WHERE userList.user_id = %s
ORDER BY title
"""

get_shows_query = """
SELECT *
FROM shows JOIN userList
ON shows.id = userList.show_id
WHERE userList.user_id = %s
ORDER BY title
"""

get_newest_episodes_query = """
SELECT newEp.episode, newEp.show_id
FROM newest_episodes AS newEp JOIN userList
ON newEp.show_id = userList.show_id
WHERE userList.watched = False AND userList.user_id = %s
ORDER BY newEp.episode
"""

get_current_newest_episode_query = """
SELECT episode
FROM newest_episodes
WHERE show_id = %s
"""

###################################################################################
###  INSERT  ######################################################################
###################################################################################

insert_user_query = """
INSERT INTO users (id) VALUES (NULL)
"""

insert_shows_query = """
INSERT IGNORE INTO shows
(title, link, watch_link)
VALUES ( %s, %s, %s)
"""

insert_userList_query = """
INSERT IGNORE INTO userList 
(user_id, show_id, watched)
VALUES ( %s, %s, %s)
"""

insert_newest_episode_query = """
INSERT INTO newest_episodes 
(episode, show_id)
VALUES ( %s, %s)
"""

###################################################################################
###  UPDATE  ######################################################################
###################################################################################

update_newest_episode_query = """
UPDATE newest_episodes
SET episode = %s
WHERE show_id = %s
"""

update_newest_episode_query = """
UPDATE userList
SET watched = True
WHERE show_id = %s
"""

###################################################################################
###  DELETE  ######################################################################
###################################################################################

delete_userlist_query = """
DELETE FROM userList
WHERE show_id = %s
"""

delete_show_query = """
DELETE FROM shows
WHERE id = %s
"""