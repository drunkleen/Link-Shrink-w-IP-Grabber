from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from app import models, oauth2
from app.database import Session, get_db
from app.schemas import urlschema
from app.utility import url_shorter

router = APIRouter(
    prefix="/url",
    tags=["URL Generator"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=urlschema.URLOut)
async def create_url(n_url: urlschema.URLCreate, db: Session = Depends(get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    shorted = url_shorter(n_url.url)
    new_url = models.URL(owner_id=current_user.id, shorten_url=shorted, **n_url.dict())
    db.add(new_url)  # add the new post
    db.commit()  # push the new changes into database
    db.refresh(new_url)  # returning post from database
    print("\n\n\n\n",new_url.shorten_url)
    return new_url


@router.get('/{url_id}', response_model=urlschema.GetURL)
async def get_post(url_id: int, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    url = db.query(models.URL).filter(models.URL.id == url_id).first()
    if not url:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"url with {url_id} doesn't exist.")

    return url


@router.delete('/{url_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(url_id: int, db: Session = Depends(get_db),
                      current_user: id = Depends(oauth2.get_current_user)):
    url_query = db.query(models.URL).filter(models.URL.id == url_id)
    deleted_url = url_query.first()

    if not deleted_url:  # check if there is not matched id
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"url with {url_id} doesn't exist.")
    if deleted_url.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="Action is Unauthorized")

    url_query.delete(synchronize_session=False)
    db.commit()  # push the new changes into database

    return Response(status_code=status.HTTP_204_NO_CONTENT)
