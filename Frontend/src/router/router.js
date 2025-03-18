import { createRouter, createWebHistory } from "vue-router";
import { jwtDecode } from "jwt-decode"; // Correct import
import AppLogin from "@/pages/AppLogin.vue";
import UserProfile from "@/pages/UserProfile.vue";
import LandingPage from "@/pages/LandingPage.vue";
import SearchPage from "@/pages/SearchPage.vue";
import MatchmakingPage from "@/pages/MatchmakingPage.vue";
import RegistrationPage from "@/pages/RegistrationPage.vue";
import PublicProfile from "@/pages/PublicProfile.vue";
import axios from "axios"; // Needed for refreshing tokens

async function isAuthenticated() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    return false; // No token means not authenticated
  }

  try {
    const decodedToken = jwtDecode(token);
    const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds

    // If the token is expired, try refreshing it
    if (decodedToken.exp < currentTime) {
      return await refreshAccessToken();
    }

    return true; // Token is valid
  } catch (error) {
    return false; // Invalid token format
  }
}

async function refreshAccessToken() {
  try {
    const response = await axios.post(
      "https://104.131.171.128/api/token/refresh/",
      {
        refresh: localStorage.getItem("refresh_token"),
      }
    );

    localStorage.setItem("access_token", response.data.access);
    return true;
  } catch (error) {
    // If refresh fails, log out the user
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    return false;
  }
}

const routes = [
  { path: "/", component: LandingPage },
  { path: "/AppLogin", component: AppLogin },
  { path: "/Matchmaking", component: MatchmakingPage },
  { path: "/LandingPage", component: LandingPage },
  { path: "/RegistrationPage", component: RegistrationPage },
  { path: "/UserProfile", component: UserProfile },

  // Protected routes (require authentication)
  {
    path: "/LandingPage",
    component: LandingPage,
    meta: { requiresAuth: true },
  },
  { path: "/SearchPage", component: SearchPage, meta: { requiresAuth: true } },
  {
    path: "/UserProfile",
    component: UserProfile,
    meta: { requiresAuth: true },
  },
  {
    path: "/profile/:id",
    name: "PublicProfile",
    component: PublicProfile,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global Navigation Guard
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth && !(await isAuthenticated())) {
    next("/AppLogin"); // Redirect to login if not authenticated
  } else {
    next(); // Proceed as normal
  }
});

export default router;
