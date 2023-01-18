FROM python:3.7.3-alpine3.9

# update and install dependencies
RUN apk update && apk add --no-cache build-base libffi-dev openssl-dev python3-dev

# Install dependencies
WORKDIR /app
ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# Copy source code
ADD . /app

# Run the fastapi
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3000"]