from sqlalchemy.orm import Session
import models
import schemas
import database
import datetime

TIMER = 60


def create_database():
    print("Creating db")
    return database.Base.metadata.create_all(bind=database.engine)


def check_remote_posts(db: Session, user_username: str):
    posts_delete = []
    d2 = datetime.datetime.now()
    posts = db.query(schemas.Post).filter(schemas.Post.user_username !=
                                          user_username).order_by(schemas.Post.date_stored.asc()).all()
    for post in posts:
        from_date = post.date_stored
        difference = (d2 - from_date).total_seconds()
        if difference >= TIMER:
            if (len(posts) - len(posts_delete) > 1):  # make sure we keep at least one post in the db
                posts_delete.append(post)
                db.delete(post)
                db.commit()

    return posts_delete


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: Session, user_in: models.UserCreate, is_active: bool = True):

    new_user = schemas.User(
        username=user_in.username,
        password=user_in.password,
        is_active=is_active
    )

    db.add(new_user)
    db.commit()

    return new_user


def get_by_username(db: Session, username: str):
    users = db.query(schemas.User).filter(
        schemas.User.username == username).first()
    return users


def get_all_users(db: Session):
    user = db.query(schemas.User).all()  # type: ignore
    return user


def get_user_posts(db: Session, user_username: str, from_date: datetime.datetime = None):
    if from_date is None:
        print("from_date is None in curd get_user_posts")
        return db.query(schemas.Post).filter(
            schemas.Post.user_username == user_username).all()
    return db.query(schemas.Post).filter(schemas.Post.user_username == user_username).filter(schemas.Post.date_created > from_date).all()


def get_post(db: Session, post_id: int):
    return db.query(schemas.Post).filter(schemas.Post.id == post_id).first()


# user_id is the id of the user whose following we want to get the posts of
def get_following_posts(db: Session, user_username: str):
    user_in = get_by_username(db, user_username)
    following = get_following(db, user_in)
    posts = []
    for follower in following:
        posts_users = get_user_posts(db, user_username=follower.username)
        for post in posts_users:
            posts.append(post)
    return posts


def create_post(db: Session, post_in: models.Post) -> schemas.Post:
    db_post = schemas.Post(content=post_in.content,
                           user_username=post_in.user_username)
    db.add(db_post)
    db.commit()
    return db_post


def shared_post(db: Session, post_in: models.Post) -> schemas.Post:
    db_post = schemas.Post(content=post_in.content,
                           user_username=post_in.user_username, date_created=post_in.date_created)
    db.add(db_post)
    db.commit()
    return db_post


def delete_post(db: Session, post_id: int):
    post_to_delete = get_post(db, post_id)
    if post_to_delete is None:
        return None
    db.delete(post_to_delete)
    db.commit()
    return post_to_delete


def delete_user(db: Session, username: str):
    user_to_delete = get_by_username(db, username)
    if user_to_delete is None:
        return None
    db.delete(user_to_delete)
    db.commit()
    return user_to_delete


def login(db: Session, user_in: models.UserCreate):
    # Must have gone (outside this function) to the cloud to check if there is such a user in the online db
    user = get_by_username(db, user_in.username)
    if user is None:
        return create_user(db=db, user_in=user_in, is_active=True)

    if user.password == user_in.password:
        user.is_active = True
        db.commit()
        return user
    return None


def logout(db: Session, user_in: models.User):
    user = get_by_username(db, user_in.username)
    if user is None:
        return None
    user.is_active = False
    db.commit()
    return user

def user_status(db: Session, user_in: models.User):
    user = get_by_username(db, user_in.username)
    if user is None:
        return None
    user.is_active = user_in.is_active
    db.commit()
    return user

def start_follow(db: Session, follow: models.Follow):
    print("I'm in start_follow")
    new_follow = schemas.Followers(
        follower_username=follow.follower_username, following_username=follow.following_username)
    db.add(new_follow)
    db.commit()
    return new_follow


def get_follow(db: Session, follow_in: models.Follow):
    follow = db.query(schemas.Followers).filter(schemas.Followers.follower_username == follow_in.follower_username).filter(
        schemas.Followers.following_username == follow_in.following_username).first()
    return follow


def unfollow(db: Session, follow_in: models.Follow):
    follow = get_follow(db, follow_in)
    if follow is None:
        return None
    db.delete(follow)
    db.commit()
    return follow


def get_followers(db: Session, user_in: models.User):
    followers = db.query(schemas.Followers).filter(
        schemas.Followers.following_username == user_in.username).all()
    users = []
    for follower in followers:
        users.append(get_by_username(
            db=db, username=follower.follower_username))
    return users


def get_following(db: Session, user_in: models.User):
    following = db.query(schemas.Followers).filter(
        schemas.Followers.follower_username == user_in.username).all()
    users = []
    for follower in following:
        users.append(get_by_username(
            db=db, username=follower.following_username))
    return users


def get_latest_post(db: Session, user_username: str) -> schemas.Post:
    all_posts = db.query(schemas.Post).filter(
        schemas.Post.user_username == user_username)
    if all_posts.count() > 0:
        latest_post = all_posts.order_by(
            schemas.Post.date_created.desc()).first()
    else:
        latest_post = None
    return latest_post
