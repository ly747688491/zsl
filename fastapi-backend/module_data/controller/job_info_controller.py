from fastapi import APIRouter

jobInfoController = APIRouter(prefix='/job')


@jobInfoController.get("/type_num")
async def get_type_num():
    return "null"
