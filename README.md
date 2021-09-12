# DiffWebChecker

DiffWebChecker is a summer project with the purpose of learning how to interact with files, webs, pdfs, UNIX ... while learning Python.

1º - The user gives a list with the URLs and the app download each website.

2º - The app compares it with the previous version 

3º - If there have been changes, they are highlighted with a color code (red for deleted parts, yellow for modified and green for new text)

4º - 3 pdfs are generated, one with the previous version of the web, other with the last version and a pdf with the 2 versions, side by side, to ease the comparison. 

5º - A message along the pdf is sent through the telegram API to a Telegram bot.


Example:
![alt text](https://github.com/Santixs/DiffWebChecker/blob/master/doc/Example1Readme.png)

To make the telegram integration work, it is necessary to create a token.txt file (with the token) and a chatID.txt file (with the ID of the group what the bot will use to send you the alerts). 

The main.py should be executed from the 'DiffWebChecker' folder.
