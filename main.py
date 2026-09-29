import os
from contextlib import redirect_stdout
from io import StringIO

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from interpreter import Interpreter
from lexer import tokenize
from parser import Parser


class RunRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=5000)


app = FastAPI(title="7TO5", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "font-src 'self' data:;"
    )
    return response


def run_7to5(source: str) -> str:
    tokens = tokenize(source)
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()
    buffer = StringIO()
    with redirect_stdout(buffer):
        interpreter.run(program)
    return buffer.getvalue().strip()


@app.get("/")
async def root():
    return RedirectResponse(url="/learn")


@app.get("/learn")
async def learn(request: Request):
    return templates.TemplateResponse(request=request, name="learn.html", context={})


@app.get("/try")
async def try_page(request: Request):
    return templates.TemplateResponse(request=request, name="try.html", context={})


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(request=request, name="about.html", context={})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/run")
async def run_code(payload: RunRequest):
    try:
        output = run_7to5(payload.code)
        return {"ok": True, "output": output}
    except Exception as exc:  # pragma: no cover
        return JSONResponse(status_code=400, content={"ok": False, "error": str(exc)})


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)