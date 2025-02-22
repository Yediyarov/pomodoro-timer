from fastapi import FastAPI
from handlers import task_router

app = FastAPI()


app.include_router(task_router)