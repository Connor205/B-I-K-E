# So What the Actual Fk is Going On

Thats a fantastic question. Lets break down what actually needs to happen and what will be living in which places inside of the repository.

What are the different parts of the project?

- Arduino Code.
  - This code will live and run on an arduino that commands a variety of motors
  - It will be a worker bee for all intensive purposes
  - There may be multiple arduinos to manage various tasks at different points
    - Shuffle
    - Deal
    - Move
- Python Code
  - Main goal of this code is to manage the arduinos
  - It will keep track of where the various decks are located along with the current state of the game
  - It will take commands from some sort of user connected interface
    - Most likely it will host some sort of web server that will be running and processing requests
  - This is the brains of the entire table, it will be dispatching commands to various arduinos and managing all of the serial communication
- Front End
  - This will display the current game state
  - Will probably have some sort of web socket connection to the main python program
  - The web socket will allow some 2 way communication
  - That communication will update the state on the frontend and as such change the rendering
  - This probably needs to be mobile friendly, in that we need to be able to display this on a touchscreen that is not particularly large and located inside the table

Now here is what I am expected to actually happen. We will write the cpp code for the arduino as we are able to and as the motor and physical design is established.
In regards to the python code, there really isn't a ton of lines to write here. Simply we need to understand the flow of the cards and create and manage our classes as such. The hard part will be managing multiple arduinos. But we should be able to port over the code from chess bot. This will allow us to create some unique classes for each individual arduino.

It makes sense to have some sort of overarching table class to manage all of this. This table class will contain the individual arduinos and provide top level methods for our APIs to call when they need to. This probably gets built last. Most of this code is simply hardware descriptive in that we will be changing and altering it as the functionality and physical design of the table itself changes.

What would be incredibly useful is some sort of build script that goes in and builds all of the arduino code uploads it and then starts the python running and the webservers.

## Arduino Sub-Modules
We'll likely need to use different Arduinos for the seperate parts of our hardware system, so it's a good idea to define these systems earlier on. These may change later when hardware starts getting put together but the general split could be:
- Shuffler and relevant input/output apparatus'
- Dealer and relevant input/output apparatus'
- User displays and LED indicators and everything player-viewable
