from fastapi import APIRouter

testController = APIRouter(prefix='/test')


@testController.get("/")
async def root():
    return {"message": "Hello World"}


@testController.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
