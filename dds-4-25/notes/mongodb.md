<link rel='stylesheet' href='markdown9.css'/>

MongoDB
-------

Configured to bind only to 127.0.0.1, disabling external access

Therefore, no credentials. MongoDB also does not store user data.

Uploaded initial database using `scripts/update_census.py`

Added the following to /etc/cron.daily/logrotate to rotate mongodb logs daily:

    kill -SIGUSR1 `pidof mongodb`
