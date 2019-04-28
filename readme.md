# Bingo (Back End)

[![Build Status](https://travis-ci.org/JayWelborn/BingoBackend.svg?branch=master)](https://travis-ci.org/JayWelborn/BingoBackend)
[![codecov](https://codecov.io/gh/JayWelborn/BingoBackend/branch/master/graph/badge.svg)](https://codecov.io/gh/JayWelborn/BingoBackend)


## About

Bingo is an app that allows users to make and plan custom bingo cards. Inspired
by a colleague fighting boredom during mandatory training, custom Bingo cards
are a great way to have fun and get people to pay attention to their
surroundings and interact.

### Packages Used

- [Django](https://www.djangoproject.com/) and
  [DjangoRestFramework](https://www.django-rest-framework.org) for API 
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) and 
  [pip](https://pip.pypa.io/en/stable/) to manage Python dependencies
- [django-rest-auth](https://github.com/Tivix/django-rest-auth) to simplify
  registration via the Rest API
- [django-allauth](https://github.com/pennersr/django-allauth) used to enable
  some extra options. **Social Authentication coming soon**
- [TravisCI](https://travis-ci.com/) for testing on each commit
- [CodeCov](https://codecov.io/) to track test coverage over time

## Requirements

Bingo requires MySQL, Python 3.5+ and virtualenv. The install script assumes you are in
a UNIX environment with Bash installed. If you want to install this project in a
different environment, you will need to install the dependencies manually.

## How to Install

##### Clone the Project

```bash
$ git clone https://github.com/JayWelborn/BingoBackend.git
$ cd Bingo
```

##### Setup Database

Using MySQL, create a database called 'bingo' with password 1234. This password
is used only for installation and can be modified later.

##### Run Installer

```bash
$ ./install.sh
```

The installer should generate a `secrets` folder within the django project
module (the one with settings.py), and generates a set of files to contain
sensitive information. These files are included in the default .gitignore and
should not be included in any public repositories.

After generating needed files, the installer will run the project's test suite
to immediately warn you of any issues.

##### Customize Secrets

At this point, you should change the included secret files from their default
values, and change your database password to match. The file `email.from` is the
email address django will use when sending emails from the `contact` API
endpoint. The email address and password should match an existing gmail account.
See [Sign in using App Passowrds](https://support.google.com/accounts/answer/185833?hl=en)
for instructions in generating a gmail password specifically for your app.

## License

    Copyright (C) 2018 Jay Welborn
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.