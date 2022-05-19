""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from cgitb import text
from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 20, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def get_audio_ids():
    with get_db_cursor() as cur:
        cur.execute("select audio_id from audios;")
        return [r['audio_id'] for r in cur]


def get_audio(audio_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM audios where audio_id=%s", (audio_id,))
        return cur.fetchone()


def public_search(text):
    with get_db_cursor() as cur:
        cur.execute("select audio_id from (select * from audios where publicity = 1) audios where search @@ plainto_tsquery('english', %s) order by ts_rank(search, plainto_tsquery('english', %s)) desc;", (text,text))
        return [r['audio_id'] for r in cur]

# select audio_id from (select * from audios where publicity = 1) audios where search @@ plainto_tsquery('english', 'hhh') order by ts_rank(search, plainto_tsquery('english', 'hhh')) desc;
# select audio_id from (select * from audios where person_id = 'google-oauth2|100867608362971613355') audios where search @@ plainto_tsquery('english', 'private') order by ts_rank(search, plainto_tsquery('english', 'private')) desc;
def private_search(personal_id,text):
    with get_db_cursor() as cur:
        cur.execute("select audio_id from (select * from audios where person_id = %s) audios where search @@ plainto_tsquery('english', %s) order by ts_rank(search, plainto_tsquery('english', %s)) desc;", (personal_id,text,text))
        return [r['audio_id'] for r in cur]


# def upload_audio(data, filename):
#     with get_db_cursor(True) as cur:
#         cur.execute("insert into audios (person_id, description, data) values (%s, %s, %s)", ('12345', 'test', data))

def upload_audio(description,data,person_id,publicity):
    with get_db_cursor(True) as cur:
        cur.execute("insert into audios (person_id, publicity,description,search, data) values (%s, %s,%s, to_tsvector('english', %s), %s)", (person_id, publicity,description,description, data))

def get_personal_audio_ids():
    with get_db_cursor() as cur:
        cur.execute("select audio_id from audios;")
        #cur.execute("slect audio_id from audios where persnal_id=%s,(personal_id,)")
        return [r['audio_id'] for r in cur]

def get_all_public_audio_ids():
    with get_db_cursor() as cur:
        cur.execute("select audio_id from audios where publicity = 1;")
        return [r['audio_id'] for r in cur]

def get_audio_ids():    
    with get_db_cursor() as cur:
        cur.execute("select audio_id from audios;")
        #cur.execute("slect audio_id from audios where persnal_id=%s,(personal_id,)")
        return [r['audio_id'] for r in cur]

def delete_audio_ids(audio_id):
    with get_db_cursor(True) as cur:
        cur.execute("DELETE FROM audios WHERE audio_id=%s",(audio_id,))

def set_audio_pubclity(audio_id,publicity):
    with get_db_cursor(True) as cur:
        cur.execute("UPDATE audios SET publicity=%s WHERE audio_id=%s",(publicity,audio_id))

def get_audio_personal(personal_id):
    with get_db_cursor() as cur:
        cur.execute("select audio_id from audios where person_id = %s",(personal_id,))
        return [r['audio_id'] for r in cur]
