FROM python:3.11-slim

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN pip install mkdocs-material~=9.5

WORKDIR /usr/src/mkdocs

COPY . .
EXPOSE 8080
CMD ["mkdocs", "serve"]