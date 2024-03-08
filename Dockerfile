FROM python:3.9

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements_test.txt 

# Make port 9998 available to the world outside this container
EXPOSE 9998


CMD [ "flask", "run", "--host=0.0.0.0", "--port=9998" ]
