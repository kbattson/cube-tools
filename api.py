from fastapi import FastAPI
from similarity import get_recs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
)

@app.get('/recommend')
def recommend(cube_id: str):
    return get_recs(cube_id)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=5000)
