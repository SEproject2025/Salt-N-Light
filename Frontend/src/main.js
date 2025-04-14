import { createApp } from "vue";
import App from "./App.vue";
import router from "./router/router";
import "./assets/tailwind.css";
import "./assets/styles.css"; //IMport global style
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faEdit,
  faTimes,
  faThumbsUp,
  faThumbsDown,
  faSave,
} from "@fortawesome/free-solid-svg-icons";

// Add the icons to the library
library.add(faEdit, faTimes, faThumbsUp, faThumbsDown, faSave);

const app = createApp(App);

app.use(router);

// Register the FontAwesomeIcon component globally
app.component("font-awesome-icon", FontAwesomeIcon);

app.mount("#app");
