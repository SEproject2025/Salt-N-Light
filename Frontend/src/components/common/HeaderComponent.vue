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
export default {
  name: "HeaderComponent",
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
  height: 70px;
  padding: 10px 20px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ddd;
  font-family: Arial, sans-serif;
}

/* Site Branding */
.site-branding {
  display: flex;
  align-items: center;
  gap: 10px; /* adjust spacing between icon and logo */
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
  font-size: 18px;
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
