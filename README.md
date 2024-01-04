# Recipe Creator Bot Inspired by Ottolenghi
 A Telegram bot that crafts Ottolenghi-inspired recipes from pictures of ingredients sent by users, dynamically adapting the recipe based on subsequent text feedback.

## Features
- **Image Recognition**: Utilizes advanced image processing to identify ingredients in the pictures sent by users.
- **Recipe Generation**: Crafts unique recipes inspired by the flavorful and vibrant style of Ottolenghi, based on the ingredients identified.
- **Interactive Experience**: Engages users in a creative culinary process, offering suggestions for recipe customization.
- **User-friendly Interface**: Seamlessly integrates within the Telegram chat for an intuitive user experience.
- **Personalized Recommendations**: Tailors recipes to user preferences and dietary restrictions, if specified.
- **Educational Aspect**: Provides cooking tips and tricks alongside recipes, encouraging culinary exploration and learning.


## Getting Started

### Prerequisites
- Python 3.x]()
- Telegram account and a Bot Token from BotFather

### Installation and Setup
1. **Clone the Repository**
   - git clone https://github.com/sinatmertens/SummarizerBot
2. **Install Dependencies**
   - cd SummarizerBot
   - pip install -r requirements.txt
3. **Environment Configuration**
   - Create a `.env` file in the project's root directory.
   - Add your Telegram Bot Token: `TELEGRAM_API_KEY=your_api_key_here`.
4. **Run the Bot**
   - python bot.py

## Configuring Your Telegram Bot

### Creating a Bot on Telegram:
1. Use Telegram's BotFather to create a new bot. Send `/newbot` to BotFather and follow the instructions.
2. Once the bot is created, you will receive a bot token.

### Configuring the Bot Token:
1. Replace `your_telegram_bot_token_here` in the `.env` file with the token provided by BotFather.


## Heroku Hosting:
- This bot is hosted on Heroku, a cloud platform that allows easy deployment and scaling. The included `Procfile` is used by Heroku to run the bot.

## Usage
After adding the bot to a Telegram chat, send a picture from your ingredients. The bot will reply with the recipe.

## How to Contribute
We welcome contributions! To contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature.
3. Make your changes and commit them.
4. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgements
A special thanks to the open-source community and all the contributors to this project.

---

For further information or support, feel free to open an issue in this repository.


