<img align=centre src="https://github.com/Terminal127/discord_bot/blob/main/img/logo-no-background.png" alt=bot width=700 height=400>

This bot would be your own personal Ai on Discord, ready to answer your questions, generate Information from pictures and encouragements. Imagine being able to ask the bot for a poem about a dragon, a code snippet for a game, or the latest news in Spanish, all within the same server. It would be like having your own pocket encyclopedia and language tutor!


## Deployment

To deploy this project run
Remember it is advisible to use virtual environment for this use.

```bash
  git clone https://github.com/Terminal127/discord_bot
  cd discord_bot
  pip install -r requirements.txt
  python3 main.py
```


## API Reference

#### Get all items

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`TOKEN`

you can add your api key here but i didn't chose to add.

`API_KEY`


## Features

- images infomation
- answer to questions
- anime information


## Usage/Examples

```python
load_dotenv()

TOKEN = os.environ.get('TOKEN') 

# Set your bot token here
# you can also add your api token here
```


#
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

