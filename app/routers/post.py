from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy import func



router = APIRouter(
    prefix='/posts',
    tags= ['Posts'])

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

# Your database models and query (as previously defined)

@router.get("/", response_model=List[schemas.PostWithVoteCount])
def get_post(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    query = (
        db.query(models.Post)
        .join(models.Vote, isouter=True)
        .group_by(models.Post.id)
        .add_column(func.count(models.Vote.post_id).label('vote_count'))
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    )
    print(str(query))
    results = query.all()

    # Create a list of PostWithVoteCount objects to return
    post_data = [
        {"id": post.id, "content": post.content, "title": post.title, "vote_count": vote_count}
        for post, vote_count in results
    ]

    return post_data


# # @router.get("/", response_model=List[schemas.Post]) 
# @router.get("/", response_model= List[schemas.PostWithVoteCount])
# def get_post(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),
#              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
#     # post = db.query(models.Post).join(models.Vote, isouter=True).group_by(models.Post.id)

#     # posts = post.all()
    

#     # print(post)
#     # Original query
#     query = (
#             db.query(models.Post)
#             .join(models.Vote, isouter=True)
#             .group_by(models.Post.id)
#             .add_column(func.count(models.Vote.id).label('vote_count'))
#             .group_by(models.Post.id)
#         )
#     results = query.all()

#     post_data = [
#         PostWithVoteCount(id=post.id, title=post.title, vote_count=vote_count)
#         for post, vote_count in results
#     ]
#     # Iterate through the results
#     # for result in results:
#     #     post = result[0]  # Post object
#     #     vote_count = result[1]  # Vote count
#     #     print(f"Post ID: {post.id}, Title: {post.title}, Vote Count: {vote_count}")

#     # post1 = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
#     # print(post1)
#     # posts = post1.all() #gets all post
#     # print(current_user.id)
#     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #where post.id = 17 e.g
#     return 


# @router.get("/", response_model=List[schemas.Post])
# def get_post(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),
#              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#     print(search)
#     post1 = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
#     print(post1)
#     posts = post1.all() #gets all post
#     # print(current_user.id)
#     # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #where post.id = 17 e.g
#     return posts




##this create posts into the db 
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user : int = Depends(oauth2.get_current_user)):  #Post uses the class above to define the type of data we want from the front end 
    print(f'we are here..............1')
    print(f'this is the user_id: {current_user.email} that we need ')
    print(f'this is the user_id : {current_user.id} that we need ')
    #print(post.model_dump()) 
    #new_post = models.Post(title=post.title, content = post.content, published=post.published)
    
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) #this line uses dict form of post as set from above schema, and then we update user_id of that dict
    
    print(f'this is our new post : {new_post}')

    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



##get one post 

@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def get_post(id: int,  db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    post  = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} doesnt exist")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "not authorized to perform requested action" )
    
    print(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_user)):
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)  #this returns a query statement like select * from 
    print(f'deleted_post nana {deleted_post}')
    deleted_post_2 = deleted_post.first() #this returns a query object, the first case where our query filter matches in the database, we cant accss it
    print(f'deleted_post nnansnnsnss{deleted_post_2}')


    
    if deleted_post_2 == None: ##if our query doesnt match anything in the db 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} doesnt exist")
    
    if deleted_post_2.owner_id != current_user.id: # we check here if the id of the user trying to delete from our db matches the user id in the post table. this is to ensure a user only delete their own post 
        print(f'current user trying to delete is : {current_user.id}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "not authorized to perform requested action" )
    
    deleted_post.delete(synchronize_session= False) #we append a delete to the original query
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user : int = Depends(oauth2.get_current_user)):
     
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with {id} doesnt exist")
    print(new_post)

    if post.owner_id != current_user.id: # we check here if the id of the user trying to delete from our db matches the user id in the post table. this is to ensure a user only delete their own post 
        print(f'current user trying to delete is : {current_user.id}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "not authorized to perform requested action" )

    post_query.update(new_post.model_dump(), synchronize_session= False)
    db.commit()
    return post
 