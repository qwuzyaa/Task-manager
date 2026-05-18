from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(tags=['pages'])

templates = Jinja2Templates(directory='templates')

@router.get("/homepage", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})
