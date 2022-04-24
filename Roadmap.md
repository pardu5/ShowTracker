# Show Tracker Roadmap (Oldest to Newest)
Multiple iterations of application, starting with MVP and working up to cloud hosted database using application.

*Last Updated 4/21/2022*

## File Based Iteration
Files held show/episode data while BeautifulSoup was used to update data

### File Based Specifics
- [x] Command line window no longer opens on app start
- [x] Threads are used to keep main process for ui interactions
- [x] Can add shows from the UI
- [x] Button next to each show to open link of where you watch it
- [x] File added to hold new episodes to be loaded on app start
- [x] Button added to new episodes to say the user is caught up

## Database Based Iteration
Then local MySQL replaced files with The Movie Database API calls replacing BeautifulSoup

### Database Based Specifics
- [x] Local database is used to save and read data instad of text files
- [x] API requests to get episode info used instead of web scraping with BeautifulSoup
- [x] Delete all new episode elements on scan and re-add elements for alphabetical sorting
- [x] Button to delete a show and the corresponding episode from database 

## AWS Hosted Iteration
Became cloud hosted when endpoint was changed from local to RDS MySQL engine database

### AWS Hosted Specifics
- [x] Create AWS RDS database and have the app use that endpoint
- [x] Make the window resizable, including text expanding and shrinking to fit screen
- [x] Included userids in database for filtering out shows that aren't theirs

## AWS Lambda Middle Man Iteration
Moved private information into AWS Lambdas and out of application for security reasons

### AWS Lambda Specifics
- [x] API gateway -> lambda function instead of directly connecting to database
- [x] Started work towards adding user accounts for MySQL login
- [x] Removal of database username and password, api key for third party and database name from application

## AWS Batch Episode Check Iteration
Having a Batch Job update the entire database on a scheduled basis would reduce the number of requests

### AWS Batch Specifics
- [x] Batch Job that directly connects to the database and checks for new shows created
- [x] AWS EventBridge used to schedule the Batch Job to automatically happen after X time
- [x] Checking for new episodes removed from app, now just pulls latest data from database
- [ ] User login that returns a userid to hold in memory rather in file
- [ ] Help button to explain how to use the app and how it works
- [ ] Edit button for shows to change information
- [ ] Pop up confirmation on deleting a show from list
- [ ] Let user choose the language they want to use
- [ ] Search for new shows in app and add from there

## Non-software Ideas
- [ ] "https://www.ko-fi.com" button to open up donations?
