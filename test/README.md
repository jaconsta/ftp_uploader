# TESTING settings.

Based on docker and [stilliard/docker-pure-ftpd](https://github.com/stilliard/docker-pure-ftpd)

Start it 

```
$ docker run -d --name ftpd_server -p 21:21 -p 30000-30009:30000-30009 -e "PUBLICHOST=localhost" stilliard/pure-ftpd:hardened
```

Access the container and create a new user. In my case **bob** and type the password you want (like **secret**, but don't use **secret** in production).

```
$ docker exec -it ftpd_server /bin/bash

$ pure-pw useradd bob -f /etc/pure-ftpd/passwd/pureftpd.passwd -m -u ftpuser -d /home/ftpusers/bob
# and manualy add the password.
```
