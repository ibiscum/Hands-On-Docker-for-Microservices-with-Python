# This Dockerfile is for localdev purposes only, so it won't be
# optimised for size
FROM alpine:latest

# set our environment variable
ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"

# install libintl
# then install dev dependencies for musl-locales
# clone the sources
# build and install musl-locales
# remove sources and compile artifacts
# lastly remove dev dependencies again
RUN apk --no-cache add libintl && \
	apk --no-cache --virtual .locale_build add cmake make musl-dev gcc gettext-dev git && \
	git clone https://gitlab.com/rilian-la-te/musl-locales && \
	cd musl-locales && cmake -DLOCALE_PROFILE=OFF -DCMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install && \
	cd .. && rm -r musl-locales && \
	apk del .locale_build

# Add the proper env variables for init the db
ARG POSTGRES_DB
ENV POSTGRES_DB $POSTGRES_DB
ARG POSTGRES_USER
ENV POSTGRES_USER $POSTGRES_USER
ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD $POSTGRES_PASSWORD
ARG POSTGRES_PORT
ENV LANG en_US.utf8
EXPOSE $POSTGRES_PORT

# For usage in startup, etc
ENV POSTGRES_HOST localhost
ENV DATABASE_ENGINE POSTGRESQL
# Store the data inside the container, as we don't care for
# persistence
RUN mkdir -p /opt/data
ENV PGDATA /opt/data

RUN apk update
RUN apk add bash curl su-exec python3
RUN apk add postgresql-jit postgresql-contrib postgresql-dev postgresql
RUN apk add python3-dev build-base linux-headers gcc libffi-dev

# Create a virtual environment for all the Python dependencies
RUN python3 -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --upgrade pip

# Adding our code
WORKDIR /opt/code

RUN mkdir -p /opt/code/db
# Add postgres setup
ADD ./docker/db/postgres-setup.sh /opt/code/db/
RUN  /opt/code/db/postgres-setup.sh

## Install our code to prepare the DB
ADD ./ThoughtsBackend/requirements.txt /opt/code

RUN pip3 install -r requirements.txt

## Need to import all the code, due dependencies to initialise the DB
ADD ./ThoughtsBackend/ /opt/code/
# Add all DB commanda
ADD ./docker/db/* /opt/code/db/

## get the db ready
RUN /opt/code/db/prepare_db.sh

# Start the database in normal operation
USER postgres
CMD ["postgres"]
