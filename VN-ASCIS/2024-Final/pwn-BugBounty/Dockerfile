FROM pwn.red/jail

COPY --from=ubuntu@sha256:58b87898e82351c6cf9cf5b9f3c20257bb9e2dcf33af051e12ce532d7f94e3fe / /srv

ENV JAIL_TMP_SIZE=1M

COPY chall /srv/app/run
COPY flag /srv/app/flag