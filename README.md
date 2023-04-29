# Python neptun calendar


## Features

- Neptun API naptár használata
- Óra előtt egy órával jelez ha órád lesz
- Előadásokról az értesítések kikapcsolása
- Mai/Holnapi/következő óráim listázása
- Vizsgáim listázása (Elkövetkezendő 8 nap)


## Tech

Felhasznált keretrendszerek / modulok

- [node.js] - Neptun API backend lekérése
- [python]- Megvalósítás
- [discord.py] - discord api


Neptun API dokumentáció [Atlantisz]
 on GitHub.

## Installation

Python neptun calendar requires [python] v13.9+ to run.

Python neptun calendar module telepítése

```sh
cd python_discord_bot
python setup.py install
```

Szükség lesz egy config file-ra ```config.json``` amiben a megfelelő értékek vannak kitöltve.

Ezután használható a 
```python
import python_discord_bot # module betöltése
python_discord_bot.start_bot() # bot instalálása
```


## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   [python]: <https://www.python.org/>
   [discord.py]: <https://discordpy.readthedocs.io/en/stable/>
   [node.js]: <http://nodejs.org>
   [Atlantisz]: <https://github.com/RuzsaGergely/Atlantisz>

