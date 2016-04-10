#Full Stack Nanodegree Project 4 Refresh

This application implements a simple backend for a Tic-Tac-Toe game using
Google Cloud Endpoints, App Engine, and Python.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions

1. Make sure to have the [App Engine SDK for Python][4] installed, version
   1.7.5 or higher.
2. Update the value of `application` in `app.yaml` to the respective Project ID(s) 
   you have registered in the [APIs Console][5].
3. Run the application, and ensure it's running by visiting your local server's
   admin console (by default [localhost:8080/_ah/admin][6].)
4. Test your Endpoints by visiting the Google APIs Explorer: 
  [localhost:8080/_ah/api/explorer][7]
5. (Optional) Generate your client library(ies) with the endpoints tool. 
    Deploy your application.

##Game Description:

Tic-Tac-Toe is a simple two player game. Game instructions are available
[here](https://en.wikipedia.org/wiki/Tic-tac-toe).

The board is represented as a list of squares with indexes as follows:
  
    [0, 1, 2  
     3, 4, 5  
     6, 7, 8]

The above representation, is an example of a 3x3 board.

###How To Play Using API endpoints

1.  Players start by creating a "user_name" and providing a valid "email" through 
    which a reminder will be sent to them.
2.  A new game is created with a "board size", and each player assigns their registered 
    user_name to the value of player_x and player_o respectively. Once a new game is created, 
    a game key `urlsafer_key` is created. Make sure you copy it down. It will be needed subsequently 
    to retrieve game and user data.
3.  Players uses this game key to "make a move" of "X" or "O". And that move is stored 
    as that player's move. if a player uses "X", the other player uses "O".
4.  The player that started the game can decide to "cancel the game". in which case, 
    the game key will be deleted.
5.  If game is not cancelled, using the game key, the "current game state" can be known. 
    This will show the move each player has made, and whose turn it is.
6.  After the game has ended in a win, draw or loss, using the game key, 
    the number of finished games, no. of user games, user scores and game history can be retrieved.

##Game example:

In the example we have following situation on the board:
  
    | X | O | X  
    | O | X |  
    | O |   |

Next move is on player_x which let's say name is George. He can make move to
positions with following indexes: 5, 7, 8. By making his move on index 8 he
will win the game. So calling "makeMove" endpoint with "user_name": George and
"move": 8, will result in winning him the game.

##Files Included:

 - tictactoe_api.py: Contains the api endpoints and game playing logic.
 - app.yaml:    App configuration.
 - cron.yaml:   Cronjob configuration.
 - main.py:     Handler for taskqueue handler.
 - models.py:   Entity definitions including helper methods.
 - forms.py:    Message definitions including helper methods.
 - utils.py:    Helper function for retrieving ndb.Models by urlsafe Key string.

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
    - Parameters: boardSize, player_x, player_o
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. player_x and player_o provided must correspond to an
    existing user - will raise a NotFoundException if not. boardSize must not be less than 3.
 
 - **cancel_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: DELETE
    - Parameters: urlsafe_game_key
    - Returns: Message confirming that game has been deleted.
    - Description: Cancels a game while game is in progess. player_x and player_o must provide 
    the game key to be deleted.
         
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
    
 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, move, user_name
    - Returns: GameForm with new game state.
    - Description: Accepts a 'move' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created.
   
 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).
    
 - **get_user_scores**  
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name, email (optional)
    - Returns: ScoreForms. 
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.
    
 - **get_user_games**
    - Path: 'user/games'
    - Method: GET
    - Parameters: user_name, email
    - Returns: GameForms.
    - Description: Gets the average number of attempts remaining for all games
    from a previously cached memcache key.
    
 - **get_finished_games**
    - Path: 'games/finished_games'
    - Method: GET
    - Parameters: None
    - Returns: StringMessage.
    - Description: Gets the average number of attempts remaining for all games
    from a previously cached memcache key.
    
 - **get_user_rankings**
    - Path: 'user/ranking'
    - Method: GET
    - Parameters: None
    - Returns: UserForms.
    - Description: Gets the ranking performance of each player.
      
 - **get_games_history**
    - Path: 'game/{urlsafe_game_key}/history'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: StringMessage.
    - Description: Gets the game history of each player.  

##Models Included:
 
 - **User**
    - Stores unique user_name and (optional) email address.
    
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.
    
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.
    
##Forms Included:
 
 - **UserForm**
    - Representation of a User's state.
 - **GameForm**
    - Representation of a Game's state. 
 - **NewGameForm**
    - Used to create a new game. 
 - **MakeMoveForm**
    - Inbound make move form.
 - **ScoreForm**
    - Representation of a completed game's Score.
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **StringMessage**
    - General purpose String container.
    
    
[1]: https://developers.google.com/appengine
[2]: http://python.org/
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://developers.google.com/appengine/downloads
[5]: https://code.google.com/apis/console
[6]: http://localhost:8080/_ah/admin
[7]: http://localhost:8080/_ah/api/explorer
