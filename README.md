# RaidAssignmentBot
A raid assignment discord bot that parses from Google Sheets to MRT format.

To recreate requirements.txt with new imports use ``pip freeze > requirements.txt``.
Run by using ``python bot.py`` in terminal.

## Setup
1. Create Herokuapp application.
2. Add herokuapp secrets to github repo secrets.
3. Add config vars (from .env) to Herokuapp config vars under Settings.

When a commit is pushed to main it will automatically build and deploy to Heroku!