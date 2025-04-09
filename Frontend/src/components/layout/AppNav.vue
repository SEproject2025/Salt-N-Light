<template>
  <nav class="navbar navbar-expand navbar-light fixed-top">
    <div class="container">
      <router-link to="/" class="navbar-brand">Home</router-link>

      <div class="navbar-nav ml-auto">
        <div class="nav-item quick-search-wrapper">
          <QuickSearch />
        </div>

        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/searchpage" class="nav-link">
              <i class="fas fa-search"></i> Advanced Search
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/AppLogin" class="nav-link">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/RegistrationPage" class="nav-link"
              >Sign up</router-link
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import QuickSearch from "@/components/search/QuickSearch.vue";

export default {
  name: "AppNav",
  components: {
    QuickSearch,
  },
};
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 1rem;
}

.navbar-brand {
  font-weight: 500;
  color: #333;
}

.nav-link {
  color: #666;
  padding: 0.5rem 1rem;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #1976d2;
}

.quick-search-wrapper {
  margin-right: 1rem;
}

.navbar-nav {
  display: flex;
  align-items: center;
}

.nav-item {
  margin-left: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .quick-search-wrapper {
    margin: 0.5rem 0;
    width: 100%;
  }

  .navbar-nav {
    flex-direction: column;
    width: 100%;
  }

  .nav-item {
    margin: 0.25rem 0;
    width: 100%;
  }

  .nav-link {
    padding: 0.5rem 0;
  }
}
</style>
