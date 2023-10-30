from fastapi import FastAPI
import json
from pathlib import Path
from fastapi.responses import FileResponse
from typing import Optional


app: FastAPI = FastAPI()

#/
@app.get("/")
async def index():
    current: Path = Path()
    file_path: Path = current /"jsonFiles/data.json"
    return FileResponse(path=file_path)

#/detail?number=int
@app.get("/detail")
async def detail(
    number: int = 0,
):
    with open('./jsonFiles/data.json', 'r') as f:
        json_load = json.load(f)
    return json_load['data'][number]



#エンジニアにとって最も重要な遊び心を忘れないために、以下のパスを混ぜてみました。
#/halloween
@app.get("/halloween")
async def halloween():
    return {'🎃': 'Happy Halloween'}

#/birthday
@app.get("/birthday")
async def birthday(
    name: Optional[str] = 'SimpleForm'
):
    return {'🎂': f'Happy birthday {name}'}