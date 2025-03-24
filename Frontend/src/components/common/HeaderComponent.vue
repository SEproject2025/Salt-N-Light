<template>
  <header class="header-banner">
    <!-- Site Icon -->
    <div class="site-icon">
      <a href="/LandingPage" title="SaltnLife">
        <img
          src="@\assets\pictures\saltnlightlogo1.webp"
          alt="SaltnLight Logo"
          class="icon"
        />
      </a>
    </div>

    <!-- Quick Search for logged in users -->
    <div v-if="isLoggedIn" class="quick-search-container">
      <QuickSearch />
    </div>

    <!-- Navigation Links -->
    <nav class="nav-links">
      <a href="/SearchPage" class="nav-link">Explore</a>
      <a href="/RegistrationPage" class="nav-link">Sign Up</a>
      <a @click="navigateToProfile" class="nav-link" style="cursor: pointer"
        >Profile</a
      >
      <div>
        <button @click="logout">Logout</button>
      </div>
    </nav>
  </header>
</template>

<script>
import QuickSearch from "@/search/QuickSearch.vue";

export default {
  name: "HeaderComponent",
  components: {
    QuickSearch,
  },
  data() {
    return {
      isLoggedIn: false,
    };
  },
  created() {
    // Check if user is logged in
    this.isLoggedIn = !!localStorage.getItem("access_token");
  },
  methods: {
    logout() {
      // Clear tokens from localStorage
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

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
  padding: 10px 20px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ddd;
  font-family: Arial, sans-serif;
}

/* Site Icon */
.site-icon .icon {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  object-fit: cover;
}

/* Quick Search Container */
.quick-search-container {
  flex: 1;
  max-width: 600px;
  margin: 0 20px;
  position: relative;
}

/* Navigation Links */
.nav-links {
  display: flex;
  gap: 20px;
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

/* Logout Button Styling */
.header-banner button {
  background-color: #333;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 40px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.header-banner button:hover {
  background-color: #0056b3;
}
</style>
