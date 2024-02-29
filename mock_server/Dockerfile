FROM python:3.10.8
WORKDIR my_mock_app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
