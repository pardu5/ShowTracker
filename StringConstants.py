import os

### Config ###
path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
CONFIG_PATH = path+"\config\config.json"
CONFIG_PLACEHOLDER = "__placeholder__"
APP_TITLE = "Show Tracker"
APP_HELP_LINK = "https://github.com/caseyshaley/ShowTracker#how-to-use-this-project"
DONATION_PAGE = "https://ko-fi.com/showtracker"

### Lambda ###
LAMBDA_ENDPOINT = "https://2e8c9ao6xj.execute-api.us-east-1.amazonaws.com/show-tracker/"
DATABASE_SETUP = "database/setup"
DELETE_LIST = "delete/list"
DELETE_SHOW = "delete/show"
INSERT_LIST = "insert/list"
INSERT_SHOW = "insert/show"
INSERT_USER = "insert/user"
SELECT_EPISODES = "select/episodes"
SELECT_SHOW = "select/show"
SELECT_TITLES = "select/titles"
SELECT_USER = "select/user"
UPDATE_WATCHED = "update/watched"

### Images ###
CROSS_IMG_PATH = path+"\images\cross_red_circle.png"
DONATION_IMG_PATH = path+"\images\kofi_button_blue.png"
EYE_IMG_PATH = path+"\images\eye_ball_circle.png"
HELP_IMG_PATH = path+"\images\\question_mark_circle.png"
INTERNET_IMG_PATH = path+"\images\internet-globe.png"
PLAY_IMG_PATH = path+"\images\green_play_button.png"
PLUS_IMG_PATH = path+"\images\\blue_plus_circle.png"

### UI Labels
LABEL_ADD_SHOW = "Add Show"
LABEL_CANCEL = "Cancel"
LABEL_CHECKING = "Checking..."
LABEL_DELETE_CONFIRMATION = "Are you sure you want to delete this show?"
LABEL_EPISODES_LIST = "List of episodes:"
LABEL_HELP = "Help"
LABEL_OK = "OK"
LABEL_PASSWORD = "Password:"
LABEL_SIGN_IN = "Sign In"
LABEL_SIGN_UP = "Sign Up"
LABEL_SCAN = "Scan"
LABEL_SHOW_ID = "Show ID:"
LABEL_SHOW_LIST = "List of shows:"
LABEL_SHOW_NAME = "Show Name:"
LABEL_SHOW_URL = "Show URL:"
LABEL_UID = "User ID: "
LABEL_UPDATED = "Updated!"
LABEL_USERNAME = "User Name:"
LABEL_YES = "Yes"