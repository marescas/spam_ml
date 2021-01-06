FROM python:3.7
EXPOSE 8000
COPY requirements.txt /opt
RUN pip install -r opt/requirements.txt
COPY . /opt
WORKDIR opt
CMD ["gunicorn", "app:server", "-b", ":8000"]