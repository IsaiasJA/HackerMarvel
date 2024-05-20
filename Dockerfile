FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /hackermar
WORKDIR /hackermar
COPY requirements.txt /hackermar/
RUN pip install -r requirements.txt
COPY . /hackermar/
CMD python manage.py runserver 0.0.0.0:8080
