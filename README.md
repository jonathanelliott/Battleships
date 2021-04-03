# Battleships
Joint work with Adam Ward for Bristol Python Dojo

## Django Battleships

If you don't have Poetry installed, please follow
[the instructions](https://python-poetry.org/docs/#installation)
on the Poetry site. When you have Poetry installed you can run:

``` bash
poetry install
```

This should then use the pyproject.toml file to install Django.

Once that has completed you can launch a virtual environment with:

``` bash
> poetry shell
```

Then cd into the gameserver directory and run:

``` bash
python manage.py runserver
```

You should now be able to view the default Django page with your browser at 127.0.0.1:8000