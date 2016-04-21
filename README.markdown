# Chat-app with REST API


Acceptance Criteria:

- Post short messages, 250 char limit, and see all messages after posting.
- Random, but unique usernames.
- <strike>Track all messages in database for 10 days, but clear any after that.</strike>

Extra credit:

- Bad words filter to change an array of bad words to be censored.
- Applications should have a config file & logging system.
- Application should be able to limit connected users.

## Install the app on linux!

First off, you'll need a running postgresql, nginx, and python3!
I leave configuring those as an exercise for the user.
You can configure the site http://chat.local by using the nginx conf file at ./conf/chat.local


### Configure

Make ./configure executable, then run it, it just creates the `CONFIG` file.

    sudo chmod ug+x ./configure
    ./configure

Modify CONFIG as suits you.

### Make


The app will `createdb ca` to create a new database and dump in the blank tables, via `make install` or `make install-db`.

    make
    make install


## Run the app for the api on localhost

    make run

## Browse to the site

http://chat.local/

## INCOMPLETE

Still TODO:
- Pull chats from an api database
- Put/post chats into api.
- Randomized username for api.

You can run the standard

    ./configure
    make
    make install

Above to get the latest version of the code and run it.


