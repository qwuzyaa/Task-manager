from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from application.functions import *
from pydantic import ValidationError
from application.schemes import CreateUser, LoginUser, UpdateUser
import bcrypt

router = APIRouter(tags=['Pages'])

templates = Jinja2Templates(directory='templates')


@router.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("startpage.html", {"request": request})

@router.post("/")
def start_page_forms(request: Request, form_type: str = Form(...), name: str = Form(None), username: str = Form(...),password: str = Form(...)):
    try:
        if form_type == "login":
            try:
                login_data = LoginUser(username=username, password=password)
            except ValidationError:
                return templates.TemplateResponse("startpage.html", {"request": request})
            user = get_user_username(login_data.username)
            if user:
                stored_hash = get_pass(login_data.username)
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
                if bcrypt.checkpw(login_data.password.encode('utf-8'), stored_hash):
                    response = RedirectResponse("/homepage", status_code=303)
                    response.set_cookie("user_id", str(user[0]))
                    return response
            return templates.TemplateResponse("startpage.html", {"request": request})
        elif form_type == "register":
            try:
                register_data = CreateUser(name=name, username=username, password=password)
            except ValidationError:
                return templates.TemplateResponse("startpage.html", {"request": request})
            if get_user_username(register_data.username):
                return templates.TemplateResponse("startpage.html", {"request": request})
            hashed = bcrypt.hashpw(register_data.password.encode('utf-8'), bcrypt.gensalt())
            hashed_str = hashed.decode('utf-8')
            user_id = create_user(register_data.name, register_data.username, hashed_str)
            response = RedirectResponse("/homepage", status_code=303)
            response.set_cookie("user_id", str(user_id))
            return response
    except Exception:
        return RedirectResponse("/errorpage")

@router.get("/homepage")
def homepage(request: Request, search: str = "", filter: str = ""):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        user = get_user_id(int(user_id))
        all_tasks = get_tasks(int(user_id))
        if search:
            tasks = get_task_name(search, int(user_id))
        elif filter == "completed":
            tasks = get_tasks_complited(int(user_id))
        elif filter == "in_progress":
            tasks = get_tasks_active(int(user_id))
        elif filter == "over":
            tasks = get_tasks_over(int(user_id))
        elif filter == "limit":
            tasks = get_tasks_limit(int(user_id))
        elif filter == "priority_low":
            tasks = get_tasks_priority(int(user_id), 0)
        elif filter == "priority_med":
            tasks = get_tasks_priority(int(user_id), 1)
        elif filter == "priority_high":
            tasks = get_tasks_priority(int(user_id), 2)
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
            "search": search,
            "current_filter": filter
        })
    except Exception:
        return RedirectResponse("/errorpage")

@router.post("/logout")
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("user_id")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@router.post("/update_task_priority/{task_id}")
def update_task_priority(task_id: int, request: Request, priority: int = Form(...)):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        update_priority(task_id, priority)
        return RedirectResponse(request.headers.get("referer", "/homepage"), status_code=303)
    except Exception:
        return RedirectResponse("/errorpage")

@router.post("/update_task_status/{task_id}")
def update_task_status(task_id: int, request: Request, status: int = Form(...)):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        update_status(task_id, status)
        return RedirectResponse(request.headers.get("referer", "/homepage"), status_code=303)
    except Exception:
        return RedirectResponse("/errorpage")

@router.delete("/delete_user")
def delete_user_button(request: Request):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        delete_user_id(int(user_id))
        response = RedirectResponse("/", status_code=303)
        response.delete_cookie("user_id")
        return response
    except Exception:
        return RedirectResponse("/errorpage")

@router.get("/create", response_class=HTMLResponse)
def create_task_page(request: Request):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        user = get_user_id(int(user_id))
        return templates.TemplateResponse("create.html", {
            "request": request,
            "user": user
        })
    except Exception:
        return RedirectResponse("/errorpage")

@router.post("/create")
def create_task_handle(request: Request, name: str = Form(...), description: str = Form(""), limit_time: str = Form(None)):
    try:
        current_user_id = request.cookies.get("user_id")
        if not current_user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        create_task(int(current_user_id), name, description, limit_time)
        return RedirectResponse("/homepage", status_code=303)
    except Exception:
        return RedirectResponse("/errorpage")

@router.get("/edituser", response_class=HTMLResponse)
def edit_user_page(request: Request):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        user = get_user_id(int(user_id))
        return templates.TemplateResponse("edituser.html", {
            "request": request,
            "user": user
        })
    except Exception:
        return RedirectResponse("/errorpage")

@router.post("/edituser")
def edit_user_submit(request: Request,name: str = Form(None),username: str = Form(None),oldpassword: str = Form(None),newpassword: str = Form(None)):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            return RedirectResponse("/")
        user = get_user_id(int(user_id))
        try:
            update_data = UpdateUser(name=name, username=username, password=newpassword)
        except ValidationError:
            return RedirectResponse("/edituser", status_code=303)
        if username and username != user[2]:  # если username изменён
            existing_user = get_user_username(username)
            if existing_user:
                return templates.TemplateResponse("edituser.html", {
                    "request": request,
                    "user": user})
        if newpassword:
            stored_hash = get_pass(user[2])
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode('utf-8')
            if not bcrypt.checkpw(oldpassword.encode('utf-8'), stored_hash):
                return templates.TemplateResponse("edituser.html", {
                    "request": request,
                    "user": user
                })
            hashed_new_password = bcrypt.hashpw(newpassword.encode('utf-8'), bcrypt.gensalt())
            hashed_new_password_str = hashed_new_password.decode('utf-8')
            update_user(int(user_id), None, None, hashed_new_password_str)
            return RedirectResponse("/homepage", status_code=303)
        if name or username:
            update_user(int(user_id), update_data.name, update_data.username, None)
            return RedirectResponse("/homepage", status_code=303)
        return RedirectResponse("/homepage", status_code=303)
    except Exception:
        return RedirectResponse("/errorpage")

@router.get("/edittask", response_class=HTMLResponse)
def edit_task_page(request: Request, task_id: int):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        user = get_user_id(int(user_id))
        task = get_task_id(task_id, int(user_id))
        return templates.TemplateResponse("edittask.html", {
            "request": request,
            "user": user,
            "task": task
        })
    except Exception:
        return RedirectResponse("/errorpage")

@router.post("/edittask")
def edit_task(request: Request,task_id: int,name: str = Form(None),description: str = Form(""),limit_time: str = Form(None)):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        if limit_time is None:
            update_task(task_id, int(user_id), name, description, None, None, None)
        else:
            update_task(task_id, int(user_id), name, description, None, limit_time, None)
        return RedirectResponse("/homepage", status_code=303)
    except Exception as e:
        print(e)
        return RedirectResponse("/errorpage")

@router.delete("/delete_task")
def delete_task_button(request: Request, task_id: int):
    try:
        user_id = request.cookies.get("user_id")
        if not user_id:
            response = RedirectResponse("/", status_code=303)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response
        delete_task(task_id, int(user_id))
        response = RedirectResponse("/homepage", status_code=303)
        return response
    except Exception:
        return RedirectResponse("/errorpage")

@router.get("/errorpage")
@router.post("/errorpage")
def error(request: Request):
    return templates.TemplateResponse("errorpage.html", {"request": request})