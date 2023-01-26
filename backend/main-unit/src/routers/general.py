from typing import List

from fastapi import APIRouter
from starlette.responses import RedirectResponse


router = APIRouter(tags=['global'])


@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


