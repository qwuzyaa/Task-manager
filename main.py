from fastapi import FastAPI
import application.pages, application.api_router
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(application.api_router.router)
app.include_router(application.pages.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)

