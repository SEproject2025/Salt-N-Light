import { createRouter, createWebHistory } from "vue-router";
import { jwtDecode } from "jwt-decode";
import AppLogin from "@/pages/AppLogin.vue";
import UserProfile from "@/pages/UserProfile.vue";
import LandingPage from "@/pages/LandingPage.vue";
import SearchPage from "@/pages/SearchPage.vue";
import MatchmakingPage from "@/pages/MatchmakingPage.vue";
import RegistrationPage from "@/pages/RegistrationPage.vue";
import PublicProfile from "@/pages/PublicProfile.vue";
import api from "@/api/axios.js";

async function isAuthenticated() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    return false;
  }

  try {
    const decodedToken = jwtDecode(token);
    const currentTime = Math.floor(Date.now() / 1000);

    if (decodedToken.exp < currentTime) {
      return await refreshAccessToken();
    }

    return true;
  } catch (error) {
    console.error("Token validation error:", error);
    return false;
  }
}

async function refreshAccessToken() {
  try {
    const response = await api.post("api/token/refresh/", {
      refresh: localStorage.getItem("refresh_token"),
    });

    localStorage.setItem("access_token", response.data.access);
    return true;
  } catch (error) {
    console.error("Token refresh error:", error);
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    return false;
  }
}

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/AppLogin",
    name: "AppLogin",
    component: AppLogin,
    meta: { guest: true },
  },
  {
    path: "/RegistrationPage",
    name: "RegistrationPage",
    component: RegistrationPage,
    meta: { guest: true },
  },
  {
    path: "/SearchPage",
    name: "SearchPage",
    component: SearchPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/Matchmaking",
    name: "Matchmaking",
    component: MatchmakingPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/UserProfile",
    name: "UserProfile",
    component: UserProfile,
    meta: { requiresAuth: true },
  },
  {
    path: "/profile/:id",
    name: "PublicProfile",
    component: PublicProfile,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global Navigation Guard
router.beforeEach(async (to, from, next) => {
  const isUserAuthenticated = await isAuthenticated();

  // If the route requires auth and user is not authenticated
  if (to.meta.requiresAuth && !isUserAuthenticated) {
    next("/AppLogin");
    return;
  }

  // If it's a guest route (login/register) and user is authenticated
  if (to.meta.guest && isUserAuthenticated) {
    next("/SearchPage");
    return;
  }

  next();
});

export default router;
