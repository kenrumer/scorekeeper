# Scorekeeper

This project is designed to enable tournament scoring for golf.  The structure of tournament->rounds->scorecards retains each players score per hole and will present an individual view.
The structure of courses->tees->holes retains each courses slope and determines handicaps

## Getting Started

Currently the documentation is hosted at http://kenrumer.pythonanywhere.com/golf/docs/ (pythonanywhere). For development we are using c9.io (cloud9). For source code repository we are using github.com/kenrumer/scorekeeper.git.
This application is written in python and run on the Django framework. You can start locally by installing git for windows or whatever your OS.  We chose to use cloud9 because there is a chromebook extension.

### Prerequisites

If you want to run this locally, you need to install the following:
Install latest python 3.6.2 64 bit
pip install django
pip install reportlab
pip install django-mathfilters
pip install --upgrade setuptools
pip install weasyprint

If running on windows:
must follow 'http://weasyprint.readthedocs.io/en/stable/install.html#windows' (no need to restart, though)
used gtk3 64 bit
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
used 'Build Tools for Visual Studio 2017' w/ windows 10 SDK ends up about 5gb (wow)
https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2017
open x86 Native Tools Command Prompt for Visual Studio 2017
pip install weasyprint
start new cmd prompt

Now start the server
cd to scorekeeper directory
python manage.py runserver
http://localhost:8000/golf/

## Running the tests

Haven't even started with Test Driven Development.  This should have been defined at the start, but is now an afterthought

### Break down into end to end tests

Not yet

### And coding style tests

Code style so far:
When possible use camelCase
single quote strings in js, css and python
double quote strings in html
2 space tabs for html and javascript
4 space tabs for python


## Deployment

In the cloud9 workspace there is a simple script that will commit to github called cgh.
It takes an optional parameter of 'message' which will override the default 'commit from cloud9'.  Use this if there is valuable commit messaging required.
In the pythonanywhere console, use the pull github script pgh to get the latest from github.  This may require web app reload from https://www.pythonanywhere.com/user/kenrumer/webapps/#tab_id_kenrumer_pythonanywhere_com


## Built With

* [Dropwizard](https://www.djangoproject.com/) - Django

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Ken Rumer** - *Initial work*

See also the list of [contributors](https://github.com/kenrumer/scorekeeper/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

