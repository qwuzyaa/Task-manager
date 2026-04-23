from fastapi import FastAPI
import application.pages, application.api_router
import uvicorn

app = FastAPI()
app.include_router(application.api_router.router)
app.include_router(application.pages.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
