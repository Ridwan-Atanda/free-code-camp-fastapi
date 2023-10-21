from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    prefix= "/vote",
    tags= ['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
         current_user : int = Depends(oauth2.get_current_user)):
    print(f'we are nowwwwwww champ ')
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    print(f'we are nowwwwwww {post} ')

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{vote.post_id} doesnt exist")

    print(current_user.id)
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) ##we check if the post id supplied by front end mathes the post id in our db ##we also check if the user id in db matches the user id supplied 
    print(vote_query)
    found_vote = vote_query.first()

    print(found_vote)

    if(vote.dir == 1):
        if found_vote:
          raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'user {current_user.id} has already voted on post {vote.post_id}')
        
        #this is the else part for when the vote is not found in our db 
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        print(f'new_vote....{new_vote}')

        db.add(new_vote)
        db.commit()
        return{"message":"successfully added vote"}
    
    else: #(vote.dir != 1)
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "succssfully deleted vote"}