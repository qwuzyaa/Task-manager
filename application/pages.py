from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from application.functions import *

router = APIRouter(tags=['Pages'])

templates = Jinja2Templates(directory='templates')


@router.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("startpage.html", {"request": request})

@router.post("/")
def start_page_forms(request: Request, form_type: str = Form(...), name: str = Form(None), username: str = Form(...),password: str = Form(...)):
    if form_type == "login":
        user = get_user_username(username)
        if user and get_pass(username)[0] == password:
            response = RedirectResponse("/homepage", status_code=303)
            response.set_cookie("user_id", str(user[0]))
            return response
        return templates.TemplateResponse("startpage.html", {"request": request, "error": "Ошибка входа"})

    elif form_type == "register":
        if get_user_username(username):
            return templates.TemplateResponse("startpage.html",
                                              {"request": request, "error": "Пользователь уже существует"})
        user_id = create_user(name, username, password)
        response = RedirectResponse("/homepage", status_code=303)
        response.set_cookie("user_id", str(user_id))
        return response

@router.get("/homepage")
def homepage(request: Request, search: str = ""):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    user = get_user_id(int(user_id))
    all_tasks = get_tasks(int(user_id))
    if search:
        print(search)
        tasks = get_task_name(search, int(user_id))
    else:
        tasks = all_tasks
    total = len(all_tasks)
    active = len([i for i in all_tasks if i[4] == 0])
    completed = len([i for i in all_tasks if i[4] == 1])
    today = datetime.now().date()
    overdue = 0
    for i in all_tasks:
        limit_time = i[5]
        if limit_time and i[4] != 1:
            deadline = datetime.strptime(limit_time, "%Y-%m-%d").date()
            if deadline < today:
                overdue += 1
    return templates.TemplateResponse("homepage.html", {
        "request": request,
        "user": user,
        "tasks": tasks,
        "total": total,
        "completed": completed,
        "active": active,
        "overdue": overdue,
        "search": search
    })

@router.post("/update_task_status/{task_id}")
def update_task_status(task_id: int, request: Request, status: int = Form(...)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    update_status(task_id, status)
    return RedirectResponse(request.headers.get("referer", "/homepage"), status_code=303)

@router.delete("/delete_user")
def delete_user_button(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    delete_user_id(int(user_id))
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("user_id")
    return response

@router.get("/create", response_class=HTMLResponse)
def create_task_page(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    user = get_user_id(int(user_id))
    return templates.TemplateResponse("create.html", {
        "request": request,
        "user": user
    })

@router.post("/create")
def create_task_handle(request: Request, name: str = Form(...), description: str = Form(""), limit_time: str = Form(None)):
    current_user_id = request.cookies.get("user_id")
    if not current_user_id:
        return RedirectResponse("/")
    create_task(int(current_user_id), name, description, limit_time)
    return RedirectResponse("/homepage", status_code=303)

@router.get("/edituser", response_class=HTMLResponse)
def edit_user_page(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    user = get_user_id(int(user_id))
    return templates.TemplateResponse("edituser.html", {
        "request": request,
        "user": user
    })

@router.post("/edituser")
def edit_user_submit(request: Request,name1: str = Form(None),username1: str = Form(None),oldpassword: str = Form(None),newpassword: str = Form(None)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    update_user(user_id, name1, username1, newpassword)
    return RedirectResponse("/homepage", status_code=303)

@router.get("/edittask", response_class=HTMLResponse)
def edit_task_page(request: Request, task_id: int):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    user = get_user_id(int(user_id))
    task = get_task_id(task_id, int(user_id))
    return templates.TemplateResponse("edittask.html", {
        "request": request,
        "user": user,
        "task": task
    })

@router.post("/edittask")
def edit_task(request: Request,task_id: int,name: str = Form(),description: str = Form(""),limit_time: str = Form(None)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    update_task(task_id, int(user_id), name, description, None, limit_time)
    return RedirectResponse("/homepage", status_code=303)

@router.delete("/delete_task")
def delete_task_button(request: Request, task_id: int):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse("/")
    delete_task(task_id, int(user_id))
    response = RedirectResponse("/homepage", status_code=303)
    return response