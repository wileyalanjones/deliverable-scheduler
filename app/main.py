from fastapi import (
    FastAPI, 
    Request, 
    UploadFile, 
    File, 
    HTTPException,
    status
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.parsing.base import extract_text
from app.extraction.factory import get_extractor
from app.database import SessionLocal, Base, engine
from app.models import (
    User,
    AuthProvider,
    Document,
    FileType,
    FileStatus,
    ItemStatus,
    ExtractedItem as ItemRow
)
from app.calendar.schemas import CalendarEvent
from app.calendar.mock import MockCalendarProvider

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
calendar = MockCalendarProvider()
Base.metadata.create_all(bind=engine)


db = SessionLocal()
demo_user = db.query(User).first()
if demo_user is None:
    demo_user = User(email="demo@example.com", auth_provider=AuthProvider.DEMO)
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
DEMO_USER_ID = demo_user.id
db.close()

@app.get("/")
def upload_page(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse(request, "upload.html", {"error": error})


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/review")
def review(request: Request):
    db = SessionLocal()
    items = db.query(ItemRow).filter(
        ItemRow.status == ItemStatus.PENDING
    ).all()

    db.close()
    return templates.TemplateResponse(request, "review.html", {"items": items})


@app.get("/calendar")
def calendar_view(request: Request):
    return templates.TemplateResponse(
        request, 
        "calendar.html",
        {"events": calendar.list_events()},
    )


@app.post("/upload")
async def upload(file: UploadFile | None = None):
    if file is None or not file.filename:                 
        return RedirectResponse("/?error=empty", status_code=303)

    data = await file.read()
    if not data:               
        return RedirectResponse("/?error=empty", status_code=303)

    file_type = file.filename.split(".")[-1].lower()

    try:
        FileType(file_type)
    except ValueError:
        return RedirectResponse(f"/?error={file_type}", status_code=303)

    text = extract_text(data, file_type)
    items = get_extractor().extract(text)

    db = SessionLocal()
    document = Document(
        user_id = DEMO_USER_ID,
        filename = file.filename,
        file_type = FileType(file_type),
        status = FileStatus.PARSED,
        parsed_text = text,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    for item in items:
        db.add(
            ItemRow(
                document_id=document.id,
                title=item.title,
                deliverable_date=item.deliverable_date,
                description=item.description,
                confidence=item.confidence,
                source_quote=item.source_quote,
                status=ItemStatus.PENDING
            )
        )

    db.commit()
    db.close()

    return RedirectResponse("/review", status_code=303)


@app.post("/items/{item_id}/approve")
def approve(item_id: int):
    db = SessionLocal()
    item = db.get(ItemRow, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    event = CalendarEvent(
        title=item.title,
        date=item.deliverable_date,
        description=item.description,
    )
    event_id = calendar.create_event(event)

    item.status = ItemStatus.APPROVED 
    item.provider_event_id = event_id
    db.commit()
    db.close()

    return RedirectResponse("/review", status_code=303)


@app.post("/items/{item_id}/reject")
def reject(item_id: int):
    db = SessionLocal()
    item = db.get(ItemRow, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    item.status = ItemStatus.REJECTED 
    db.commit()
    db.close()

    return RedirectResponse("/review", status_code=303)


@app.post("/calendar/clear")
def clear_calendar():
    calendar.clear()
    return RedirectResponse("/calendar", status_code=303)


@app.post("/calendar/events/{event_id}/delete")
def delete_event(event_id: str):
    calendar.delete_event(event_id)
    return RedirectResponse("/calendar", status_code=303)