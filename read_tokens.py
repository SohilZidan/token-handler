import argparse
import os
import time
import sys
from typing import List, Tuple
from psycopg2 import sql
import psycopg2


def parse_args():
    """
    argument parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', default="tokens.txt", help="the storage file path")
    parser.add_argument('--database', '--db', choices=['redis', 'postgres'], default="postgres")
    return parser.parse_args()

# def read_tokens_redis(file, db):
#     r = redis.Redis(db=db)
#     r.flushall()
#     with open(file, 'r') as f:
#         for line in tqdm(f):
#             _token = line.strip()
#             r.zincrby("_duplicates", 1, _token)
#     res = r.zrangebyscore("_duplicates", min="(1", max="+inf", withscores=True)
#     return res

def read_tokens_postgres(file: str, db: str, user: str='postgres') -> List[Tuple[str, int]]:
    """read tokens from `file` and usind `user` and database `db`.
    Store tokens in the db, compute frequencies of duplicate.

    Args:
        file (str): path of the tokens file
        db (str): database name, it has to be already created
        user (str, optional): user of postgreSQL. Defaults to 'postgres'.

    Returns:
        List[Tuple[str, int]]: duplicated tokens
    """

    # connect
    conn = psycopg2.connect(f"dbname='{db}' user='{user}'")
    cur = conn.cursor()


    # 0 # create tables
    cur.execute(
    sql.SQL("""create TEMP TABLE {}
    (
        ident serial PRIMARY KEY,
        token varchar NOT NULL
    );""").format(sql.Identifier("TMPTOKENS"))
    )
    # 1 # copy TMPTOKENS (token) from file;

    cur.execute(
        sql.SQL("copy {} (token) from %s").format(sql.Identifier('TMPTOKENS')),
        [file]
    )

    # 2 # create access tokens table with frequencies
    cur.execute(
        sql.SQL("""
        create TEMP table {}
        as
        select token, count(token) as freq
        from {}
        group by token;
        """).format(sql.Identifier("access_tokens"), sql.Identifier("TMPTOKENS"))
    )
    # 3 # create unique index on access_tokens(token)
    cur.execute(
        sql.SQL(
            "create unique index on {}(token)"
            ).format(sql.Identifier("access_tokens"))
    )

    # 4 # a list of duplicates
    cur.execute(
        sql.SQL(
            "select * from {} as at where at.freq > %s;").format(sql.Identifier("access_tokens")),
        [1]
    )
    res = cur.fetchall()

    cur.close()
    conn.close()
    return res


if __name__=="__main__":
    args = parse_args()
    file_path = os.path.realpath(args.file)
    if not os.path.exists(file_path):
        sys.exit("file does not exist")

    current_time = time.time()
    if args.database == 'postgres':
        _res = read_tokens_postgres(file_path, 'test-db', 'postgres')
    else:
        _res = [] #read_tokens_redis(file_path, db=0)

    end_time = time.time()
    print("elapsed time =", end_time-current_time)
    print("duplicates:", len(_res))
