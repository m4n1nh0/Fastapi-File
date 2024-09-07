from fastapi import FastAPI

from routes import init_routes

app = FastAPI()


init_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
