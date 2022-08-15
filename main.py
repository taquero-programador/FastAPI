#!/usr/bin/env python3

from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: int = Path(default=int, title="ID item", gt=0, le=1000),
    q: str):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result
