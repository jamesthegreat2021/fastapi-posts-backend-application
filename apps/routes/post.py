from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func



router = APIRouter(

    prefix = "/posts", 
    tags = ['Posts']

)

@router.get("/", response_model= list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    print(search)
    print(limit)
    print(skip)
    print(current_user.email)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()
    print(results)
    
    return [{"post": post, "votes": votes} for post, votes in results]




@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def generate_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) values (%s, %s, %s) returning *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()

    
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{id}", response_model = schemas.Post)
def get_a_single_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    #new_post = cursor.fetchone()
    #print(new_post)
    print(id)

    post = db.query(models.Post).filter(models.Post.id == id).first()

    print(post)

    if not post:

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= 'not found')
    
    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" DELETE from posts WHERE id = %s returning * """, (str(id),))
    #deleted_post = cursor.fetchone()
    
    #conn.commit()
    
    post_delete = db.query(models.Post).filter(models.Post.id == id)


    post = post_delete.first()

    if post == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post {id} to be deleted not found')
    #query here and not the actual data
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"the post {post.id}  you want to delete is not yours, it is of user {post.owner_id}")
    post_delete.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts set title = %s, content = %s, published = %s where id = %s returning * """, (post.title, post.content,post.published, (str(id),)))
    #updated_post = cursor.fetchone()
    
    #conn.commit()
    print(current_user.id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post {id} is nowhere to be found')
    
    if post_to_update.owner_id != current_user.id: 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"failed to update post with id {post_to_update.id}, the owner is {post_to_update.owner_id}")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()