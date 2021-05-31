### Requirements

* python3.6
* postgres
* ubuntu 18.04

### setup

* install postgres:

  ```bash
  apt update
  apt install postgresql postgresql-contrib
  ```

* create python env:

  ```bash
  virtualenv -p python3.6 token-env
  ```

* activate it:

  ```bash
  . token-env/bin/activate
  ```

* install python requirements:

  ```bash
  pip install -r requirements.txt
  ```

* Create Database
  * sudo -i -u postgres

  * createdb test-db

  * psql test-db

  * change the method of postgres !!

    from peer to md5 inside the file: [`/etc/postgresql/10/main/pg_hba.conf`]
    https://gist.github.com/AtulKsol/4470d377b448e56468baef85af7fd614

### running

* token generator:  `generate_tokens.py` has the function **generate_tokens** which does the task

  ```bash
  python generate_tokens.py
  ```

  args:

  - `--token_len`: default 7
  - `--num`: default 10 millions
  - `--file`: default tokens.txt

  * 

* token reader: `read_tokens.py`: has the function read_**tokens_postgres**

  example:

  ```bash
  python read_tokens.py
  ```

  - `--file`: default tokens.txt
  - `--database`: not useful now