<template>
    <div class="card text-start" style="margin: 10px;margin-right: 0px;margin-left: 0px;">
        <div class="card-body">
            <div class="row">
                <div class="col-md-6" style="height: auto;max-height: 50px;">
                    <h4 style="margin: 0px;height: 30px;">@{{user_username}}</h4>
                </div>
                <div class="col">
                    <h6 style="text-align: right;height: 30px;">⌛{{dateFormatted}}</h6>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12" style="height: auto;max-height: 50px;">
                    <p>{{content}}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="js">
import { defineComponent } from 'vue'

export default defineComponent({
    name: "Message",

    props: {
        id: Number,
        user_username: String,
        date_created: String,
        content: String
    },
    computed: {
        dateFormatted() {
            return this.date_created.split('.')[0].replace('T',' ');
        }
    },
})
</script>