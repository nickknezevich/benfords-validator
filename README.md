# benfords-validator
Benfords validator is a small application that will allow you to upload files (txt, csv, xlxs) and test designated column dataset against the Benford's Law.

## Instalation

```bash
docker-compose build
```

```bash
docker-compose up -d
```

Client will run on http://localhost:8000
Backend will run on http://localhost:5001

## Users

There are two created users with following credentials:
username: jsmith@gmail.com, password: test1234
username: alincoln@gmail.com, password: test1234

User jsmith will have two predefined validation entries.

## In Examples you will find files which were used to test the application.
### These files resides in assets file examples.

https://github.com/nickknezevich/benfords-validator/tree/main/client/src/assets/file-examples
