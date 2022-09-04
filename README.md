# gedcom-to-hugo

This is my set of Python scripts designed to read a `gedcom` export and convert it into a set of `.md` files suitable for publication at https://helge.mcfate.family via my "private" https://github.com/SummittDweller/the-Helge-Project.git project.  

Thus far only the `individuals.py` script produces acceptable output as you will see at https://helge.mcfate.family/individuals.  

This is a perpetual work-in-progress.  Check back again for updates, especially during and just after the winter months (when some progress can be exepected).

## GitHub `venv` Guidance

Add `venv` to your `.gitignore` file. Then, you should create `requirements.txt` file and populate it with the packages you have installed. Then, on your production server, create the virtual environment and run `pip install -r requirements.txt`.

Read [this](https://stackoverflow.com/questions/41457612/how-to-use-requirements-txt-to-install-all-dependencies-in-a-python-project/41458329#41458329) to learn more about the requirements file.


