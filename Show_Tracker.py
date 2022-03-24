import ctypes
import tkinter as tk
from tkinter import ttk
from tkinter import *
from mysql.connector import connect, Error
import requests
import webbrowser
import os
from threading import Thread
import json
from os.path import exists as file_exists
import queries
from dotenv import dotenv_values
config = dotenv_values("./config/.env")

###################################################################################
###  VARIABLES  ###################################################################
###################################################################################

path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "")
    )
user = config["SHOW_TRACKER_USER"]
password = config["SHOW_TRACKER_PASSWORD"]
api_key = config["SHOW_TRACKER_API_KEY"]
print(f"USER: {user}\nPASSWORD: {password}\nAPI_KEY: {api_key}")
"""
database = "show_tracker"
host = "localhost"
"""
database = "entertainmenttracker"
host = "entertainmenttracker.cgotjtwwrdst.us-east-1.rds.amazonaws.com"
configPath = path+"\config\config.json"

label_holder=[]

configured = False
connected = False

user_id = -1
frame_row = 0

###################################################################################
###  SET UP  ######################################################################
###################################################################################

ctypes.windll.shcore.SetProcessDpiAwareness(1)
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

###################################################################################
###  Functions  ###################################################################
###################################################################################

# Configures the GUI for window resizing
def guiSetUp(self):
    top=self.winfo_toplevel()

    top.rowconfigure(1, weight=1)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)

    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)

# Adds a new user to the database if they don't have a 
# configure file on app launch
def userSetUp():
    global user_id
    with open(configPath, "r") as configFile:
        data = json.load(configFile)
        user_id = data["user_id"]
        if data["user_id"] > 0:
            print(f"User ID: {user_id}")
            return

    try:
        with connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(queries.insert_user_query)
                user_id = cursor.lastrowid
                connection.commit()
    except Error as e:
        print(f"Error: {e}")

    user_info = {
        "user_id" : user_id,
    }

    configData = json.dumps(user_info, indent = 4)
    with open(configPath, "w") as configFile:
        configFile.write(configData)

# Starts a thread to gather all the shows the user has in their list
def startShows():
    shows = getShows()
    INTERNET_IMG_PATH = path+"\images\internet-globe.png"
    for show in shows:
        addButtonAndLabel(scrollable_frame, show, INTERNET_IMG_PATH, True)

# Look up shows based on user_id from database
def getShows():
    try:
        with connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                userid_tuple = (user_id,)
                cursor.execute(queries.get_shows_titles_query, userid_tuple, multi=True)
                ret = cursor.fetchall()
                connection.commit()
                return ret
    except Error as e:
        print(f"Error: {e}")

# Starts a thread to gather all newest episodes that haven't been watched
# by user in their list
def startEpisodes():
    newEpisodes = getNewestEpisodes()
    EYE_IMG_PATH = path+"\images\eye_ball_circle.png"
    for episode in newEpisodes:
        addButtonAndLabel(scrollable_frame_episodes_right, episode, EYE_IMG_PATH, False)

# Create a pop up and provide user with space to add info about show
def addShow(event):
    # Create pop up window
    top = Toplevel(window)
    top.grab_set()
    parent = event.widget.master
    x = parent.winfo_rootx()
    y = parent.winfo_rooty()
    geometry = "+%d+%d" % (x+100, y)
    top.geometry(geometry)

    frame_pop_up_name = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_name, text="Show Name:")
    label.pack(side=tk.LEFT)
    entry = Entry(frame_pop_up_name, width = 25)
    entry.pack(side=tk.LEFT, padx=10)
    frame_pop_up_name.pack(pady=(5, 0))

    frame_pop_up_id = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_id, text="Show ID:")
    label.pack(side=tk.LEFT)
    entry = Entry(frame_pop_up_id, width = 25)
    entry.pack(side=tk.LEFT, padx=10)
    frame_pop_up_id.pack()

    frame_pop_up_url = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_url, text="Show URL:")
    label.pack(side=tk.LEFT)
    entry = Entry(frame_pop_up_url, width = 25)
    entry.pack(side=tk.LEFT, padx=10)
    frame_pop_up_url.pack()

    ok_button = Button(top, text="OK", command=lambda:close_win(top))
    ok_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 10))

# Close pop up and add show based on the info provided by user
def close_win(top):
    children = top.winfo_children()
    name = children[0].winfo_children()[1].get()
    link = children[1].winfo_children()[1].get()
    url = children[2].winfo_children()[1].get()
    shows_record = (name, link, url)

    try:
        with connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(queries.insert_shows_query, shows_record, multi=True)
                show_id = cursor.lastrowid
                cursor.fetchall()

                userList_tuple = (user_id, show_id, 0)
                cursor.execute(queries.insert_userList_query, userList_tuple, multi=True)
                connection.commit()

                INTERNET_IMG_PATH = path+"\images\internet-globe.png"
                data = (cursor.lastrowid, name, url)
                addButtonAndLabel(scrollable_frame, data, INTERNET_IMG_PATH, True)
    except Error as e:
        print(f"Error: {e}")

    top.grab_release()
    top.destroy()
    readdNewElements(scrollable_frame, True)
    window.update()

# Starts a thread to check all shows and re-add them to the GUI
def startCheckingShows():
    t = Thread(target=checkShows)
    t.start()

    t = Thread(target=readdNewElements, args=(scrollable_frame_episodes_right, False))
    t.start()

# Grab latest user list of shows and check for new episodes for each
def checkShows():
    v.set("Checking...")
    window.update()
    try:
        with connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                show_tuple = (user_id,)
                cursor.execute(queries.get_shows_query, show_tuple, multi=True)
                showsList = cursor.fetchall()
                connection.commit()

            for show in showsList:
                resultEpisode = get_latest_episode_of(show[1], show[2])

                # Grab episode in the database
                with connection.cursor() as cursor:
                    show_tuple = (show[0],)
                    cursor.execute(queries.get_current_newest_episode_query, show_tuple, multi=True)
                    currentEpisode = cursor.fetchall()
                    connection.commit()

                # Handle result episode vs current episode
                changed = True
                episode_tuple = (resultEpisode, show[0])
                if len(currentEpisode) == 0:
                    with connection.cursor() as cursor:
                        cursor.execute(queries.insert_newest_episode_query, episode_tuple, multi=True)
                        connection.commit()
                elif currentEpisode[0][0] != resultEpisode:
                    with connection.cursor() as cursor:
                        episode_tuple = (resultEpisode, show[0])
                        cursor.execute(queries.update_newest_episode_query, episode_tuple, multi=True)
                        connection.commit()
                else:
                    changed = False

                # Newest episode was changed/added for the first time
                if cursor.rowcount != 0 and changed:
                    newEpisode_tuple = (resultEpisode, show[0])
                    CROSS_IMG_PATH = path+"\images\eye_ball_circle.png"
                    addButtonAndLabel(scrollable_frame_episodes_right, newEpisode_tuple, CROSS_IMG_PATH, False)
            v.set("Updated!")
    except Error as e:
        print(f"Error: {e}")

# Send requests to API to gather most recent episode info of show
def get_latest_episode_of(show_name, show_url_string) -> str:
    url = (
        f"https://api.themoviedb.org/3/tv/{show_url_string}?api_key={api_key}"
    )

    response = requests.get(url)
    episodeJSON = response.json()
    name = episodeJSON["name"]
    latest_episode = episodeJSON["last_episode_to_air"]
    season_number = latest_episode["season_number"]
    episode_number = latest_episode["episode_number"]
    return f"{name}: Season {season_number} Episode {episode_number}"

# Destroy children of parent widget then get the newest data for the respective 
# parent widget
def readdNewElements(parent, isLeft):
    textList = []
    for child in parent.winfo_children():
        if child.winfo_class() == "TLabel":
            continue
        grandChildren = child.winfo_children()
        text = grandChildren[1]["text"]
        textList.append(text)
        child.destroy()
    
    if isLeft:
        data = getShows()
        imagePath = "\images\internet-globe.png"
    else:
        data = getNewestEpisodes()
        imagePath = "\images\eye_ball_circle.png"

    EYE_IMG_PATH = path+f"{imagePath}"

    for element in data:
        addButtonAndLabel(parent, element, EYE_IMG_PATH, isLeft)

# Get list of newest episodes in database
def getNewestEpisodes():
    try:
        with connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                userid_tuple = (user_id,)
                cursor.execute(queries.get_newest_episodes_query, userid_tuple, multi=True)
                episodes = cursor.fetchall()
                connection.commit()
                return episodes
    except Error as e:
        print(f"Error: {e}")

# Add label with corresponding buttons that go with it
def addButtonAndLabel(parent, data, image, isLeft):
    textLength = 0
    text = ""
    frame_temp = tk.Frame(master=parent, pady=5)

    img = PhotoImage(file = image)
    subImg = img.subsample(int(20/ratioWidth), int(20/ratioHeight))
    label_holder.append(subImg)
    button_temp = tk.Button(frame_temp, image=subImg, width=f"{width*0.0175}",
                            height=f"{width*0.0175}", borderwidth=0)
    button_temp.pack(side=tk.LEFT, anchor="nw")

    if isLeft:
        textLength = parent.master.winfo_width()*0.9
        text = data[1]
        if data[2] != "":
            args={"url": data[2]}
            button_temp.bind(
                "<Button-1>",
                lambda event, arg=args: openURL(event, arg)
            )
        else:
            button_temp.destroy()

        CROSS_IMG_PATH = path+"\images\cross_red_circle.png"
        img = PhotoImage(file = CROSS_IMG_PATH)
        subImg = img.subsample(int(20/ratioWidth), int(20/ratioHeight))
        label_holder.append(subImg)

        button_delete = tk.Button(frame_temp, image=subImg, width=f"{width*0.0175}", 
                                    height=f"{width*0.0175}", borderwidth=0)
        button_delete.pack(side=tk.LEFT, anchor="nw")
        args={"id": data[0]}
        button_delete.bind(
            "<Button-1>",
            lambda event, arg=args: removeShow(event, arg)
        )
    elif not isLeft:
        text = data[0]
        args={"show_id": data[1]}
        button_temp.bind(
            "<Button-1>",
            lambda event, arg=args: setEpisodeToWatched(event, arg)
        )

    label_temp = ttk.Label(frame_temp, text=text, justify="left")
    label_temp.pack(fill=tk.X, expand=True)
    frame_temp.pack(fill=tk.X, expand=True)

# GUI root event when the screen is resized. Changes the text wrap length to fit
# inside the screen
def wrapLengthChange(event, data):
    width = window.winfo_width()
    if width == 1:
        return
    leftListFrame = data["parent1"]
    rightListFrame = data["parent2"]
    wrapSize = int(width/2)-100

    childrenLeft = leftListFrame.winfo_children()
    childrenRight = rightListFrame.winfo_children()
    numChildrenLeft = len(childrenLeft)
    numChildrenRight = len(childrenRight)

    if numChildrenLeft == 0 or numChildrenRight == 0:
        return

    for child in childrenLeft:
        grandChildren = child.winfo_children()
        numGrandChildren = len(grandChildren)
        if numGrandChildren > 0:
            label = grandChildren[numGrandChildren - 1]
            if label.winfo_class() == "TLabel":
                label.config(wraplength=wrapSize)

    for child in childrenRight:
        grandChildren = child.winfo_children()
        numGrandChildren = len(grandChildren)
        if numGrandChildren > 0:
            label = grandChildren[numGrandChildren - 1]
            if label.winfo_class() == "TLabel":
                label.config(wraplength=wrapSize)

# URL button event to open URL given by the user
def openURL(event, arg):
    url = arg["url"]
    if url != "":
        webbrowser.open(url, new=2)

# Remove a show from database that the user no longer wants
def removeShow(event, arg):
    show_id = arg["id"]

    try:
        with connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                show=(show_id,)
                cursor.execute(queries.delete_userlist_query, show)
                cursor.execute(queries.delete_show_query, show)
                connection.commit()
                if cursor.rowcount > 0:
                    event.widget.master.destroy()
                    readdNewElements(scrollable_frame_episodes_right, False)
    except Error as e:
        print(f"Error: {e}")

# Set newest episode to watched so it doesn't show up in list anymore
def setEpisodeToWatched(event, arg):
    try:
        with connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                episode = (arg["show_id"],)
                cursor.execute(queries.update_newest_episode_query, episode, multi=True)
                if cursor.rowcount > 0:
                    event.widget.master.destroy()
                connection.commit()
    except Error as e:
        print(f"Error: {e}")

###################################################################################
###  DATABASE SET UP  #############################################################
###################################################################################

def databaseSetUp():
    try:
        with connect(
            host=host,
            user=user,
            password=password,
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                print("Checking on database and tables...")
                db = (database,)
                cursor.execute(queries.create_db_query)
                cursor.execute(queries.use_db_query)
                connection.commit()

                cursor.execute(queries.create_shows_table_query)
                print("Shows tables created successfully")
                cursor.execute(queries.create_newest_episodes_table_query)
                print("Episodes tables created successfully")
                cursor.execute(queries.create_users_table_query)
                print("Users tables created successfully")
                cursor.execute(queries.create_userList_table_query)
                print("User list tables created successfully")
                connection.commit()
            return True
    except Error as e:
        print(f"Set Up Error: \n\t{e}")
        return False

###################################################################################
###  GUI  #########################################################################
###################################################################################

print(f"Resolution: {screensize}") # 3840x2160 tested on
width = int(screensize[0]*0.75)
height = int(screensize[1]/2)
ratioWidth = screensize[0] / 3840
ratioHeight = screensize[1] / 2160

window = tk.Tk()
window.geometry(f"{width}x{height}")
window.title("Show Tracker")
window.minsize(int(screensize[0]/2), 450)
guiSetUp(window)
connected = databaseSetUp()

if connected:
    userSetUp()

window.rowconfigure(0, minsize=75)
window.rowconfigure(1, minsize=300)
window.rowconfigure(2, minsize=75)

### Frames Set Up ###
frame_features_top = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=5)
frame_shows_left = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=5)
frame_episodes_right = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=5)
frame_bar_bottom = tk.Frame(master=window, relief=tk.RIDGE, borderwidth=5)

### Frame Features Top elements ###
# Add Show button's image
PLUS_IMG_PATH = path+"\images\\blue_plus_circle.png"
image = PhotoImage(file = PLUS_IMG_PATH)
subImg = image.subsample(int(10/ratioWidth), int(10/ratioHeight))
label_holder.append(subImg)
# Add Show button
button_features_top = tk.Button(frame_features_top, image=subImg, width=f"{width*0.015}", 
                                height=f"{width*0.015}", borderwidth=0)
button_features_top.pack(side=tk.RIGHT)
button_features_top.bind(
    "<Button-1>",
    addShow
)
lbl_list = tk.Label(text="Add show", master=frame_features_top)
lbl_list.pack(side=tk.RIGHT)
frame_features_top.grid(sticky="nsew", row=frame_row, column=0, columnspan=2)
frame_row = frame_row + 1

### Frame Shows Left elements ###
canvas_shows_left = tk.Canvas(frame_shows_left)
scrollbar = ttk.Scrollbar(frame_shows_left, orient="vertical", command=canvas_shows_left.yview)
scrollable_frame = ttk.Frame(canvas_shows_left)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_shows_left.configure(
        scrollregion=canvas_shows_left.bbox("all")
    )
)
canvas_shows_left.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_shows_left.configure(yscrollcommand=scrollbar.set)
ttk.Label(scrollable_frame, text="List of shows:", anchor="nw", font='Helvetica 10 bold').pack(anchor="nw")

if connected:
    t = Thread(target=startShows)
    t.start()

scrollbar.pack(side="right", fill="y")
canvas_shows_left.pack(side="left", fill="both", expand=True, padx=(0, 0))
frame_shows_left.grid(sticky="nsew", row=frame_row, column=0)

### Frame Episodes Right elements ###
canvas_episodes_right = tk.Canvas(frame_episodes_right)
scrollbar_episodes_right = ttk.Scrollbar(frame_episodes_right, orient="vertical", command=canvas_episodes_right.yview)
scrollable_frame_episodes_right = ttk.Frame(canvas_episodes_right)
scrollable_frame_episodes_right.bind(
    "<Configure>",
    lambda e: canvas_episodes_right.configure(
        scrollregion=canvas_episodes_right.bbox("all")
    )
)
canvas_episodes_right.create_window((0, 0), window=scrollable_frame_episodes_right, anchor="nw")
canvas_episodes_right.configure(yscrollcommand=scrollbar_episodes_right.set)
ttk.Label(scrollable_frame_episodes_right, text="List of new episodes:", anchor="nw", font='Helvetica 10 bold').pack(anchor="w")

if connected:
    t = Thread(target=startEpisodes)
    t.start()

scrollbar_episodes_right.pack(side="right", fill="y")
canvas_episodes_right.pack(side="right", fill="both", expand=True, padx=(0, 0))
frame_episodes_right.grid(sticky="nsew", row=frame_row, column=1)
frame_row = frame_row + 1

### Frame Bar Bottom elements ###
PLAY_IMG_PATH = path+"\images\green_play_button.png"
image = PhotoImage(file = PLAY_IMG_PATH)
subImg = image.subsample(int(18/ratioWidth), int(18/ratioHeight))
label_holder.append(subImg)
button_bar_bottom = tk.Button(frame_bar_bottom, image=subImg, width=f"{width*0.015}", 
                                height=f"{width*0.015}", borderwidth=0, compound=RIGHT,
    command=lambda: [startCheckingShows()])
button_bar_bottom.pack(side=tk.RIGHT)
lbl_list = tk.Label(text="Scan", master=frame_bar_bottom)
lbl_list.pack(side=tk.RIGHT)
v = tk.StringVar(frame_bar_bottom, "")
lbl_update_text = tk.Label(textvariable=v, master=frame_bar_bottom)
lbl_update_text.pack(side=tk.LEFT, anchor="w")
frame_bar_bottom.grid(sticky="nsew", row=frame_row, column=0, columnspan=2)

args={"parent1": scrollable_frame, "parent2": scrollable_frame_episodes_right}
window.bind(
    '<Configure>', 
    lambda event, arg=args: wrapLengthChange(event, arg)
)

window.mainloop()

###################################################################################
##  END  ##########################################################################
###################################################################################