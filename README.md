# VidCha Bot
Discord BOT for Youtube Subscription/Notification using Python 3

## Requirement
- Python >= 3.6 (I'm testing on 3.9 but all 3.x should work, 3.6 or later for sure)
- [Discord Application](https://discord.com/developers) (aka. `Bot`)
- [Youtube Data API](https://developers.google.com/youtube/v3/)
- little knowledge about Python, Pip, API, Discord (Also [Thai](https://en.wikipedia.org/wiki/Thai_language) if you want to translate this app, just kidding :smile:)

## Installation
1. `Clone` this project to your PC (aka. `download`)
2. install require libraries using pip from `requirements.txt`
    ```
    > pip install -r requirements.txt
    ```
3. config your Bot using `.env` file. you can use `.env.example` file for reference or just copy paste and rename it to `.env`.
4. migrate your database using `pem`
    ```
    > pem migrate
    ```
5. run your Bot `bot.py`

    ```
    > python bot.py
    ```

## Conclusions
- This bot is now Thai, you can translate it by replacing text in it's code
- This boi is not smooth like criminal. I'm just creating it cause I need to rest from my work for about a few hours.
    It's need a lot of `refactor` to be looking good, I will do it if I have to :P
- This boi is half `OOP` and `FP`, I'm design it to be `OOP` in my head but I just forget it ? I `may` change this Boi to MVC in the future.
- Many lines in this project just fked up with `best practices`. so 1) just reading my code only for understand how it works don't ever think to copy it and 2) Don't do this with your own works or your company's works.

## Screenshots
### Subscribe to youtube channel ###
![subscribe](https://i.imgur.com/rkGIzdf.png)
### Notify when having new videos ###
![new](https://i.imgur.com/JIc6abt.png)
### List subscribed channels ###
![list](https://i.imgur.com/WWcS8rV.png)
### Help commands ###
![help](https://i.imgur.com/nEF2bwk.png)

## References
- [Youtube Data API](https://developers.google.com/youtube/v3)
- [Discord.py](https://discordpy.readthedocs.io/en/stable/)

## License
![We don't do that here](https://i.imgur.com/RUdPyQP.jpg)
