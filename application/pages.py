from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(tags=['pages'])

templates = Jinja2Templates(directory='templates')

'''
@router.get("/startpage", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("startpage.html", {"request": request})
'''
@router.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("startpage.html", {"request": request})

@router.get("/homepage", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@router.get("/create", response_class=HTMLResponse)
def create_task_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})
