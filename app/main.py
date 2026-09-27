from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import BASE_DIR, settings
from .routes import router


app = FastAPI(title=settings.app_name)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "app" / "static"),
    name="static",
)

app.state.templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}