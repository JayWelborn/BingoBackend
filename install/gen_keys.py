"""gen_keys.py

Generates a set of secret key files. These files are intended to contain
sensitive information (SECRET_KEY, API keys, etc). By default they will all
contain the string "PASSWORD". These should be replaced with real keys before
running the application.
"""

import os
from pathlib import Path


def main():
    base = Path(__file__).resolve().parents[1]
    secrets = os.path.join(base, "bingo", "bingo", "secrets")
    if not (os.path.exists(secrets)):
        os.mkdir(secrets)

    keys = {}

    for filename in ["database.password", "django_secret.key", "email.from",
                     "email.password"]:

        key = filename.replace(".", "_").upper()

        if not os.path.exists(os.path.join(secrets, filename)):
            with open(os.path.join(secrets, filename + "2"), "w") as file:
                file.write("password")
            keys[key] = "password"

        else:
            with open(os.path.join(secrets, filename), "r") as file:
                keys[key] = file.readline()

    with open(os.path.join(base, ".env"), "w") as env_file:
        for key, val in keys.items():
            env_file.write("{}={}\n".format(key, val))


if __name__ == "__main__":
    main()
