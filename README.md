Clone the repository:
bash
git clone https://github.com/Syntaxore/flask_test_ecology
cd flask_test_ecology

Set up a virtual environment (optional but recommended):
bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt
Initialize the database:


flask shell
from app import db
db.create_all()
exit()

Run the application:
bash
flask run

Access the application:
Open your web browser and go to http://127.0.0.1:5000.
