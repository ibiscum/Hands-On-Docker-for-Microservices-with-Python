# ----------------------------------------
# This image will compile the dependencies
# It will install compilers and other packages, 
# that won't be carried over to the runtime image
# ----------------------------------------
FROM alpine:latest AS compile-image

# Add requirements for python and pip
RUN apk add --update python3

RUN mkdir -p /opt/code
WORKDIR /opt/code

# Install dependencies
RUN apk add python3-dev build-base gcc linux-headers postgresql-dev libffi-dev

# Create a virtual environment for all the Python dependencies
RUN python3 -m venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --upgrade pip

# Install and compile uwsgi
# RUN pip3 install uwsgi==2.0.18
RUN pip3 install uwsgi

# Install other dependencies
COPY ThoughtsBackend/requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt

# ----------------------------------------
# This image is the runtime, will copy the 
# dependencies from the other
# ----------------------------------------
FROM alpine:latest AS runtime-image

# Install python
RUN apk add --no-cache --update python3 curl libffi postgresql-libs sqlite

# Copy uWSGI configuration
RUN mkdir -p /opt/uwsgi
ADD docker/app/uwsgi.ini /opt/uwsgi/
ADD docker/app/start_server.sh /opt/uwsgi/

# Create a user to run the service
RUN addgroup -S uwsgi
RUN adduser -H -D -S uwsgi

# Copy the venv with compile dependencies from the compile-image
COPY --chown=uwsgi:uwsgi --from=compile-image /opt/venv /opt/venv

# Be sure to activate the venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the code
COPY --chown=uwsgi:uwsgi ThoughtsBackend/ /opt/code/

# Run parameters
RUN chown -R uwsgi:uwsgi /opt/uwsgi
WORKDIR /opt/code
RUN rm -f db.sqlite3; python init_db.py; chown uwsgi:uwsgi db.sqlite3
EXPOSE 8000
USER uwsgi

CMD ["/bin/sh", "/opt/uwsgi/start_server.sh"]
