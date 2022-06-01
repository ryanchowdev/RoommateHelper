# RoommateHelper
A Discord bot that facilitates living with roommates.

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

### Invite the bot to your own Discord server

Simply visit [this URL](https://discord.com/api/oauth2/authorize?client_id=977072357321609257&permissions=532680277056&scope=bot) and you will be prompted to add the bot to your server.

### Usage

Run the following command in your Discord channel to display a general help menu.
```
=help
```

Alternatively, run the following help commands to display a help menu for the specified feature.
* Alarm
```
=help alarm
```
* Calculator
```
=help calculator
```
* Coin Flip
```
=help coinflip
```
* Google Maps/Locations of Interest
```
=help gmaps
```
* Lists
```
=help lists
```
* Money
```
=help money
```
* Polls
```
=help polls
```
* Restrict
```
=help restrict
```
* Rules
```
=help rules
```
* Schedule
```
=help schedule
```
* Weather
```
=help weather
```


## Running your own copy of the bot

### Dependencies

* Python3
* aiosqlite==0.17.0
* discord.py==1.7.3
* python-dotenv==0.20.0
* pytz==2020.5
* urllib3==1.26.3
* youtube_dl==2021.12.17
* [OpenWeatherMap](https://openweathermap.org) API key
* [Discord Bot](https://discord.com/developers/) API key

### Installing

* To install, simply clone the repository and install the dependencies above.
```
git clone https://github.com/ryanchowdev/RoommateHelper.git
cd ./RoommateHelper
pip -r requirements.txt
```
* Then create a *.env* file with your Discord and [OpenWeatherMap](https://openweathermap.org) API keys like so
```
DISCORD_TOKEN=<key>
OPENWEATHER_KEY=<key>
```

### Executing program

* To start the bot, simply run *main.py*
```
python3 main.py
```

## Authors

Ryan Chow

Timothy Ding

Randy Kim

Ferdinand Adell

Justin Leung

## Version History

* 1.0
    * Initial Release

## Known Bugs

See the [Testing](https://github.com/ryanchowdev/RoommateHelper/blob/main/Testing) file for more details.
