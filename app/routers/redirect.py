from fastapi import status, HTTPException, Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
from app.database import Session, get_db
from app import models
from user_agents import parse

router = APIRouter(
    prefix="/s",
    tags=["Shorted URL"]
)


@router.get('/{url_short}')
async def redirect_to_url(request: Request,
                          url_short: str,
                          db: Session = Depends(get_db)):

    query = db.query(models.URL).filter(models.URL.shorten_url == url_short).first()
    user_access = query.owner_id
    redirection = query.url

    # logging.info
    user_agent = request.headers.get("User-Agent")
    ua_string = str(user_agent)
    user_agent_obj = parse(ua_string)

    new_url_log = models.URLLog(user_accessibility=user_access,
                                client_browser=user_agent_obj.browser.family,
                                client_os=user_agent_obj.os.family,
                                client_device=user_agent_obj.device.family,
                                client_ip=request.client.host)

    db.add(new_url_log)
    db.commit()
    db.refresh(new_url_log)

    if 'https://' in redirection or 'http://' in redirection:
        return RedirectResponse(url=redirection)
    else:
        return RedirectResponse(url=f'https://{redirection}')
