FROM python:3.12-slim

# Install packages
RUN apt update
RUN apt install -y curl wget sudo gcc git

# Add uv for faster dependency management
ENV VIRTUAL_ENV=/home/packages/.venv
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

# Set working directory
WORKDIR /code

COPY ./env/requirements.in /code/env/requirements.in
RUN /root/.cargo/bin/uv venv /home/packages/.venv
RUN /root/.cargo/bin/uv pip compile  /code/env/requirements.in -o /code/env/requirements.txt
RUN /root/.cargo/bin/uv pip install --system --no-cache -r /code/env/requirements.txt

# Copy app directory
COPY ./src/app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]