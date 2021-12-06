# patner SERVICE

## How to start
use `venvpatner/bin/activate` to activate python environment.
install all dependency `pip install -r requirments.txt`
For development container, use `gunicorn --bind 0.0.0.0:8123 app:app -w 2 --threads 16` or `nohup python app.py &` `gunicorn` will not wok on windows
for windows `nohup python app.py &` after activating the venv and instaling from pip

In prod, run the container from the docker image created from the Dockerfile

## Environment Variables
- JWT_SECRET_KEY: For JWT signing and verification



## Requirements
- MYSql credentials in src/config.py.
