##building stage
FROM python:3 as builder
#ADD app/app.py /
WORKDIR /src/
COPY . /src/
RUN pip install -r requirements.txt

##running stage
EXPOSE 8000
#CMD ["killall python"]
CMD ["python", "app/app.py"]