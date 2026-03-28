from fastapi import FastAPI
from similarity import get_recs_sql
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

DB_URL = os.environ.get("DATABASE_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
)

@app.get('/recommend')
def recommend(cube_id: str):
    return get_recs_sql(cube_id)

@app.get('/test')
def test():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cubes")
    count = cur.fetchone()
    cur.close()
    conn.close()
    return {"count": count}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=5000)
