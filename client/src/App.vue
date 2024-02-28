<template>
  <Header />
  <LeftBar />
  <div id="content" data-uk-height-viewport="expand: true">
    <div class="uk-container uk-container-expand">
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped></style>

<script>
import { version } from "../package.json";
import UIkit from "uikit";
import Icons from 'uikit/dist/js/uikit-icons';

// Icons
UIkit.use(Icons);

// Components
import Header from "@/components/Header.vue";
import LeftBar from "@/components/LeftBar.vue";

import { io } from "socket.io-client";

export default {
  components: {
    Header,
    LeftBar,
  },
  data() {
    return {
      socket: null,
    };
  },
  mounted() {
    console.log("Ver:", version);
    
    this.socket = io();

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    this.socket.on("connect", () => {
      this.socket.emit("connection", { data: "Client connected!" });
    });

    // Set log window
    this.socket.on("status_log", (msg, cb) => {
      console.log(msg.data);
    });

    this.socket.on("error", (msg, cb) => {
      console.log(msg.data);
    });
  },
};
</script>