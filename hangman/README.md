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