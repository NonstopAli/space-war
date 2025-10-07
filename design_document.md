Design Document — Space war
Overview
Space war is a simple 2D shooting game built using Python and the Pygame library.
The player controls a spaceship that moves horizontally across the bottom of the screen and shoots bullets upward to destroy a fleet of descending aliens.
The goal of the game is to shoot down all the aliens before they reach the bottom of the screen.
Inspiration
This project was inspired by the Alien Invasion project from the book Python Crash Course.
However, I modified and customized many parts of the code, including image assets, structure, and gameplay details, to create my own version called Space war.
Features
Player-controlled spaceship that moves left and right
Ability to shoot bullets upward using the spacebar
Fleet of aliens that move horizontally and descend gradually
Score display that increases when aliens are destroyed
Game over condition when aliens reach the bottom of the screen
Victory message when all aliens are destroyed
Custom images for the ship, bullet, and aliens
Design Decisions
Game Logic: The game uses Pygame’s sprite system to manage bullets, the ship, and alien collisions efficiently.
Scoring: Each alien destroyed increases the score by a fixed amount (10 points).
End Conditions:
The game ends in victory when all aliens are destroyed.
The game ends in defeat when any alien reaches the bottom of the screen.
User Interface: The score and game status messages (like “Game Over” or “You Won”) are displayed on the screen using pygame.font.
Assets: All images used (ship, bullet, and alien) were personally selected and scaled to fit the game’s design.
Technologies Used
Language: Python
Library: Pygame
IDE: Visual Studio Code
Future Improvements
If I continue to develop this project, I plan to:
Add sound effects for shooting and explosions
Introduce multiple levels of increasing difficulty
Add a restart option after the game ends
Create a main menu and pause system