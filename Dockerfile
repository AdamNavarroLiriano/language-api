FROM python:3.12-slim

# Install packages
RUN apt update
RUN apt install -y curl wget sudo gcc git

# Add uv for faster dependency management
ENV VIRTUAL_ENV=/home/packages/.venv
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

# Set working directory
WORKDIR /app

COPY ./env/requirements.in /app/env/requirements.in
RUN /root/.cargo/bin/uv venv /home/packages/.venv
RUN /root/.cargo/bin/uv pip compile  /app/env/requirements.in -o /app/env/requirements.txt
RUN /root/.cargo/bin/uv pip install --system --no-cache -r /app/env/requirements.txt

# Copy app directory
COPY ./app/main.py /app/main.py
COPY ./app/__init__.py /app/__init__.py

# Copy other code directory
COPY ./app/exceptions /app/exceptions
COPY ./app/models /app/models
COPY ./app/routers /app/routers

EXPOSE 80

CMD ["fastapi", "run", "main.py", "--port", "80"]