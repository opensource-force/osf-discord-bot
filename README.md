# OSF Community Discord Bot

A Discord bot designed for the OSF (Open Source Force) community. The bot helps manage projects and gather user preferences efficiently.

## MVP Features
# OSF Community Discord Bot

A Discord bot designed for the OSF (Open Source Force) community. This bot facilitates project management and helps users find suitable projects to contribute to.

## Features

### 1. Project Management

- **Add Project Command**: Allows users to add new projects to the database. Users can provide details such as project name, description, and relevant tags.

### 2. Project Matching

- **Find Projects Command**: Helps users discover projects to contribute to based on their interests and preferences. The bot can match projects with users using predefined tags or AI-based recommendations.

## Getting Started

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/opensource-force/osf-discord-bot.git
   ```
   
2. **Navigate to the Project Directory** 

   ```bash
   cd osf-discord-bot
   ```

3. **create a .env file** 

    create a .env file in the root directory of the project and add your discord bot token:
    
   ```bash
   bot_token=your_discord_bot_token_here
   ```
   
   Note: You need to register for a bot in the Discord Developer Portal.

4. **Install requirements.txt**

    Install the required Python packages using requirements.txt:
    ```bash
    pip install -r requirements.txt
    ```
    
5. **Run the bot**

    Start the bot using the following command():
    ```bash
    python bot.py
    ```
    
    Note: You need to invite the bot to your server. You can do this by going to OAuth in the Discord Developer Portal, generating an OAuth2 URL, and using it to add the bot to your server.


    


