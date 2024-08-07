<template>

    <body style="height: 700px; display: block; width: 100%;">
        <nav class="navbar navbar-light navbar-expand-md py-3"
            style="background: var(--bs-gray-dark);color: rgb(255,255,255);">
            <div class="container">
                <a class="navbar-brand d-flex align-items-center" href="#">
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
                    <span style="font-family: Armata, sans-serif;color: rgba(255,255,255,0.9);">
                        Peerly
                    </span>
                </a>
                <div class="collapse navbar-collapse text-center d-md-flex justify-content-md-end" id="navcol-2">
                    <button class="btn btn-primary" type="button" data-bs-target="#auth-modal" data-bs-toggle="modal">
                        Login
                    </button>
                </div>
            </div>
        </nav>
        <div class="modal fade" role="dialog" tabindex="-1" id="auth-modal">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-body" style="font-family: Armata, sans-serif;">
                        <div class="d-md-flex justify-content-md-center align-items-md-center">
                            <h4 class="modal-title d-md-flex flex-row justify-content-md-center align-items-md-center"
                                style="text-align: center;">
                                Login
                            </h4>
                        </div>
                        <div class="mb-3" style="text-align: left;">
                            <label class="form-label" style="text-align: left;">
                                Username
                                <span style="color: rgb(255, 0, 0);">
                                    *
                                </span>
                            </label>
                            <input class="form-control" type="text" id="username" placeholder="Username" />
                        </div>
                        <div class="mb-3" style="text-align: left;">
                            <label class="form-label" style="text-align: left;">
                                Password
                                <span style="color: rgb(255, 0, 0);">*</span>
                            </label>
                            <input class="form-control" type="password" id="password" name="password"
                                placeholder="Password" />
                        </div>
                        <div class="mb-3" style="text-align: left;">
                            <label class="form-label" style="text-align: left;">
                                Port
                                <span style="color: rgb(255, 0, 0);">*</span>
                            </label>
                            <input class="form-control" type="number" id="port" name="port"
                                placeholder="8000" />
                        </div>
                        <div class="mb-3">
                            <button class="btn btn-primary d-block w-100" type="submit" @click="login" data-bs-dismiss="modal">
                                Login
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="text-align: center;font-family: Armata, sans-serif;margin: 30px;">
            <h1>We don't like peer pressure.</h1>
            <h1>Unless you like it, then it's cool.</h1>
        </div>

    </body>
</template>

<script lang="js">
import axios from 'axios';
import { defineComponent } from 'vue';
import router from '../router';

export default defineComponent({
    name: 'Home',
    methods: {
        async login() {
            var username = document.getElementById('username').value;
            var password = document.getElementById('password').value;
            var port = document.getElementById('port').value;

            var data = {
                username: username,
                password: password
            };

            var url = 'http://localhost:' + port + '/login';
            await axios.post(url, data)
            .then((response) => {
                console.log(response);
                console.log(username);

                router.push({ name: 'Timeline', params: { user: username, port: port } });
            }).catch((error) => {
                console.log(error);
            });
        }
    }
});

</script>