from Node import Node
from Info import Info

import crud
import models
import schemas
import utils
from typing import List
import datetime

from Message import Logout, Follow, Unfollow, GetFeed, ShareFeed, GetFollowers, GetFollowing, ShareFollowers, ShareFollowing, FollowingOnline, FollowerOnline, MutualFollowerOnline, GetPosts

import asyncio
import sys
import threading
import time
import json
BASE_PORT = 8468
USERS_INFO_KEY = "\%"
TIMER = 1 * 60  # 1 minute


class Peer():
    def __init__(self, id):
        self.id = id
        utils.start_utils(id)
        self.node = Node(id, self)
        self.feed = []
        self.status = []


### LIFETIME ###

    def add_backend(self, backend):
        self.backend = backend

    def stop(self):
        self.node.stop()
        self.backend.stop()
        sys.exit(1)

#############

    def menu(self):
        while True:
            try:
                option = int(input(
                    "1. Follow\n2. Unfollow\n3. Get Feed\n4. Get Followers\n5. Get Following\n6.Make Post\n7. Exit\n8. GET INFO\n9. SET TEST\n10.GET TEST\n11.login\n12.logout\n"))
                break
            except:
                continue

        if option == 1:
            username = input("Enter username of user to follow: ")
            self.t_follow(username)
        elif option == 2:
            username = input("Enter username of user to unfollow: ")
            self.send_message(username, Unfollow(
                self.username, username).serialize())
        elif option == 3:
            username = input("Enter username of user to get feed: ")
            self.send_message(username, GetFeed(
                self.username, username).serialize())
        elif option == 4:
            username = input("Enter username of user to get followers: ")
            self.send_message(username, GetFollowers(
                self.username, username).serialize())
        elif option == 5:
            username = input("Enter username of user to get following: ")
            self.send_message(username, GetFollowing(
                self.username, username).serialize())
        elif option == 6:
            post = input("Enter post: ")
            self.t_create_post(post)
        elif option == 7:
            self.stop()
        elif option == 8:
            username = input("Enter username of user to get info: ")
            info = self.node[username]
            print("NETWORK WAS INFO", info)
        elif option == 9:
            data = input("Enter data to set: ")
            self.node['test'] = data
        elif option == 10:
            print("TEST WAS", self.node['test'])
        elif option == 11:
            name = input("Enter name of user to create: ")
            password = name
            utils.login(name, password)
        elif option == 12:
            name = input("Enter name of user to delete: ")
            utils.logout(name)

    def start(self):
        # utils.create_user(username, password)

        # Only while we don't have login working and connected with the frontend
        #self.backend.create_user(user_in = models.UserCreate(username=username, password=password, is_active=True))
        # crud.create_user(crud.get_db, models.UserCreate(username=username, password='password', is_active=True))
        threading.Thread(target=self.node.start).start()
        while True:
            self.menu()

    def send_message(self, id, message):
        self.node.send_message(id, message)



    def handler(self, message):

        print("HANDLING MESSAGE", message)

        try:
            if isinstance(message, Logout):
                self.handle_logout(message)
            elif isinstance(message, Follow):
                self.handle_follow(message)
            elif isinstance(message, Unfollow):
                self.handle_unfollow(message)
            elif isinstance(message, GetFeed):
                self.handle_get_feed(message)
            elif isinstance(message, ShareFeed):
                self.handle_share_feed(message)
            elif isinstance(message, GetFollowers):
                self.handle_get_followers(message)
            elif isinstance(message, GetFollowing):
                self.handle_get_following(message)
            elif isinstance(message, ShareFollowers):
                self.handle_share_followers(message)
            elif isinstance(message, ShareFollowing):
                self.handle_share_following(message)
            elif isinstance(message, FollowingOnline):
                self.handle_following_online(message)
            elif isinstance(message, FollowerOnline):
                self.handle_follower_online(message)
            elif isinstance(message, MutualFollowerOnline):
                self.handle_mutual_follower_online(message)
            elif isinstance(message, GetPosts):
                self.handle_get_posts(message)
            else:
                print("Unknown message")
                pass
        except Exception as e:
            print("ERROR HANDLING MESSAGE", e)
            pass

    def handle_logout(self, message: Logout):

        utils.user_status(message.username, False)
        self.add_to_status([{
            "username": message.username,
            "is_active": False
        }])
        
    def update_info_followers(self):
        online_info = self.node[self.username]
        online_followers = online_info.followers
        self.info.followers = online_followers

    def handle_follow(self, message: Follow):
        # DONT UPDATE KADEMLIA BUT UPDATE LOCALLY (KADEMLIA NEEDS TO BE ALREADY UPDATED IN B_START FOLLOW WHICH ALSO NEEDS TO BE CHANGED)
        print("In handle_follow:")
        if (message.following == self.username):

            # Update local info data
            self.update_info_followers()
            # Update local db
            self.follow(message.follow, message.follow_password,
                        message.following)
        else:
            print(
                f"User that sent the message wants to follow {message.following} but peer is {self.username}")

    def follow(self, follower, follower_password, following):
        # We are "following"
        has_user = json.loads(utils.get_user(follower).content)
        if has_user is None:
            utils.create_user(follower, follower_password)
        utils.create_follow(follower, self.username)

    def handle_unfollow(self, message: Unfollow):
        print("In handle_unfollow: ")
        if (message.unfollowing == self.username):
            # Update local info data
            self.update_info_followers()

            # Update local db
            self.unfollow(message.unfollow, message.unfollowing)
        else:
            print(
                f"User that sent the message wants to unfollow {message.unfollowing} but peer is {self.username}")

    def unfollow(self, unfollower, unfollowing):
        print("I'm in unfollow")
        utils.unfollow(unfollower, unfollowing)

    def handle_get_feed(self, message: GetFeed):
        if (message.user == self.username):
            self.get_feed(message.user)
        else:
            print(f"Subscribing to {message.user} but peer is {self.username}")

    def get_feed(self, user):
        pass

    def handle_share_feed(self, message: ShareFeed):
        print("In handle_share_feed: ")
        # We got a post shared from another user (the post might have not been from them)
        posts = message.posts
        print(f"post is {posts}")
        created_posts = []

        for post in posts:
            created_post = utils.shared_post(post['user_username'],
                                             post['content'], post['date_created'])
            created_post = json.loads(created_post.content)
            created_posts.append(created_post)

        # posts = [Message.get_unserialized_post(post) for post in posts]
        self.add_to_feed(created_posts)

        print(f"starting timer at {datetime.datetime.now()}")
        threading.Timer(TIMER, utils.check_delete_posts).start()

    def handle_get_followers(self, message: GetFollowers):
        if message.following == self.username:
            self.get_followers(message.following)
        else:
            print(
                "Getting followers of {message.user} but peer is {self.username}")

    def get_followers(self, following):
        pass

    def handle_get_following(self, message: GetFollowing):
        if message.follower == self.username:
            self.get_following(message.follower)
        else:
            print(
                "Getting following of {message.user} but peer is {self.username}")

    def get_following(self, follower):
        pass

    def handle_share_followers(self, message: ShareFollowers):
        self.share_followers(message.followers)

    def share_followers(self, followers):

        for follower in followers:
            model = models.Follow(
                follower_id=follower.follower_id, following_id=follower.following_id)

    def handle_share_following(self, message: ShareFollowing):
        self.share_following(message.following)

    def share_following(self, following):

        for follow in following:
            model = models.Follow(
                follower_id=follow.follower_id, following_id=follow.following_id)

    def handle_following_online(self, message: FollowingOnline):
        following = message.following
        most_recent_date = datetime.datetime.fromisoformat(message.last_date)

        post = utils.get_latest_post(following)
        if post is not None:
            post_date = datetime.datetime.fromisoformat(post['date_created'])
            if post_date < most_recent_date:
                self.send_message(following, GetPosts(
                    self.username, following, post_date.isoformat())())
        else:
            self.send_message(following, GetPosts(self.username, following)())

        utils.user_status(following, True)
        self.add_to_status([{
            'username': following,
            'is_active': True,
        }])

    def handle_follower_online(self, message: FollowerOnline):
        most_recent_date = datetime.datetime.fromisoformat(
            message.last_date) if message.last_date != "" else None

        post = utils.get_latest_post(self.username)
        if post is not None:
            post_date = datetime.datetime.fromisoformat(post['date_created'])
            posts = []
            if most_recent_date is None:
                posts = json.loads(utils.get_posts_from(self.username).content)
            elif most_recent_date < post_date:
                posts = json.loads(utils.get_posts_from(
                    self.username, most_recent_date).content)

            if posts is []:
                return
            else:
                self.send_message(message.follower,
                                  ShareFeed(self.username, posts, True)())

        utils.user_status(message.follower, True)
        self.add_to_status([{
            'username': message.follower,
            'is_active': True
        }])

    def handle_mutual_follower_online(self, message: MutualFollowerOnline):
        following = message.following
        most_recent_date = datetime.datetime.fromisoformat(
            message.last_date) if message.last_date != "" else None

        post = utils.get_latest_post(following)
        if post is not None:
            post_date = datetime.datetime.fromisoformat(post['date_created'])
            posts = []
            if most_recent_date is None:
                posts = json.loads(utils.get_posts_from(following).content)
            elif most_recent_date < post_date:
                posts = json.loads(utils.get_posts_from(
                    following, most_recent_date).content)

            if posts is []:
                return
            else:
                self.send_message(message.follower, ShareFeed(
                    following, posts, True)())

    def handle_get_posts(self, message: GetPosts):
        asker = message.asker
        owner = message.owner
        from_date = datetime.datetime.fromisoformat(message.from_date)

        posts = json.loads(utils.get_posts_from(owner, from_date).content)
        if posts is []:
            return
        else:
            self.send_message(asker, ShareFeed(owner, posts, True)())

### TESTING THROUGH CONSOLE ###
    def t_create_post(self, post: str):
        utils.create_post(self.username, post)

    def t_follow(self, following: str):
        utils.start_follow(self.username, following)

### REAL TIME FEED ###

    def has_new_feed(self):
        return self.feed != []

    def add_to_feed(self, posts):
        print("In add_to_feed")
        self.feed.extend(posts)

    def get_new_feed(self) -> List[models.Post]:
        feed = [post for post in self.feed]
        self.feed = []
        return feed

    def has_new_status(self):
        return self.status != []

    def add_to_status(self, usernames):
        self.status.extend(usernames)

    def get_new_status(self) -> List[str]:
        status = [user for user in self.status]
        self.status = []
        return status


### INVOKED BY BACKEND ###

    def b_login(self, username, password, db):

        info = self.node[username]
        if info is None:
            # No such user found in network
            print("No such user found in network")
            return (False, True)

        if username == info.username and password != info.password:
            print("Wrong password")
            return (True, False)

        # User exists in network and has this password
        print("User exists in network and has this password ", username)
        self.username = username
        self.password = password
        self.info = info.set_online()
        self.node.set_info()
        # following and followers

        print("Updating followers and following")
        followers = json.loads(utils.get_followers(
            self.username).content)  # gets people you follow
        follower_set = set(
            map(lambda model_user: model_user['username'], followers))

        to_remove_dif = follower_set - set(self.info.followers)
        to_add_dif = set(self.info.followers) - follower_set

        for follower in to_remove_dif:
            self.unfollow(follower, self.username)

        for follower in to_add_dif:
            follower_info = self.node[follower]
            has_user = json.loads(utils.get_user(
                follower_info.username).content)
            if has_user is None:
                utils.create_user_info(follower_info)
            utils.create_follow(follower_info.username, self.username)

        following = json.loads(utils.get_following(
            self.username).content)  # gets people following you
        following_set = set(
            map(lambda model_user: model_user['username'], following))

        to_remove_dif = following_set - set(self.info.following)
        to_add_dif = set(self.info.following) - following_set

        for following in to_remove_dif:
            self.unfollow(self.username, following)

        for following in to_add_dif:
            following_info = self.node[following]
            has_user = json.loads(utils.get_user(following.username).content)
            if has_user is None:
                utils.create_user_info(following_info)
            utils.create_follow(self.username, following_info.username)

        self.update_with_followers(db)

        self.update_with_following(db)

        #  first step: go get followers and following from db
        # second step assemble into a set
        # third step calculate the differences in both directions
        # fourth step from the differences get who we need to create and follows that we need to delete
        # fifth step delete
        # sixth step for the ones we have to create go fetch their info (and their password)
        # seventh step, after getting password, call self.follow()

        # TODO COMPARE FOLLOWERS (MIGHT HAVE BEEN UPDATE WHILE WE WERE OFFLINE)
        return (True, True)

    def b_create_user(self, username, password):
        self.info = Info(username, password, self.node.host,
                         self.node.node_port, [], [], True)
        self.node[username] = self.info
        print("Added user to network", username)
        self.username = username
        self.password = password

    def b_logout(self):
        # Still need to inform the followers that you are logging out

        self.info.set_offline()

        print(self.username)
        print("Logged out ", self.info)
        self.node[self.username] = self.info
        
        for follower in self.info.followers:
            self.send_message(follower, Logout(self.username)())
        for following in self.info.following:
            self.send_message(following, Logout(self.username)())


        self.username = None
        self.password = None
        self.info = None

    def b_create_post(self, post: models.Post):
        # After the creation of a post we should
        # 1: Display it in our feed
        # 2: Share it with our followers --> first we need to get followers

        #user = models.User(username=self.username, is_active=True)
        #followers = crud.get_followers(db, user)
        followers = self.info.followers
        # followers_info = [self.node[follower] for follower in self.info.followers]

        message = ShareFeed(self.username, [post])()
        for follower in followers:
            self.send_message(follower, message)
        # utils.create_post(self.username, post)

    def b_start_follow(self, follow: models.Follow):
        # Update kademlia

        following = follow.following_username  # user we want to start to follow
        _, following_info = self.node.add_follow(
            self.username, following)  # updates kademlia
        if following_info is not None:
            is_online = following_info.get_online()
            if is_online:
                self.node.send_message_from_info(following_info, Follow(
                    self.username, self.info.password, following)())
        else:
            print("Following info is none in Peer's b_start_follow")

    def b_search_follow(self, username, db):
        # Search for a user in the network
        # If found, return the info
        # If not found, return None
        user = self.node[username]
        print('GOT USER FROM KADEMLIA', user)
        if user is not None:
            print("User found in network")
            db_user = json.loads(utils.get_user(user.username).content)
            if db_user is None:
                user_in = models.UserCreate(
                    username=user.username, password=user.password)
                user = crud.create_user(db, user_in, is_active=user.is_online)
            else:
                user = db_user
            return user
        return None

    def b_unfollow(self, follow: models.Follow):
        # Update kademlia
        # We are "follower"
        following = follow.following_username
        _, following_info = self.node.remove_follow(
            self.username, following)
        if following_info is not None:
            is_online = following_info.get_online()
            if is_online:
                self.node.send_message_from_info(following_info, Unfollow(
                    self.username, following)())
        else:
            print("Following info is none in Peer's b_unfollow")

    def update_with_followers(self, db):  # people who follow the user
        followers = self.info.followers

        # get my latest
        # last_create_date = crud.get
        latest_post = crud.get_latest_post(db, self.username)
        last_date_created = latest_post.date_created.isoformat(
        ) if latest_post is not None else None

        for follower in followers:
            follower_info = self.node[follower]
            if follower_info.is_online:
                if last_date_created is not None:
                    self.node.send_message_from_info(
                        follower_info, FollowingOnline(self.username, last_date_created)())
                else:
                    self.node.send_message_from_info(
                        follower_info, FollowingOnline(self.username)())

    def update_with_following(self, db):  # people that the user follows
        following = self.info.following
        # get latest
        # last_created_date = crud.get]
        for following in following:
            latest_post = crud.get_latest_post(db, following)
            last_date_created = latest_post.date_created.isoformat(
            ) if latest_post is not None else None
            following_info = self.node[following]
            if following_info.is_online:
                if last_date_created is not None:
                    self.node.send_message_from_info(
                        following_info, FollowerOnline(self.username, last_date_created)())
                else:
                    self.node.send_message_from_info(
                        following_info, FollowerOnline(self.username)())
            else:
                for follower in following_info.followers:
                    if follower == self.username:
                        continue

                    follower_info = self.node[follower]
                    if follower_info.is_online:
                        if last_date_created is not None:
                            self.node.send_message_from_info(follower_info, MutualFollowerOnline(
                                self.username, following, last_date_created)())
                        else:
                            self.node.send_message_from_info(
                                follower_info, MutualFollowerOnline(self.username, following)())
                    else:
                        # Can't do anything to update. They and everyone who follows them are offline
                        return
