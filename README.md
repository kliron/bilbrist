# Bilbrist app

## Prerequisites (python 3)

1. Copy `secrets` folder in bilbrist directory (top level directory).
2. Install python dependencies: `pip install flask Flask-HTTPAuth gunicorn`

## To run with flask built-in webserver (debug mode, do NOT use in production) 
    
    export FLASK_ENV=development
    flask run --cert=secrets/ssl/cert.pem --key=secrets/ssl/key.pem

## To run with production server (gunicorn)

    gunicorn --certfile=secrets/ssl/cert.pem --keyfile=secrets/ssl/key.pem --workers 2 --bind :3000 app:app

## Self-signed SSL certificate security warning

First time you navigate to the app, the browser is going to flash a security error message because the SSL certificate 
is not signed by a known certificate authority.

- In Firefox click on `Advanced` and then click `Accept the risk and continue`.
- In Chrome even if you click `Advanced` you won't see the option to accept and continue. Instead, you
need to type either `thisisunsafe` or `badidea` to continue. You won't see the string printed anywhere, just click on 
  the browser window so that it is in the foreground and just type one of the words.
