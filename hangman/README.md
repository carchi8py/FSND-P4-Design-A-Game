#Full Stack Nanodegree Project 4: Hangman Api

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
1.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
1.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.
 
 
 
##Game Description:
Hagman is a word guessing game, where you guess a letter and your told if it 
is in the word or not. Each right guess results in a letter of the word being
revealed. Every wrong guess results in a turn being taken away. You keep
guessing until the word is fully shown and you win, or you run out of turns 
and your lose

## Score:
Two different score are keeps for this game.
1. Win and Losses. The first is the number of wins and losses you've had. A win is any time you complete a hangman game with out running out of guessess. A loss is any time you run out of guessess before completeing the game. Use the get_user_rankings to get the players with the most wins
1. Number of guesses: The second score is the number of guesses left when you finish the game. If you had 1 guess left you'll have a 1. if you had all 5 guess left you'll have a 5. The idea for this score is to show player who needed the least ammount of guesses to solve the word. You can use the get_high_scores to return this

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, target (optional), attemps (optional)
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Target is
    optional, if you don't provided it a random word will be used. Attemps 
    is the number of guess you have to guess the word.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new game state.
    - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.
     
 - **get_user_game**
    - Path: 'games/user/{urlsafe_game_key}'
    - Method: GET
    - Parameters: user_name
    - Returns: GameForms with the user's current games.
    - Description: Returns all of an individual User's active games.

- **cancel_game**
    - Path: 'games/{urlsafe_game_key}'
    - Method: POST
    - Parameters: urlsafe_game_key
    - Returns: Messages confirming deletion of the game.
    - Description: Cancel an unfished game.

- **get_high_scores**
    - Path: 'scores/high'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms
    - Description: Returns all winning Scores ascending ordered by the attempts used.

- **get_user_rankings**
    - Path: 'ranking'
    - Method: GET
    - Parameters: None
    - Returns: UserForms
    - Description: Returns a list of user by most wins.

- **get_game_history**
    - Path: 'game/history/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: MoveHistoryForm
    - Description: Returns all game moves.
    

##Models Included:
 - **User**
    - Stores unique user_name, (optional) email address, the number of winns, and losses.
    
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.
    
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.
    
##Forms Included:
- **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name, revealed_word, moves).
- **GameForms**
    - Multiple ScoreForm container.
- **NewGameForm**
    - Used to create a new game (user_name, target, attempts)
- **MakeMoveForm**
    - Inbound make move form (guess).
- **ScoreForm**
    - Representation of a completed game's Score (user_name, date, won flag,
    guesses).
- **ScoreForms**
    - Multiple ScoreForm container.
- **UserForm**
    - Representation of a user's performance (user_name, performance).
- **UserForms**
    - Multiple UserForm container.
- **MoveHistoryForm**
    - MoveHistoryForm for outbound a completed game's moves history.
- **StringMessage**
    - General purpose String container.

##Example of how to test
- Call Hangman.create_user and create a user
```json
{
 "message": "User user created"
}
```
- Call hangman.new_game and give your username
```json
{
 "attempts_remaining": "5",
 "game_over": false,
 "message": "Good Luck",
 "revealed_word": "***********",
 "urlsafe_key": "agtkZXZ-aGFuZ21hbnIRCxIER2FtZRiAgICAgPiFCQw",
 "user_name": "user"
}
```
- Call hangman.make_move give urlsafe_key and pick a letter
```json
{
 "attempts_remaining": "5",
 "game_over": false,
 "message": "Hit",
 "moves": [
  "Guess: 'a', Result: '*********a*'"
 ],
 "revealed_word": "*********a*",
 "urlsafe_key": "agtkZXZ-aGFuZ21hbnIRCxIER2FtZRiAgICAgPiFCQw",
 "user_name": "user"
}
```
```json
{
 "attempts_remaining": "4",
 "game_over": false,
 "message": "Miss",
 "moves": [
  "Guess: 'a', Result: '*********a*'",
  "Guess: 'z', Result: '*********a*'"
 ],
 "revealed_word": "*********a*",
 "urlsafe_key": "agtkZXZ-aGFuZ21hbnIRCxIER2FtZRiAgICAgPiFCQw",
 "user_name": "user"
}
```
- Call hangman.get_game and give the urlsafe_key
```json
{
 "moves": [
  "Guess: 'a', Result: '*********a*'",
  "Guess: 'z', Result: '*********a*'"
 ]
}
```
- Call hangman.get_user_rankings to see the who has the most wins
{
```json
 "items": [
  {
   "loses": "0",
   "user_name": "carchi8py",
   "wins": "1"
  },
  {
   "loses": "0",
   "user_name": "bob",
   "wins": "1"
  }
 ]
}
```
- Call Hangman.get_high_scores to see who has the least ammount of guesses to win
```json
{
 "items": [
  {
   "date": "2016-07-06",
   "guesses": "0",
   "user_name": "bob",
   "won": true
  },
  {
   "date": "2016-07-04",
   "guesses": "48",
   "user_name": "carchi8py",
   "won": true
  }
 ]
}
```
 