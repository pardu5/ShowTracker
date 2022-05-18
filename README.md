# Show Tracker

## Project Description
Let users build up a list of shows they want to track. They can get updates on new episodes and house links to places to watch each show. All in all, to reduce the amount of wasted time going to tons of different websites to see if a new episode has come out yet.

## Donation Link
If you want to help out a little bit, head on over to https://ko-fi.com/showtracker!

## How to Install and Run
### Command Line Option:
Run the command in the root directory of this project
```python
py -3 Show_Tracker.py
```
### Pyinstaller Option:
- Install pyinstaller
- Run the command to generate a build and dist directory
```python
pyinstaller Show_Tracker_Dir.spec
```
- Inside dist directory there will be a Show_Tracker.exe that you can run
- Optional: If you would like a console to appear while running the executable, you can change the "console=False" line in the .spec file to "console=True"

## How to Use This Project
Upon running the executable file, you will be shown a sign in screen.
This project uses a seperate database API to get all of the show info. While adding a show, use "https://www.themoviedb.org/" to get a specific id. At this moment, shows are checked for new episodes every 6 hours.
### New User
- Type in a username and password that you want to use
- Click the "Sign Up" button
### Returning User
- Type in the username and password you used previously
- Click the "Sign In" button
### While Signed In
- In the top right corner there is a button that says "Add Show". Click this to open up a popup menu
- Each show has two fields that are required, Title and ID, and one optional field, URL
- Set the title to whatever you want it
- The ID will be the show id given at the third party website after looking it up
```
Ex: Search up Game of Thrones from the website and open up the search result. There is an
id in the url that will be needed, "https://www.themoviedb.org/tv/1399-game-of-thrones".
```
- While adding Game of Thrones in the ui, "1399-game-of-thrones" will be used as the show id
- After adding all the info needed, you should see your show appear on the left under "List of shows:"
- If you click the scan button in the bottom right, it will go look for the latest episode of the show and display it on the right under "List of new episodes:"
- The X button next to the show name will delete the show from your list, the internet globe (if you supplied one) will open the url you provided in a web browser, and the eyeball will set the show as currently up to date. This means that the lastest episode of that show will stop showing up in the episodes list. Until a new episode comes out that is.
