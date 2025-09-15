FROM python:3.9-slim

WORKDIR /app
COPY . /app/

# Run environment setup script
RUN python setup_env.py

RUN apt-get update && apt-get install -y protobuf-compiler

COPY MarketDataFeed.proto /app/
RUN protoc --python_out=. MarketDataFeed.proto

COPY . /app/
RUN pip install protobuf websockets python-dotenv

CMD ["python", "src/main.py"]
