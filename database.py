import psycopg2
from psycopg2 import pool
import time
from datetime import datetime, timezone

class Database:
  def connect(self):
    print("initializing postgres")
    self.pool = psycopg2.pool.ThreadedConnectionPool(1, 10,
      host="192.168.50.85",
      database="plantmonitor",
      user="app",
      password="abc123"
    )

    

  def getVersion(self):
    conn = self.pool.getconn()
    cur = conn.cursor()
    cur.execute('SELECT version()')

    db_version = cur.fetchone()
    print(db_version)
    cur.close()
    return db_version

  def saveImage(self, name, image):
    conn = self.pool.getconn()
    cur = conn.cursor()

    dt = datetime.now(timezone.utc)

    cur.execute('INSERT INTO images (name, file, timestamp) VALUES (%s, %s, %s) RETURNING id', (name, image,dt))
    returned_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    return returned_id

  def getImageById(self, id):
    conn = self.pool.getconn()
    cur = conn.cursor()

    print(id)

    cur.execute('SELECT file FROM images WHERE id = %s', (id,))
    f = cur.fetchone()
    cur.close()

    if (f == None):
      return None

    return f[0]