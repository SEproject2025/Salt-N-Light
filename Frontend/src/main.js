import { createApp } from "vue";
import App from "./App.vue";
import router from "./router/router";
import "./assets/styles.css"; //IMport global style
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import {
  faEdit,
  faTimes,
  faThumbsUp,
  faThumbsDown,
  faSave,
  faBookmark,
} from "@fortawesome/free-solid-svg-icons";
import { faBookmark as farBookmark } from "@fortawesome/free-regular-svg-icons";

// Add the icons to the library
library.add(
  faEdit,
  faTimes,
  faThumbsUp,
  faThumbsDown,
  faSave,
  faBookmark,
  farBookmark
);

const app = createApp(App);

app.use(router);

// Register the FontAwesomeIcon component globally
app.component("font-awesome-icon", FontAwesomeIcon);

app.mount("#app");
