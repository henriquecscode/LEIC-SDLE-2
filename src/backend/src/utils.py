import requests
import sys
import json
import datetime

port = 8000


def get_port():
    db_suffix = port + int(sys.argv[1])
    return db_suffix


def start_utils(id):
    global port
    port = port + id
    print("Starting utils on port: ", port)


def login(username, password):
    url = "http://localhost:" + str(port) + "/login"
    user_in = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=user_in)
    return response


def logout(username):
    url = "http://localhost:" + str(port) + "/logout"
    user_in = {
        "username": username
    }
    requests.post(url, json=user_in)

def user_status(username, status):
    url = "http://localhost:" + str(port) + "/user-status"
    user_in = {
        "username": username,
        "is_active": status
    }
    requests.post(url, json=user_in)

def get_user(username):
    url = "http://localhost:" + str(port) + "/user/" + username
    response = requests.get(url)
    return response


def create_user(username, password):
    is_active = True
    url = "http://localhost:" + str(port) + "/create-user/" + str(is_active)
    user_in = {
        "username": username,
        "password": password
    }

    requests.post(url, json=user_in)


def create_user_info(info):
    url = "http://localhost:" + \
        str(port) + "/create-user/" + str(info.is_online)
    user_in = {
        "username": info.username,
        "password": info.password
    }

    requests.post(url, json=user_in)


def create_post(username, post, date_created=None):
    url = "http://localhost:" + str(port) + "/create-post"
    post_in = {
        "content": post,
        "user_username": username,
    }

    if date_created is not None:
        post_in["date_created"] = date_created
    response = requests.post(url, json=post_in)
    return response


def shared_post(username, post, date_created):
    url = "http://localhost:" + str(port) + "/shared-post"
    post_in = {
        "content": post,
        "user_username": username,
        "date_created": date_created
    }
    response = requests.post(url, json=post_in)
    return response


def start_follow(follower_username, following_username):
    url = "http://localhost:" + str(port) + "/start-follow"
    follow_in = {
        "follower_username": follower_username,
        "following_username": following_username
    }
    requests.post(url, json=follow_in)


def create_follow(follower_username, following_username):
    url = "http://localhost:" + str(port) + "/create-follow"
    follow_in = {
        "follower_username": follower_username,
        "following_username": following_username
    }
    requests.post(url, json=follow_in)


def unfollow(follower_username, following_username):
    url = "http://localhost:" + str(port) + "/unfollow"
    follow_in = {
        "follower_username": follower_username,
        "following_username": following_username
    }
    requests.post(url, json=follow_in)


def get_followers(username):
    url = "http://localhost:" + str(port) + "/get-followers/" + username
    response = requests.get(url)
    return response


def get_following(username):
    url = "http://localhost:" + str(port) + "/get-following/" + username
    response = requests.get(url)
    return response


def get_latest_post(username):
    url = "http://localhost:" + str(port) + "/latest-post/" + username
    response = requests.get(url)
    if response.status_code == 204:
        return None
    return json.loads(response.content)


def get_posts_from(username, date_created=datetime.datetime(1970, 1, 1, 0, 0, 0, 0)):
    date_created = date_created.isoformat()
    url = "http://localhost:" + str(port) + "/user-posts/"
    post_in = {
        "user_username": username,
        "date_created": date_created,
        "content": ""
    }
    response = requests.post(url, json=post_in)
    return response


def check_delete_posts():
    print(f"Checking for outdated posts at {datetime.datetime.now()}")
    url = "http://localhost:" + str(port) + "/outdated-posts"
    requests.delete(url)
