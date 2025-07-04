# formanting linter 
ruff format

# check 
ruff check . --fix

# run tests
pytest

# run server uvicorn
uvicorn app.main:app --host 192.168.1.7 --port 8000 --reload