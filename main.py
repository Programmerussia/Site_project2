from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
import starlette.status
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)
templates = Jinja2Templates(directory='templates')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

SESSION_KEY ="1234"
def  dayName():
    now = datetime.now()      # текущие дата и время
    days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
    return days[datetime.weekday(now)]

@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return templates.TemplateResponse('index.html', {'request': request, 'data':data})

@app.get('/carousel', response_class=HTMLResponse)
def root(request: Request):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    day = dayName()
    return templates.TemplateResponse('carousel.html', {'request': request, 'data':data,'day':day})

@app.get('/admin', response_class=HTMLResponse)
def admin(request: Request):
    if request.session.get("my_var", None) == SESSION_KEY:
        return templates.TemplateResponse('admin.html', {'request': request})
    else:
        return  templates.TemplateResponse('login.html', {'request': request})

@app.get("/a")
async def session_set(request: Request):
    request.session["my_var"] = "1234"
    return 'ok'


@app.get("/b")
async def session_info(request: Request):
    my_var = request.session.get("my_var", None)
    return my_var


@app.post('/postdata', response_class=HTMLResponse)
def change_data(request: Request, dropdown = Form(), day = Form(), time = Form(), lesson_name = Form(), room = Form()):
    data = {}
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('data.json', 'w', encoding='utf-8') as f:
        cls, group = dropdown.split('.')
        data[day][cls][group][time] = lesson_name + '\n'+ '(' + 'каб.'+ room + ')'
        json.dump(data, f, ensure_ascii=False, indent=4)
    return templates.TemplateResponse('admin.html', {'request': request})




@app.get('/login', response_class=HTMLResponse)
def login_html(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.post('/logindata')
async def login(request: Request, email = Form(), password = Form()):

    with open('users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        try:
            if data[email] == password:
                request.session["my_var"] = SESSION_KEY
                return RedirectResponse(url='/admin', status_code=starlette.status.HTTP_302_FOUND)
        except:
            pass
        return RedirectResponse(url='/login', status_code=starlette.status.HTTP_303_SEE_OTHER)