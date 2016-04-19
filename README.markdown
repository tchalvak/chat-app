Chat-app in PHP
###############

Acceptance Criteria:
Post short messages, 250 char limit, and see all messages after posting.
Random, but unique usernames.
Track all messages in database for 10 days, but clear any after that.

Extra credit:
Bad words filter to change an array of bad words to be censored.
Applications should have a config file & logging system.
Application should be able to limit connected users.

Install the app on linux!
##############

First off, you'll need a running postgresql, nginx, and python3!
I leave configuring those as an exercise for the user.
You can configure the site http://chat.local by using the nginx conf file at ./conf/chat.local


Configure
###################

Make ./configure runnable, then run it, it just creates the config file.

    sudo chmod ug+x ./configure
    ./configure

Make
#####################

The app will `createdb ca` to create a new database and dump in the blank tables, via `make install` or `make install-db`.  It'll also 

make
make install


Run the app for the api on localhost
##################

make run

Browse to the site
##################

http://chat.local/

INCOMPLETE
#################
Sadly, I didn't get the full chat running, just mainly a basic dummy frunt-end for it.

Still todo:
- Pull chats from api.
- Put/post chats into api.
- Randomized username for api.

You can run the standard

    ./configure
    make
    make install

Above to get the latest version of the code and run a more complete site.


