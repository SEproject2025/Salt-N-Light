#Welcome to Salt & Light

###How to run a local server

Steps 3-5 should only be necessary the first time you do it.
1. Access the repository on VS Code
2. Right click the `app/` folder within our repository and select "open in integrated terminal"
3. Type `pip` to see if it is installed
4. If not follow the install instructions
5. Run the command `pip install -r ./requirements.txt`
6. Run the command `python3 manage.py runserver`

###:sparkles: Githooks setup :sparkles:

Githooks are awesome! They keep the code nice and clean and your QA process short
and sweet. Hooks run before things like commit and push to keep you from forgetting
things that are really easy to forget.

To use them, it's as easy as running `git config core.hooksPath .githooks` after
you've pulled the latest changes of course. :)

Since most everyone in this project is using VSCode, you should be able to do this
in the VSCode git config menu if needed. (Update this if I'm wrong. ;))

Current hooks that exist:

1. a pre-push hook to prevent accidental push to main and lint your code before sending
   off to github
