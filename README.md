<h1 align="center" id="title"> E paper weather station
 </h1>
<p align="center"><a href="https://imgur.com/LaVBJ9S"><img src="https://i.imgur.com/LaVBJ9Sl.jpg" title="source: imgur.com" /></a></a><a href="https://imgur.com/Jxe5c2Q"><img src="https://i.imgur.com/Jxe5c2Ql.jpg" title="source: imgur.com" /></a></p>

<h2>💻 The concept:</h2>
The idea behind the project was to realise a simple display that would provide the following information:

- current weather, https://openweathermap.org/api
- calendar with current date,
- weather forecast for the next few days, https://openweathermap.org/api
- current news from Poland, https://newsapi.org/
- my task list from google sheet. Google Cloud
The above data refreshes every 15 minutes. 

<h2>🛠️ Components :</h2>
<p>1. Raspberry Pi zero</p>
<p>2. 7.5inch e-Paper HAT</p>
<p>3. Photo frame</p>

<h2>📚 Modules and libraries:</h2>
<p> </p>
Modules:

- Assistant main.py - main program, configure it to always switch on when the raspberry pi is switched on
- display.py - 
- news.py - module responsible for news
- clear.py - clean the display before refreshing it
- weather.py - module responsible for weather


<h2>🧑‍💻 Usage</h2>
If you want to use this project you will need to set up your own api for weather, news, configure the google cloud data sheet and set the time zone you are in on the Raspberry Pi. You will also need to translate the texts displayed on the screen into your native language.You need to generate your own dash_id, gsheet_keys for your own sheet and insert them in the credentials folder.

