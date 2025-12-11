* Setup:

1) Activate the virtual environment:

source setup/venv/bin/activate

If there is not virtual environment, create it:

$ cd setup
$ python3 -m venv venv

After creation, active it:

source venv/bin/activate

Install the libraries (see item )

$ pip3 install -r requirements.txt

* Alternatively, you can install libraries by hand:

$ pip3 install flask
$ pip3 install flask_sqlalchemy
$ pip3 install flask_cors
$ pip3 install pytest

* Maintenance: when necessary, generate new requirements:

pip3 freeze > requirements

2) Now you can run the backend :-)

In folder "src", run:

flask run --debug

3) Call the backend, in the web browser:

localhost:5000