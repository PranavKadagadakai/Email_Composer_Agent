# app/main.py

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.config import get_settings
from app.services.orchestrator import EmailOrchestrator
from app.utils.logger import setup_logger

setup_logger()
get_settings()

app = FastAPI(title="Email Composer Agent")

templates = Jinja2Templates(directory="app/templates")
orchestrator = EmailOrchestrator()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send", response_class=HTMLResponse)
def send_email(
    request: Request,
    to_email: str = Form(...),
    task: str = Form(...),
    tone: str = Form("professional"),
):
    try:
        result = orchestrator.compose_and_send(
            request_model := type(
                "EmailRequest",
                (),
                {"to_email": to_email, "task": task, "tone": tone, "constraints": None},
            )()
        )

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "success": f"Email sent to {to_email}",
                "subject": result["subject"],
            },
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(e),
            },
        )


app.include_router(router)
