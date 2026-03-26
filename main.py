from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import mstache
import os
import uvicorn

app = FastAPI()

def render_template(template_name: str, context: dict) -> str:
    template_path = os.path.join("templates", template_name)
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    return mstache.render(template, context)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = {
        "title": "Главная страница",
        "items": ["Товар 1", "Товар 2", "Товар 3"],
        "user": {"name": "Иван", "is_admin": True}
    }
    return render_template("index.html", context)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
