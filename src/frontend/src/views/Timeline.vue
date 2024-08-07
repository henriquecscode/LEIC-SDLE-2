<template>
    <body style="height: 700px; display: block; width: 100%;">
        <nav class="navbar navbar-light navbar-expand-md py-3"
            style="background: var(--bs-gray-dark);color: rgb(255,255,255);">
            <div class="container">
                <a class="navbar-brand d-flex align-items-center" @click="goHome()">
                    <span
                        class="bs-icon-sm bs-icon-rounded bs-icon-primary d-flex justify-content-center align-items-center me-2 bs-icon"
                        style="background: #9585ff;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor"
                            viewBox="0 0 16 16" class="bi bi-bezier">
                            <path fill-rule="evenodd"
                                d="M0 10.5A1.5 1.5 0 0 1 1.5 9h1A1.5 1.5 0 0 1 4 10.5v1A1.5 1.5 0 0 1 2.5 13h-1A1.5 1.5 0 0 1 0 11.5v-1zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1zm10.5.5A1.5 1.5 0 0 1 13.5 9h1a1.5 1.5 0 0 1 1.5 1.5v1a1.5 1.5 0 0 1-1.5 1.5h-1a1.5 1.5 0 0 1-1.5-1.5v-1zm1.5-.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1zM6 4.5A1.5 1.5 0 0 1 7.5 3h1A1.5 1.5 0 0 1 10 4.5v1A1.5 1.5 0 0 1 8.5 7h-1A1.5 1.5 0 0 1 6 5.5v-1zM7.5 4a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1z">
                            </path>
                            <path
                                d="M6 4.5H1.866a1 1 0 1 0 0 1h2.668A6.517 6.517 0 0 0 1.814 9H2.5c.123 0 .244.015.358.043a5.517 5.517 0 0 1 3.185-3.185A1.503 1.503 0 0 1 6 5.5v-1zm3.957 1.358A1.5 1.5 0 0 0 10 5.5v-1h4.134a1 1 0 1 1 0 1h-2.668a6.517 6.517 0 0 1 2.72 3.5H13.5c-.123 0-.243.015-.358.043a5.517 5.517 0 0 0-3.185-3.185z">
                            </path>
                        </svg>
                    </span>
                    <span style="font-family: Armata, sans-serif;color: rgba(255,255,255,0.9);">Peerly</span>
                </a>
                <span
                    style="font-family: Armata, sans-serif;color: rgba(255,255,255,0.9); margin-left: 10px;">{{this.$route.params.user}}</span>
                <div class="collapse navbar-collapse text-center d-md-flex justify-content-md-end" id="navcol-2">
                    <button class="btn btn-primary" type="button" @click="logout">Logout</button>
                </div>
            </div>
        </nav>
        <div class="container">
            <div class="row">
                <div class="col-md-9">
                    <div style="margin-top: 15px;">
                        <input type="text" v-on:keyup.enter="createPost" v-model="postInput"
                            style="width: 100%;padding: 10px;padding-top: 5px;resize: none;border-style: solid;border-color: rgba(33,37,41,0.24);border-radius: 6px;"
                            placeholder="What's happening?" />
                        <!-- <button @click="createPost" type="button">📨</button> -->
                    </div>

                    <div style="text-align: center;font-family: Armata, sans-serif;margin: 0px;"
                        v-if="posts.length != 0">
                        <Message v-for="message in posts" :id="message.id" :user_username="message.user_username"
                            :date_created="message.date_created" :content="message.content" />
                    </div>

                    <div style="text-align: center;font-family: Armata, sans-serif;margin-top: 20px;" v-else>
                        No messages to show... maybe wait a little?
                    </div>
                </div>
                <div class="col-md-3">
                    <div>
                        <div class="row">
                            <div class="col">
                                <div class="row" style="font-family: Armata, sans-serif;">
                                    <div class="col" style="margin-top: 15px;">
                                        <h5>Users</h5>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <input type="text" v-on:keyup.enter="search" v-model="inputFollow"
                            style="width: 100%;padding: 10px; margin-bottom: 15px; padding-top: 5px;resize: none;border-style: solid;border-color: rgba(33,37,41,0.24);border-radius: 6px;" />


                        <div v-if="(following.length != 0)" class="row" style="margin-bottom: 5px;" v-for="user in following">
                                <div class="col" style="font-family: Armata, sans-serif;">
                                    <h6 v-if="user.is_active" style="margin-bottom: 0px; display: flex; align-content: center; justify-content: flex-start; align-items: center;">
                                        🟢 {{ user.username }}

                                        <button v-if="notFollowing(user)" class="btn btn-primary" type="button"
                                            style="margin-left: 5px;" @click="follow(user.username)">🤝</button>
                                        <button v-else class="btn btn-primary" type="button" style="margin-left: 5px;"
                                            @click="unfollow(user.username)">💔</button>
                                    </h6>
                                    <h6 v-else style="margin-bottom: 0px; display: flex;">
                                        🔴 {{ user.username }}

                                        <button v-if="notFollowing(user)" class="btn btn-primary" type="button"
                                            style="margin-left: 5px;" @click="follow(user.username)">🤝</button>
                                        <button v-else class="btn btn-primary" type="button" style="margin-left: 5px;"
                                            @click="unfollow(user.username)">💔</button>
                                    </h6>
                                </div>
                            </div>
                            <div class="row" style="margin-bottom: 5px;" v-for="user in users">
                                <div v-if="(following.indexOf(user) == -1)" class="col" style="font-family: Armata, sans-serif;">
                                    <h6 style="margin-bottom: 0px; display: flex; align-content: center; justify-content: flex-start; align-items: center;">
                                        {{user.username}}

                                        <button v-if="notFollowing(user)" class="btn btn-primary" type="button"
                                            style="margin-left: 5px;" @click="follow(user.username)">🤝</button>
                                        <button v-else class="btn btn-primary" type="button" style="margin-left: 5px;"
                                            @click="unfollow(user.username)">💔</button>
                                    </h6>
                                </div>
                            </div>
                        <p v-if="(following.length == 0)">No users to show.</p>

                    </div>
                </div>
            </div>
        </div>
    </body>
</template>

<script lang="js">
    import axios from 'axios';
    import { defineComponent } from 'vue';
    import Message from '../components/Message.vue';
    import router from '../router';

    export default defineComponent({
        name: 'Timeline',

        components: {
            Message,
        },

        props: {
            user: String,
            port: String
        },

        methods: {
            goHome() {
                this.logout();
            },
            async logout() {
                await axios.post("http://localhost:" + this.$route.params.port + "/logout", {
                    "username": this.$route.params.user,
                    "is_active": false
                }).then((response) => {
                    console.log(response);
                    window.location.href = "http://localhost:5173";
                    //router.push({ name: 'Home' });
                })
                .catch((error) => {
                    console.log(error);
                });

            },

            async createPost() {
                console.log('CREATING POST');
                await axios.post("http://localhost:" + this.$route.params.port + "/create-post", {
                    "content": this.postInput,
                    "user_username": this.$route.params.user
                })
                    .then((response) => {
                        console.log(response);
                        this.posts.push(response.data);
                    })

                this.postInput = "";
            },

            async follow(userToFollow) {
                await axios.post("http://localhost:" + this.$route.params.port + "/start-follow", {
                    "follower_username": this.$route.params.user,
                    "following_username": userToFollow
                })
                    .then((response) => {
                        console.log(response);
                        var found = this.users.find((user) => {
                            return user.username == userToFollow;
                        });

                        this.following.push(found);
                        
                        this.users.splice(this.users.indexOf(found), 1);

                        this.$forceUpdate();
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },

            async unfollow(userToFollow) {
                await axios.post("http://localhost:" + this.$route.params.port + "/unfollow", {
                    "follower_username": this.$route.params.user,
                    "following_username": userToFollow
                })
                    .then((response) => {
                        console.log(response);
                        this.following.splice(this.following.indexOf(userToFollow), 1);
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },

            async search() {
                await axios.get("http://localhost:" + this.$route.params.port + "/search-user/" + this.inputFollow)
                    .then((response) => {
                        console.log(response);
                        if (response.data.username != this.$route.params.user) {
                            this.users.push(response.data);
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                    });

            },

            notFollowing(user) {
                return (this.following.indexOf(user) == -1);
            },

            async mutuals(potentialMutual) {
                this.followers = [];

                await axios.get("http://localhost:" + this.$route.params.port + "/get-followers/" + this.$route.params.user).then((response) => {
                    for (var i = 0; i < response.data.length; i++) {
                        this.followers.push(response.data[i]);
                    }
                });

                var i, j;

                for (var k = 0; k < this.following.length; k++) {
                    if (this.following[k].username == potentialMutual.username) {
                        i = k;
                    }
                }

                for (var k = 0; k < this.followers.length; k++) {
                    if (this.followers[k].username == potentialMutual.username) {
                        j = k;
                    }
                }

                console.log(j, k);
                return (j == k);
            }
        },

        data() {
            return {
                inputFollow: '',
                posts: [],
                users: [],
                creation: new Date(),
                following: [],
                followers: [],
                inputFollow: "",
                postInput: ""
            };
        },

        async created() {
            let url = "http://localhost:" + this.$route.params.port + "/update-feed";
            let evtSrc = new EventSource(url);
            evtSrc.onmessage = (e) => {
                var data = JSON.parse(e.data)
                if ('posts' in data) {
                    var posts = data.posts;
                    for (var p in posts) {
                        this.posts.push(posts[p]);
                    }
                }
                if ('status' in data) {
                    console.log(data.status);
                    var users = data.status;
                    console.log(users)
                    console.log('this users before', this.following);
                    for (var u in users) {
                        let index = this.following.findIndex((user) => { return user.username == users[u].username });
                        if (index != -1) {
                            this.following[index] = users[u];
                        }
                    }
                    console.log('this users after', this.following);
                }
            }

            evtSrc.onerror = (e) => { console.error(e) };

            await axios.get("http://localhost:" + this.$route.params.port + "/get-following/" + this.$route.params.user).then((response) => {
                for (var i = 0; i < response.data.length; i++) {
                    this.following.push(response.data[i]);
                }
            });

            await axios.get("http://localhost:" + this.$route.params.port + "/user-posts/" + this.$route.params.user).then((response) => {
                for (var i = 0; i < response.data.length; i++) {
                    this.posts.push(response.data[i]);
                }
            });

            await axios.get("http://localhost:" + this.$route.params.port + "/following-posts/" + this.$route.params.user).then((response) => {
                for (var i = 0; i < response.data.length; i++) {
                    this.posts.push(response.data[i]);
                }
            });

            this.posts.sort((a, b) => {
                return new Date(b.date_created) - new Date(a.date_created);
            });
        }
    });
</script>