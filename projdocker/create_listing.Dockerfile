FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./create_listing.py ./invokes.py ./
CMD [ "python", "./create_listing.py" ]
