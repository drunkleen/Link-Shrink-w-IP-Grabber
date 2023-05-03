from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import RedirectResponse
from app.database import Session, get_db
from app import models

router = APIRouter(
    prefix="/s",
    tags=["Shorted URL"]
)


@router.get('/{url_short}')
async def redirect_to_url(url_short: str, db: Session = Depends(get_db)):

    redirection = db.query(models.URL).filter(models.URL.shorten_url == url_short).first().url

    if 'https://' in redirection or 'http://' in redirection:
        return RedirectResponse(url=redirection)
    else:
        return RedirectResponse(url=f'https://{redirection}')
