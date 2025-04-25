<template>
  <header class="header-banner">
    <!-- Site Branding -->
    <div class="site-branding">
      <!-- Site Logo -->
      <div class="site-logo">
        <a href="/LandingPage">
          <img
            src="@/assets/pictures/Evangelium-Logo-01.png"
            alt="Evangelium Logo"
            class="logo"
          />
        </a>
      </div>
    </div>

    <!-- Navigation Links -->
    <nav class="nav-links">
      <!-- Matchmaking -->
      <a
        href="/Matchmaking"
        class="flex flex-col items-center hover:text-blue-500 transition-colors duration-200"
      >
        <span class="material-symbols-outlined">diversity_3</span>
        <span>Connect</span>
      </a>
      <!-- Explore -->
      <a
        href="/SearchPage"
        class="flex flex-col items-center hover:text-blue-500 transition-colors duration-200"
      >
        <span class="material-symbols-outlined"> travel_explore </span>
        <span>Explore</span>
      </a>

      <!-- Sign Up -->
      <a
        href="/RegistrationPage"
        class="flex flex-col items-center hover:text-blue-500 transition-colors duration-200"
      >
        <span class="material-symbols-outlined"> how_to_reg </span>
        <span>Sign Up</span>
      </a>

      <!-- Profile -->
      <a
        @click="navigateToProfile"
        class="flex flex-col items-center hover:text-blue-500 transition-colors duration-200"
        style="cursor: pointer"
      >
        <span class="material-symbols-outlined">account_circle</span>
        <span>Me</span>
      </a>

      <!-- Logout -->
      <a
        v-if="isLoggedIn"
        @click="logout"
        class="flex flex-col items-center hover:text-blue-500 transition-colors duration-200"
        style="cursor: pointer"
      >
        <span class="material-symbols-outlined">logout</span>
        <span>Logout</span>
      </a>
    </nav>
  </header>
</template>

<script>
import { inject } from "vue";

export default {
  name: "HeaderComponent",
  setup() {
    const isLoggedIn = inject("isLoggedIn");
    const updateLoginState = inject("updateLoginState");

    return {
      isLoggedIn,
      updateLoginState,
    };
  },
  created() {
    // Listen for storage events to detect login/logout
    window.addEventListener("storage", this.handleStorageChange);
  },
  beforeUnmount() {
    // Clean up event listener
    window.removeEventListener("storage", this.handleStorageChange);
  },
  methods: {
    handleStorageChange(event) {
      if (event.key === "access_token") {
        this.updateLoginState(!!event.newValue);
      }
    },
    logout() {
      // Clear tokens from localStorage
      localStorage.clear();
      this.updateLoginState(false);
      // Redirect to login
      this.$router.push("/");
    },
    navigateToProfile() {
      // Check if user is logged in by looking for access token
      const token = localStorage.getItem("access_token");
      if (token) {
        this.$router.push("/UserProfile");
      } else {
        this.$router.push("/AppLogin");
      }
    },
  },
};
</script>

<style scoped>
/* General Header Styling */
.header-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
  padding: 10px 20px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ddd;
  font-family: Arial, sans-serif;
  position: relative;
}

/* Site Branding */
.site-branding {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Site Logo */
.site-logo .logo {
  margin-left: 50px;
  height: auto;
  width: 185px;
  border-radius: 0;
  object-fit: contain;
}

/* Navigation Links */
.nav-links {
  margin-right: 50px;
  display: flex;
  gap: 20px;
  font-size: 15px;
  text-align: center;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

.nav-link:hover {
  color: #007bff;
}

/* Logout Button Styling 
.header-banner button {
  background-color: #333;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 40px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}*/

.header-banner button:hover {
  background-color: #0056b3;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-banner {
    padding: 10px;
    height: auto;
    flex-direction: column;
    gap: 10px;
  }

  .site-logo .logo {
    margin-left: 0;
    width: 150px;
  }

  .nav-links {
    margin-right: 0;
    width: 100%;
    justify-content: space-around;
    gap: 10px;
    font-size: 13px;
  }

  .nav-links a {
    flex: 1;
    max-width: 80px;
  }

  .material-symbols-outlined {
    font-size: 20px;
  }
}
</style>
