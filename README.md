# linux-alerter
This was a personal project initially started for fun that just kind of kept growing.

**IMPORTANT: This was written specifically on my Fedora system, thus `journalctl` is an integral part of its functionality.**

## Pre-requisites
* Linux Packages:
    * `fswebcam` for capturing the webcam.
        * Install with your packaging system, i.e.:
        >sudo dnf install fswebcam
        
        >sudo apt-get install fswebcam
* Python Modules:
    * `Python-Decouple` for reading `.env` files.
        >pip install python-decouple
    * `Requests` for sending HTTP requests (POST, GET, PULL, etc.)
        >pip install requests
    * `datetime` for getting unicode timestamps.
        >pip install datetime

* **Setting up `.env` file**
    * Create a file in the repo directory called `.env`. Within that file you want it to read: `WEBHOOK=`, followed by the link to your Discord Webhook.

### The features are as follows:

* `alerter.py` => The primary module for sending POST requests to the Discord Webhook.
* `login-watcher.py` => Script that constantly checks on an interval the amount of failed login attempts since the last check. If the number of failed attempts exceed the threshold then a message is sent detailing the times of the failed attempts, as well as taking a webcam capture and locally storing it.