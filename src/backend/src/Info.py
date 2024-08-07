INFO_SPLITTER = ';'
USER_SPLITTER = '\t'


class Info:

    def __init__(self, username, password, ip, port, followers, following, is_online):
        self.username = username
        self.password = password
        self.ip = ip
        self.port = int(port)
        self.followers = set(followers)
        self.following = set(following)
        self.is_online = is_online

    @classmethod
    def deserialize(cls, string):
        string = string.split(INFO_SPLITTER)
        username = string[0]
        password = string[1]
        ip = string[2]
        port = int(string[3])
        followers = string[4].split(USER_SPLITTER) if string[4] else []
        following = string[5].split(USER_SPLITTER) if string[5] else []
        if string[6] == 'True':
            is_online = True
        else:
            is_online = False
        return cls(username, password, ip, port, followers, following, is_online)

    def serialize(self):
        return INFO_SPLITTER.join([self.username, self.password, self.ip, str(self.port), USER_SPLITTER.join(self.followers), USER_SPLITTER.join(self.following), str(self.is_online)])

    def __str__(self):
        return self.serialize()

    def add_follower(self, username):
        self.followers.add(username)
        return self

    def remove_follower(self, username):
        self.followers.remove(username)
        return self

    def add_following(self, username):
        self.following.add(username)
        return self

    def remove_following(self, username):
        self.following.remove(username)
        return self

    def set_online(self):
        self.is_online = True
        return self

    def set_offline(self):
        self.is_online = False
        return self

    def get_online(self):
        return self.is_online
    
    
