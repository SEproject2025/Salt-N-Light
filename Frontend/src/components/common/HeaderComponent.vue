<template>
  <header class="header-banner">
    <!-- Site Icon -->
    <div class="site-icon">
      <router-link to="/" title="SaltnLife">
        <img
          src="@\assets\pictures\saltnlightlogo1.webp"
          alt="SaltnLight Logo"
          class="icon"
        />
      </router-link>
    </div>

    <!-- Quick Search -->
    <QuickSearch class="header-search" />

    <!-- Navigation Links -->
    <nav class="nav-links">
      <router-link to="/SearchPage" class="nav-link">Explore</router-link>
      <router-link to="/RegistrationPage" class="nav-link">Sign Up</router-link>
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
import QuickSearch from "@/components/search/QuickSearch.vue";

export default {
  name: "HeaderComponent",
  components: {
    QuickSearch,
  },
  methods: {
    logout() {
      // Clear tokens from localStorage
      localStorage.clear();

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
  position: relative;
}

/* Site Icon */
.site-icon .icon {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  object-fit: cover;
}

/* Header Search */
.header-search {
  flex: 1;
  max-width: 600px;
  margin: 0 20px;
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

/* Responsive Design */
@media (max-width: 768px) {
  .header-banner {
    flex-wrap: wrap;
    padding: 10px;
  }

  .header-search {
    order: 3;
    width: 100%;
    margin: 10px 0;
    max-width: none;
  }

  .nav-links {
    gap: 10px;
  }
}
</style>
