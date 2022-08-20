from flask import Flask
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


flaskapp = Flask(__name__, static_folder='build', static_url_path='')


@flaskapp.route('/')
def router():
    return flaskapp.send_static_file('index.html')


app = FastAPI()
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_credentials=True,
    allow_origin_regex="http://0.0.0.0:*",
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/v1")
def read_main():
    return {"message": "Доброе утро!"}


app.mount("/", WSGIMiddleware(flaskapp))


@app.on_event("startup")
async def startup_event():
    logger.warning("Starting up!")


@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("Shutting down!")


def main():
    # handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    uvicorn.run("server:app", reload=True, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()

# http://127.0.0.1:8080/
