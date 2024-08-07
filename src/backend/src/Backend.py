"""
Responsible for the interactions with the frontend
"""
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
from fastapi import FastAPI, Response, Request, Depends, status, HTTPException
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from os.path import isfile
from mimetypes import guess_type
import crud
import models
from typing import List
import asyncio
import threading
import signal
import json

MESSAGE_STREAM_DELAY = 0.2


class Backend:
    def __init__(self, peer=None) -> None:
        self.peer = peer
        self.init_app()

    def init_app(self):
        self.app = FastAPI()
        origins = ["*"]
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )
        crud.create_database()
        

        @self.app.post('/create-user/{is_active}', response_model=models.User, status_code=status.HTTP_200_OK)
        def create_user(*, db: Session = Depends(crud.get_db), user_in: models.UserCreate, is_active: bool):
            user = crud.create_user(db=db, user_in=user_in, is_active=is_active)
            return user

        @self.app.get('/users', response_model=List[models.User], status_code=status.HTTP_200_OK)
        def get_all_user(db: Session = Depends(crud.get_db)):
            user = crud.get_all_users(db=db)
            return user

        @self.app.get("/user/{username}", status_code=status.HTTP_200_OK)
        def get_user_by_email(username: str, db: Session = Depends(crud.get_db)):
            user = crud.get_by_username(db=db, username=username)
            return user

        @self.app.delete('/user/{username}', status_code=status.HTTP_200_OK)
        def delete_user(username: str, db: Session = Depends(crud.get_db)):
            user_to_delete = crud.get_by_username(db=db, username=username)
            if user_to_delete is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

            crud.delete_user(db=db, username=username)
            return user_to_delete

        @self.app.get('/user-posts/{username}', response_model=List[models.Post], status_code=status.HTTP_200_OK)
        def get_user_posts(username: str, db: Session = Depends(crud.get_db)):
            user_posts = crud.get_user_posts(db=db, user_username=username)
            return user_posts

        @self.app.post('/user-posts', response_model=List[models.Post], status_code=status.HTTP_200_OK)
        def get_user_posts_latest(post_in: models.Post, db: Session = Depends(crud.get_db)):
            user_posts = crud.get_user_posts(db=db, user_username=post_in.user_username, from_date=post_in.date_created)
            return user_posts

        @self.app.get('/following-posts/{username}', response_model=List[models.Post], status_code=status.HTTP_200_OK)
        def get_user_following_posts(username: str, db: Session = Depends(crud.get_db)):
            following_posts = crud.get_following_posts(
                db=db, user_username=username)
            return following_posts

        @self.app.post('/create-post', response_model=models.Post, status_code=status.HTTP_200_OK)
        def create_post(*, db: Session = Depends(crud.get_db), post_in: models.Post):
            post = crud.create_post(db=db, post_in=post_in)
            self.peer.b_create_post(post)
            return post

        @self.app.post('/shared-post', response_model=models.Post, status_code=status.HTTP_200_OK)
        def shared_post(*, db: Session = Depends(crud.get_db), post_in: models.Post):
            post = crud.shared_post(db=db, post_in=post_in)
            return post

        @self.app.get('/post/{post_id}', response_model=List[models.Post], status_code=status.HTTP_200_OK)
        def get_post_by_id(post_id: int, db: Session = Depends(crud.get_db)):
            post = crud.get_post(db=db, post_id=post_id)
            return post

        @self.app.delete('/post/{post_id}', status_code=status.HTTP_200_OK)
        def delete_post(post_id: int, db: Session = Depends(crud.get_db)):
            post_to_delete = crud.get_post(db=db, post_id=post_id)
            if post_to_delete is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

            crud.delete_post(db=db, post_id=post_id)
            return post_to_delete

        @self.app.post('/login', status_code=status.HTTP_200_OK)
        def login(*, db: Session = Depends(crud.get_db), user_in: models.UserCreate):
            is_in_network, can_login = self.peer.b_login(user_in.username, user_in.password, db)
            if can_login:
                user = crud.login(db=db, user_in=user_in)
                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password")
                if not is_in_network:
                    self.peer.b_create_user(user.username, user.password)
                
                crud.check_remote_posts(db=db, user_username=user_in.username)
                return user
            raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password")

        @self.app.post('/logout', status_code=status.HTTP_200_OK)
        def logout(*, db: Session = Depends(crud.get_db), user_in: models.User):
            self.peer.b_logout()
            user = crud.logout(db=db, user_in=user_in)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
            return user

        @self.app.post('/user-status', response_model=models.User, status_code=status.HTTP_200_OK)
        def user_status(*,  db: Session = Depends(crud.get_db), user_in: models.User):
            user = crud.user_status(db=db, user_in=user_in)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
            return user

        @self.app.post('/start-follow', response_model=models.Follow, status_code=status.HTTP_200_OK)
        def follow(*, db: Session = Depends(crud.get_db), follow: models.Follow):
            new_follow = crud.start_follow(db=db, follow=follow)
            self.peer.b_start_follow(follow)
            return new_follow

        @self.app.post('/create-follow', response_model=models.Follow, status_code=status.HTTP_200_OK)
        def create_follow(*, db: Session = Depends(crud.get_db), follow: models.Follow):
            new_follow = crud.start_follow(db=db, follow=follow)
            return new_follow

        @self.app.get('/get-followers/{username}', response_model=List[models.User], status_code=status.HTTP_200_OK)
        def get_user_followers(*, db:Session=Depends(crud.get_db), username:str):
            user = crud.get_by_username(db=db, username=username)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

            followers = crud.get_followers(db=db, user_in=user)
            return followers

        @self.app.get('/get-following/{username}', response_model=List[models.User], status_code=status.HTTP_200_OK)
        def get_user_following(*, db:Session=Depends(crud.get_db), username:str):
            user = crud.get_by_username(db=db, username=username)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

            following= crud.get_following(db=db, user_in=user)
            return following

        @self.app.post('/unfollow', status_code=status.HTTP_200_OK)
        def delete_follow(*, db: Session = Depends(crud.get_db), follow_in: models.Follow):
            follow_to_delete = crud.get_follow(db=db, follow_in=follow_in)
            if follow_to_delete is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
            follow = crud.unfollow(db=db, follow_in=follow_in)
            self.peer.b_unfollow(follow)
            return follow

        @self.app.get('/search-user/{username}', response_model=models.User, status_code=status.HTTP_200_OK)
        def search_user(*, username:str, db: Session = Depends(crud.get_db)):
            # search for user by username in kademlia
            # return a model to the frontend
            user= self.peer.b_search_follow(username, db)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
            return user

        @self.app.get('/latest-post/{username}', response_model=models.Post, status_code=status.HTTP_200_OK)
        def get_latest_post(*, username:str, db: Session = Depends(crud.get_db)):
            post = crud.get_latest_post(db=db, user_username=username)
            if post is None:
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            return post

        @self.app.delete('/outdated-posts',response_model=List[models.Post], status_code = status.HTTP_200_OK)
        def delete_outdated_posts(*,db:Session=Depends(crud.get_db)):
            posts = crud.check_remote_posts(db=db, user_username=self.peer.id)
            return posts

        @self.app.get('/update-feed', status_code=status.HTTP_200_OK)
        async def update_feed(*, request: Request, db: Session = Depends(crud.get_db)):

            async def event_generator():
                while True:
                    # If client has closed the connection
                    if await request.is_disconnected():
                        break

                    feed = {}
                    # Checks for new messages and return them to client if any
                    if self.peer.has_new_feed():
                        print("BACKEND: Sending new feed to client")
                        feed['posts'] = self.peer.get_new_feed()
                        # connection = engine.raw_connection()
                        # with connection.cursor() as cur:
                        #     cur.execute("DECLARE c CURSOR FOR TAIL sensors_view_1s")
                        #     cur.execute("FETCH ALL c")
                        #     for row in cur:
                        #         yield row
                    if self.peer.has_new_status():
                        print("BACKEND: Sending new status to client")

                        feed['status'] = self.peer.get_new_status()
                    if feed != {}:
                        print('SENDING FEED', feed)
                        yield json.dumps(feed)
                    await asyncio.sleep(MESSAGE_STREAM_DELAY)

            return EventSourceResponse(event_generator())

    def start(self):
        self.thread = threading.Thread(target=self.run).start()

    def run(self):
        try:
            uvicorn.run(self.app, host="127.0.0.1", port=8000+self.peer.id)
        except Exception as e:
            print(e)

    def stop(self):
        self.thread.join()
        # If no work use kill $(pgrep -P $uvicorn_pid)
        os.kill(self.thread.pid, signal.SIGTERM)
