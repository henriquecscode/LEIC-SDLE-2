import json
import datetime
import schemas
import models


class MessageDecodeError(Exception):
    pass


class Message:
    def __init__(self, m_type, payload):
        self.m_type = m_type
        self.payload = payload
        self.message = {
            "m_type": m_type,
            "payload": payload
        }
        for (k, v) in self.payload.items():
            setattr(self, k, v)
        print('message created', self)

    @classmethod
    def deserialize(cls, message):
        message = json.loads(message)
        m_type = message['m_type']
        payload = message['payload']
        if m_type == 'logout':
            return Logout.deserialize(payload)
        elif m_type == 'follow':
            return Follow.deserialize(payload)
        elif m_type == 'unfollow':
            return Unfollow.deserialize(payload)
        elif m_type == 'get_feed':
            return GetFeed.deserialize(payload)
        elif m_type == 'share_feed':
            return ShareFeed.deserialize(payload)
        elif m_type == 'get_followers':
            return GetFollowers.deserialize(payload)
        elif m_type == 'get_following':
            return GetFollowing.deserialize(payload)
        elif m_type == 'share_followers':
            return ShareFollowers.deserialize(payload)
        elif m_type == 'share_following':
            return ShareFollowing.deserialize(payload)
        elif m_type == 'following_online':
            return FollowingOnline.deserialize(payload)
        elif m_type == 'follower_online':
            return FollowerOnline.deserialize(payload)
        elif m_type == 'mutual_follower_online':
            return MutualFollowerOnline.deserialize(payload)
        elif m_type == 'get_posts':
            return GetPosts.deserialize(payload)
        else:
            raise MessageDecodeError

    def serialize(self):
        return json.dumps(self.message)

    def __call__(self):
        return self.serialize()

class Logout(Message):
    def __init__(self, username):
        self.username = username
        payload = {
            "username": username
        }
        super().__init__('logout', payload)

    @classmethod
    def deserialize(cls, payload):
        username = payload['username']
        return cls(username)

class Follow(Message):
    def __init__(self, follow, follow_password, following):
        print("trying to create Follow", follow, following)
        self.follow = follow
        self.follow_password = follow_password
        self.following = following
        payload = {
            "follow": follow,
            "follow_password": follow_password,
            "following": following
        }
        super().__init__('follow', payload)

    @classmethod
    def deserialize(cls, payload):
        print("deserializing follow inside follow class")
        follow = payload['follow']
        follow_password = payload['follow_password']
        following = payload['following']
        return cls(follow, follow_password, following)


class Unfollow(Message):
    def __init__(self, unfollow, unfollowing):
        self.unfollow = unfollow
        self.unfollowing = unfollowing
        payload = {
            "unfollow": unfollow,
            "unfollowing": unfollowing
        }

        super().__init__('unfollow', payload)

    @classmethod
    def deserialize(cls, payload):
        unfollow = payload['unfollow']
        unfollowing = payload['unfollowing']
        return cls(unfollow, unfollowing)


class GetFeed(Message):
    def __init__(self, user, offset=0, amount=-1):
        payload = {
            "user": user,
            "offset": 0,
            "amount": -1
        }
        super().__init__('get_feed', payload)

    @classmethod
    def deserialize(cls, payload):
        user = payload['user']
        offset = payload['offset'] if 'offset' in payload else 0
        amount = payload['amount'] if 'amount' in payload else -1
        return cls(user, offset, amount)


class ShareFeed(Message):
    def __init__(self, user, posts, is_serialized=False):
        user = user
        if not is_serialized:
            posts = [get_serialized_post(post) for post in posts]
        else:
            posts = posts
        payload = {
            "user": user,
            "posts": posts
        }
        super().__init__('share_feed', payload)

    @classmethod
    def deserialize(cls, payload):
        user = payload['user']
        posts = payload['posts']
        return cls(user, posts, is_serialized=True)


class GetFollowers(Message):
    def __init__(self, following):
        payload = {
            "following": following
        }
        super().__init__('get_followers', payload)

    @classmethod
    def deserialize(cls, payload):
        following = payload['following']
        return cls(following)


class GetFollowing(Message):
    def __init__(self, follower):
        payload = {
            "follower": follower
        }
        super().__init__('get_following', payload)

    @classmethod
    def deserialize(cls, payload):
        follower = payload['follower']
        return cls(follower)


class ShareFollowers(Message):
    def __init__(self, followers):
        payload = {
            "followers": followers
        }
        super().__init__('share_followers', payload)

    @classmethod
    def deserialize(cls, payload):
        followers = payload['followers']
        return cls(followers)


class ShareFollowing(Message):
    def __init__(self, following):
        payload = {
            "following": following
        }
        super().__init__('share_following', payload)

    @classmethod
    def deserialize(cls, payload):
        following = payload['following']
        return cls(following)


class FollowingOnline(Message):
    def __init__(self, following, last_date=datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()):
        payload = {
            "following": following,
            "last_date": last_date
        }
        super().__init__('following_online', payload)

    @classmethod
    def deserialize(cls, payload):
        following = payload['following']
        last_date = payload['last_date']
        return cls(following, last_date)


class FollowerOnline(Message):
    def __init__(self, follower, last_date=datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()):
        payload = {
            "follower": follower,
            "last_date": last_date
        }
        super().__init__('follower_online', payload)

    @classmethod
    def deserialize(cls, payload):
        follower = payload['follower']
        last_date = payload['last_date']
        return cls(follower, last_date)


class MutualFollowerOnline(Message):
    def __init__(self, follower, following, last_date=datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()):
        payload = {
            "follower": follower,
            "following": following,
            "last_date": last_date
        }
        super().__init__('mutual_follower_online', payload)

    @classmethod
    def deserialize(cls, payload):
        follower = payload['follower']
        following = payload['following']
        last_date = payload['last_date']
        return cls(follower, following, last_date)


class GetPosts(Message):
    def __init__(self, asker, owner, from_date=datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()):
        payload = {
            "asker": asker,
            "owner": owner,
            "from_date": from_date
        }
        super().__init__('get_posts', payload)

    @classmethod
    def deserialize(cls, payload):
        asker = payload['asker']
        owner = payload['owner']
        from_date = payload['from_date']
        return cls(asker, owner, from_date)


def get_serialized_post(post: schemas.Post):
    return {
        'user_username': post.user_username,
        'content': post.content,
        'date_created': post.date_created.isoformat()
    }


def get_unserialized_post(post: dict) -> schemas.Post:
    post = schemas.Post(
        content=post['content'],
        user_username=post['user_username'],
        date_created=datetime.datetime.fromisoformat(post['date_created'])
    )
    return post
