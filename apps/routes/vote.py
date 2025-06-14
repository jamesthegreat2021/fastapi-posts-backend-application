from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from .. import schemas, models,database,oauth2
from sqlalchemy.orm import Session

router = APIRouter(

    prefix="/vote", 
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(vote.post_id)
    print(vote.dir)
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"the post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    voted_post = vote_query.first()
    
    if vote.dir == 1:
        if voted_post:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has voted on the post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesifuly added the vote"}
    
    else: 
        if not voted_post:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "succesifuly deleted vote"}

        
       
       
