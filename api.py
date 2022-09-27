from fastapi import FastAPI, Request, Response, Header, status
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Union
from misc import email_validation, generate_license, validate_password, email_code
from data_base import check_email, check_login, check_invite, add_user, change_pass, add_pass_token, fetch_pass_token, password_reset, delete_pass_token, fetch_user, set_hwid, reset_hwid
from email_module import send_email
import uvicorn
import asyncio
import logging
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
logging.getLogger('asyncio').setLevel(logging.CRITICAL)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class email_model(BaseModel):
    user_email: str

class login_model(BaseModel):
    user_email: str
    user_password: str    

class register_model(BaseModel):
    user_email: str
    user_password: str
    user_invite_code: str

class change_password_model(BaseModel):
    user_password: str
    user_email: str 
    new_password: str

class update_password_model(BaseModel):
    reset_token: str 
    user_email: str
    new_password: str

class auth_model(BaseModel):
    user_license: str 
    user_hwid: str 

@app.get("/")
async def home_page(request: Request):
    try:
        if request.cookies["user_data"] != None:
            return RedirectResponse(url='/dash')
    except KeyError:
        return RedirectResponse(url='/login')        
        
@app.get("/dash")
async def dashboard(request: Request):
    print(request.headers["user-agent"])
    if "iPhone" in request.headers["user-agent"] or "Android" in request.headers["user-agent"]:
        return {"error": "Dashboard Can Not Be Accessed On A Mobile Device"}

    return templates.TemplateResponse("dash.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request):
    try:
        if request.cookies["user_data"] != None:
            return RedirectResponse(url='/dash')
    except KeyError:
        return RedirectResponse(url='/login')      

@app.get("/login")
async def login_page(request: Request):
    try:
        if request.cookies["user_data"] != None:
            return RedirectResponse(url='/dash')
    except KeyError:
        return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def login_page(request: Request):
    try:
        if request.cookies["user_data"] != None:
            return RedirectResponse(url='/dash')
    except KeyError:
        return templates.TemplateResponse("register.html", {"request": request})    

@app.get("/reset")
async def reset_password(request: Request):
    try:
        reset_code = request.query_params["code"]
        user_email = request.query_params["email"]
        if fetch_pass_token(reset_code, user_email) == True:
            return templates.TemplateResponse("reset_password.html", {"request": request})  
        else:
            return RedirectResponse(url='/login')        
    except KeyError:
        return RedirectResponse(url='/login')        

@app.post("/api/login")
async def login(login_model: login_model, response: Response, request: Request):
    content_type = request.headers.get('content-type')
    if request.method != "POST" or "application/json" not in content_type:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return {"sucess": False, "error": "invalid request/content type", "status_code": "405"} 

    user_details = check_login(login_model.user_email, login_model.user_password)      

    if user_details == False:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"sucess": False, "error": "email or password not recognised", "status_code": "403"}
    else:
        return {"sucess": True, "email": user_details["email"], "password": user_details["password"], "license": user_details["license"], "license_type": user_details["license_type"], "plan_type": user_details["plan_type"], "hwid": user_details["hwid"]}

@app.post("/api/register")
async def register_account(register_model: register_model, response: Response, request: Request):
    content_type = request.headers.get('content-type')
    if request.method != "POST" or "application/json" not in content_type:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return {"sucess": False, "error": "invalid request/content type", "status_code": "405"}
    if validate_password(register_model.user_password) != True:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"sucess": False, "error": "password strength invalid", "status_code": "401"}
    if email_validation(register_model.user_email) == False:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"sucess": False, "error": "invalid email", "status_code": "403"}    
    if check_login(register_model.user_email, register_model.user_password) != False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"sucess": False, "error": "email alredy registerd", "status_code": "400"}
    if check_invite(register_model.user_invite_code) != True:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"sucess": False, "error": "invalid invite code", "status_code": "403"}    
    if add_user(register_model.user_email, register_model.user_password, generate_license()) != True:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"sucess": False, "error": "internal server error", "status_code": "500"}
    else:
        return {"sucess": True}

@app.post("/api/change_password")
async def change_password(change_password_model: change_password_model, response: Response, request: Request):
    content_type = request.headers.get('content-type')
    if request.method != "POST" or "application/json" not in content_type:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return {"sucess": False, "error": "invalid request/content type", "status_code": "405"}
    if validate_password(change_password_model.new_password) != True:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"sucess": False, "error": "password strength invalid", "status_code": "401"}   
    if check_login(change_password_model.user_email, change_password_model.user_password) == False:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"sucess": False, "error": "password not recognised", "status_code": "403"}
    if change_pass(change_password_model.user_password, change_password_model.new_password) != True:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"sucess": False, "error": "internal server error", "status_code": "500"}

    return True     

@app.post("/api/update_password")
async def update_password(update_model: update_password_model, response: Response, request: Request):
    content_type = request.headers.get('content-type')
    if request.method != "POST" or "application/json" not in content_type:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    if validate_password(update_model.new_password) != True:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"sucess": False, "error": "password strength invalid", "status_code": "401"}    
    if fetch_pass_token(update_model.reset_token, update_model.user_email) != True:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"sucess": False, "error": "invalid password token or email", "status_code": "401"}
    if password_reset(update_model.user_email, update_model.new_password) != True:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"sucess": False, "error": "internal server error", "status_code": "500"}    

    delete_pass_token(update_model.reset_token)
    return {"sucess": True}


@app.post("/api/forgot_password")
async def forgot_password(email_model: email_model, response: Response, request: Request):
    content_type = request.headers.get('content-type')
    if request.method != "POST" or "application/json" not in content_type:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    if check_email(email_model.user_email) != True:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"sucess": False, "error": "email not recognised", "status_code": "404"}
    
    password_code = email_code()
    if send_email(email_model.user_email, password_code) != True:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"sucess": False, "error": "recover email cant send", "status_code": "500"}
    
    add_pass_token(password_code, email_model.user_email)
    return {"sucess": True}    

@app.post("/api/bot/auth")
async def bot_auth(auth_model: auth_model, response: Response, request: Request):
    content_type = request.headers.get('content-type')
    if request.method != "POST" or "application/json" not in content_type:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED

    if user := fetch_user(auth_model.user_license) != True:
        response.status_code = status.HTTP_404_NOT_FOUND     
        return {"sucess": False, "error": "invalid user license", "status_code": "404"}
    
    if user["hwid"] == "N/A":
        set_hwid(auth_model.user_license, auth_model.user_hwid)

    return {"sucess": True}     

@app.post("/api/reset_hwid")
async def reset_hwid(login_model: login_model, response: Response, request: Request):
    content_type = request.headers.get('content-type')
    if request.method != "POST" or "application/json" not in content_type:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return {"sucess": False, "error": "invalid request/content type", "status_code": "405"} 
    if reset_hwid(login_model.user_email, login_model.user_password) != True:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"sucess": False, "error": "login not found", "status_code": "404"}

    return {"sucerss": True}    


#Development start
async def main():
    config = uvicorn.Config("api:app", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())