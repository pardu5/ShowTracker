import ctypes
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import webbrowser
import os
from threading import Thread
import json
import StringConstants

###################################################################################
###  VARIABLES  ###################################################################
###################################################################################

api_lambda = "https://2e8c9ao6xj.execute-api.us-east-1.amazonaws.com/show-tracker/"

label_holder=[]

has_account = False

user_id = -1
frame_row = 0

error_stringvar = None

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

# Ask the user to sign in or sign up if the config file 
# doesn't have a username and password already set
def userSetUp():
    global user_id
    global has_account
    global error_stringvar
    placeholder = StringConstants.CONFIG_PLACEHOLDER

    with open(StringConstants.CONFIG_PATH, "r") as configFile:
        data = json.load(configFile)
        username = data["username"]
        password = data["password"]
        if not username == placeholder and not password == placeholder:
            params = {"username": username, "password": password}
            response = requests.get(api_lambda+StringConstants.SELECT_USER, params=params)
            user_id = response.json()
            print(f"Username: {username}\nPassword: {password}")
            has_account = True
            return

    top = generatePopUpWindow()

    frame_pop_up_username = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_username, text=StringConstants.LABEL_USERNAME)
    label.pack(side=tk.LEFT)
    entry_username = Entry(frame_pop_up_username, width = 25)
    entry_username.pack(side=tk.LEFT, padx=10)
    frame_pop_up_username.pack(pady=(5, 0))
    entry_username.focus()

    frame_pop_up_password = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_password, text=StringConstants.LABEL_PASSWORD)
    label.pack(side=tk.LEFT)
    entry_password = Entry(frame_pop_up_password, width = 25)
    entry_password.pack(side=tk.LEFT, padx=10)
    frame_pop_up_password.pack(pady=(5, 0))

    frame_pop_up_buttons = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    error_stringvar = tk.StringVar(frame_pop_up_buttons, "")
    lbl_error_text = tk.Label(textvariable=error_stringvar, master=frame_pop_up_buttons)
    lbl_error_text.pack(side=tk.LEFT, anchor="w")
    sign_in_button = Button(frame_pop_up_buttons, text=StringConstants.LABEL_SIGN_IN, 
                    command=lambda:[signUpOrIn("IN", entry_username.get(), entry_password.get(), top)])
    sign_in_button.pack(side=tk.RIGHT, padx=(0, 10))
    sign_up_button = Button(frame_pop_up_buttons, text=StringConstants.LABEL_SIGN_UP, 
                    command=lambda:[signUpOrIn("UP", entry_username.get(), entry_password.get(), top)])
    sign_up_button.pack(side=tk.RIGHT, padx=(0, 10))
    frame_pop_up_buttons.pack(side=tk.RIGHT, pady=(5, 0))

    window.wait_window(top)

def signUpOrIn(choice, username, password, top):
    global user_id
    global has_account

    if username == "" or password == "":
        return

    response = ""
    params = {"username": username, "password": password}
    if choice == "IN":
        response = requests.get(api_lambda+StringConstants.SELECT_USER, params=params)
        text = "Login information is invalid"
    elif choice == "UP":
        response = requests.get(api_lambda+StringConstants.INSERT_USER, params=params)
        text = "Username already exists.\nTry signing in instead?"
    result = response.json()
    if not result == -1:
        user_id = response.json()
        has_account = True
    else:
        error_stringvar.set(text)
        return

    user_info = {"username" : username, "password": password}
    configData = json.dumps(user_info, indent = 4)
    with open(StringConstants.CONFIG_PATH, "w") as configFile:
        configFile.write(configData)
    close_win(top)

# Starts a thread to gather all the shows the user has in their list
def startShows():
    shows = getShows()
    for show in shows:
        addButtonAndLabel(scrollable_frame, show, StringConstants.INTERNET_IMG_PATH, True)

# Look up shows based on user_id from database
def getShows():
    params = {"user_id": user_id}
    response = requests.get(api_lambda+StringConstants.SELECT_TITLES, params=params)
    return response.json()

# Starts a thread to gather all newest episodes that haven't been watched
# by user in their list
def startEpisodes():
    newEpisodes = getNewestEpisodes()
    for episode in newEpisodes:
        addButtonAndLabel(scrollable_frame_episodes_right, episode, StringConstants.EYE_IMG_PATH, False)

def generatePopUpWindow():
    top = Toplevel(window)
    top.grab_set()
    top.focus()
    x = window.winfo_rootx()
    y = window.winfo_rooty()
    geometry = "+%d+%d" % (x+100, y)
    top.geometry(geometry)
    return top

# Create a pop up and provide user with space to add info about show
def addShow(event):
    global has_account
    if not has_account:
        return

    # Create pop up window
    top = generatePopUpWindow()

    frame_pop_up_name = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_name, text=StringConstants.LABEL_SHOW_NAME)
    label.pack(side=tk.LEFT)
    entry = Entry(frame_pop_up_name, width = 25)
    entry.pack(side=tk.LEFT, padx=10)
    frame_pop_up_name.pack(pady=(5, 0))
    entry.focus()

    frame_pop_up_id = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_id, text=StringConstants.LABEL_SHOW_ID)
    label.pack(side=tk.LEFT)
    entry = Entry(frame_pop_up_id, width = 25)
    entry.pack(side=tk.LEFT, padx=10)
    frame_pop_up_id.pack()

    frame_pop_up_url = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_url, text=StringConstants.LABEL_SHOW_URL)
    label.pack(side=tk.LEFT)
    entry = Entry(frame_pop_up_url, width = 25)
    entry.pack(side=tk.LEFT, padx=10)
    frame_pop_up_url.pack()

    ok_button = Button(top, text=StringConstants.LABEL_OK, command=lambda:closeAddShow(top))
    ok_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 10))

def closeAddShow(top):
    children = top.winfo_children()
    name = children[0].winfo_children()[1].get()
    link = children[1].winfo_children()[1].get()
    url = children[2].winfo_children()[1].get()

    if name == "" or link == "":
        return
    close_win(top)

    params = {"name": name, "link": link, "url": url}
    response = requests.get(api_lambda+StringConstants.INSERT_SHOW, params=params)
    show_id = response.json()

    if show_id == 0:
        params = {"show_title": name}
        response = requests.get(api_lambda+StringConstants.SELECT_SHOW, params=params)
        show_id = response.json()[0][0]
        print(f"Show ID: {show_id}")

    params = {"user_id": user_id, "show_id": show_id}
    response = requests.get(api_lambda+StringConstants.INSERT_LIST, params=params)

    data = (show_id, name, url)
    addButtonAndLabel(scrollable_frame, data, StringConstants.INTERNET_IMG_PATH, True)

    t = Thread(target=readdNewElements, args=(scrollable_frame, True))
    t.start()

# Close pop up and add show based on the info provided by user
def close_win(top):
    top.grab_release()
    top.destroy()
    window.update()

# Starts a thread to check all shows and re-add them to the GUI
def startCheckingShows():
    t = Thread(target=checkShows)
    t.start()

# Grab latest user list of shows and check for new episodes for each
def checkShows():
    window_update_stringvar.set(StringConstants.LABEL_CHECKING)
    window.update()

    t = Thread(target=readdNewElements, args=(scrollable_frame_episodes_right, False))
    t.start()

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
    
    IMG_PATH = ""
    if isLeft:
        data = getShows()
        IMG_PATH = StringConstants.INTERNET_IMG_PATH
    else:
        data = getNewestEpisodes()
        IMG_PATH = StringConstants.EYE_IMG_PATH

    for element in data:
        addButtonAndLabel(parent, element, IMG_PATH, isLeft)
    window_update_stringvar.set(StringConstants.LABEL_UPDATED)

# Get list of newest episodes in database
def getNewestEpisodes():
    pathString = "select/episodes"
    params = {"user_id": user_id}
    response = requests.get(api_lambda+StringConstants.SELECT_EPISODES, params=params)
    return response.json()

# Add image button with or without text on a parent frame
def addImageButton(parent, image, text, level, sample):
    img = PhotoImage(file = image)
    subImg = img.subsample(int(sample/ratioWidth), int(sample/ratioHeight))
    if level == "Top":
        button_temp = tk.Button(parent, text=text, image=subImg,compound="right", 
                                borderwidth=5, padx=10, cursor="hand2")
        button_temp.pack(side=tk.RIGHT, padx=5)
    elif level == "Middle":
        button_temp = tk.Button(parent, image=subImg, width=f"{width*0.0175}",
                                height=f"{width*0.0175}", borderwidth=0, cursor="hand2")
        button_temp.pack(side=tk.LEFT, anchor="nw")
    elif level == "Bottom":
        button_temp = tk.Button(parent, text=text, image=subImg, 
                                borderwidth=5, compound="right", padx=10,
                                command=lambda: [startCheckingShows()], cursor="hand2")
        button_temp.pack(side=tk.RIGHT, padx=5)
    label_holder.append(subImg)
    return button_temp

# Add label with corresponding buttons that go with it
#
# For shows:    data = [show_id, show_title, show_url]
# For episodes: data = [episode_text, show_id]
def addButtonAndLabel(parent, data, image, isLeft):
    text = ""
    frame_temp = tk.Frame(master=parent, pady=5)

    button_temp = addImageButton(frame_temp, image, "", "Middle", 20)

    if isLeft:
        text = data[1]
        if data[2] != "":
            args={"url": data[2]}
            button_temp.bind(
                "<Button-1>",
                lambda event, arg=args: openURL(event, arg)
            )
        else:
            button_temp.destroy()

        button_delete = addImageButton(frame_temp, StringConstants.CROSS_IMG_PATH, "", "Middle", 20)
        args={"id": data[0]}
        button_delete.bind(
            "<Button-1>",
            lambda event, arg=args: confirmShowDelete(event, arg)
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

    params = {"show_id": show_id}
    response = requests.get(api_lambda+StringConstants.DELETE_LIST, params=params)

    """params = {"show_id": show_id}
    response = requests.get(api_lambda+StringConstants.DELETE_SHOW, params=params)"""

    event.widget.master.destroy()
    readdNewElements(scrollable_frame_episodes_right, False)

def confirmShowDelete(event, arg):
    top = generatePopUpWindow()

    frame_pop_up_confirm = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    label = tk.Label(frame_pop_up_confirm, text=StringConstants.LABEL_DELETE_CONFIRMATION)
    label.pack(side=tk.LEFT)
    frame_pop_up_confirm.pack(padx=(10, 10))

    frame_pop_up_buttons = tk.Frame(master=top, borderwidth=5)
    # Elements inside frame
    yes_button = Button(frame_pop_up_buttons, text=StringConstants.LABEL_YES, command=lambda:[removeShow(event, arg), close_win(top)])
    yes_button.pack(side=tk.RIGHT, padx=(0, 10))
    cancel_button = Button(frame_pop_up_buttons, text=StringConstants.LABEL_CANCEL, command=lambda:close_win(top))
    cancel_button.pack(side=tk.RIGHT, padx=(0, 10))
    frame_pop_up_buttons.pack(side=tk.RIGHT, pady=(5, 0))

# Set newest episode to watched so it doesn't show up in list anymore
def setEpisodeToWatched(event, arg):
    params = {"show_id": arg["show_id"], "user_id": user_id}
    response = requests.get(api_lambda+StringConstants.UPDATE_WATCHED, params=params)

    event.widget.master.destroy()

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
window.title(StringConstants.APP_TITLE)
window.minsize(int(screensize[0]/2), 450)
guiSetUp(window)
window.update()
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
# Add user_id label
uid_stringvar = tk.StringVar(frame_features_top, StringConstants.LABEL_UID+f"{user_id}")
label_userid = ttk.Label(frame_features_top, textvariable=uid_stringvar, justify="left")
label_userid.pack(side=tk.LEFT, padx=[5,0])
# Add Show button w/ image
button_add_show_top = addImageButton(frame_features_top, StringConstants.PLUS_IMG_PATH, 
                        StringConstants.LABEL_ADD_SHOW, "Top", 10)
button_add_show_top.bind(
    "<Button-1>",
    addShow
)
# Add Ko-fi donation button
button_donation_top = addImageButton(frame_features_top, StringConstants.DONATION_IMG_PATH, "", "Top", 3)
args={"url": StringConstants.DONATION_PAGE}
button_donation_top.bind(
    "<Button-1>",
    lambda event, arg=args: openURL(event, arg)
)
# Add Help button w/ image
button_help_top = addImageButton(frame_features_top, StringConstants.HELP_IMG_PATH, 
                    StringConstants.LABEL_HELP, "Top", 25)
args={"url": StringConstants.APP_HELP_LINK}
button_help_top.bind(
    "<Button-1>",
    lambda event, arg=args: openURL(event, arg)
)
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
ttk.Label(scrollable_frame, text=StringConstants.LABEL_SHOW_LIST, anchor="nw", font='Helvetica 10 bold').pack(anchor="nw")

if has_account:
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
ttk.Label(scrollable_frame_episodes_right, text=StringConstants.LABEL_EPISODES_LIST, anchor="nw", font='Helvetica 10 bold').pack(anchor="w")

if has_account:
    t = Thread(target=startEpisodes)
    t.start()

scrollbar_episodes_right.pack(side="right", fill="y")
canvas_episodes_right.pack(side="right", fill="both", expand=True, padx=(0, 0))
frame_episodes_right.grid(sticky="nsew", row=frame_row, column=1)
frame_row = frame_row + 1

### Frame Bar Bottom elements ###
# Scan show's image
button_bar_bottom = addImageButton(frame_bar_bottom, StringConstants.PLAY_IMG_PATH, 
                        StringConstants.LABEL_SCAN, "Bottom", 18)
window_update_stringvar = tk.StringVar(frame_bar_bottom, "")
lbl_update_text = tk.Label(textvariable=window_update_stringvar, master=frame_bar_bottom)
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