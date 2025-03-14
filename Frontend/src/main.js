import { createApp } from "vue";
import App from "./App.vue";
import router from "./router/router";
import "./assets/styles.css"; //IMport global style
import { library } from "@fontawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fontawesome/vue-fontawesome";
import {
  faEdit,
  faTimes,
  faThumbsUp,
  faThumbsDown,
  faSave,
} from "@fontawesome/free-solid-svg-icons";

// Add the icons to the library
library.add(faEdit, faTimes, faThumbsUp, faThumbsDown, faSave);

const app = createApp(App);

app.use(router);

// Register the FontAwesomeIcon component globally
app.component("font-awesome-icon", FontAwesomeIcon);

app.mount("#app");
