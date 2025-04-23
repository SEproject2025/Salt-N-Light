<template>
  <nav class="navbar navbar-expand navbar-light fixed-top">
    <div class="container">
      <router-link to="/" class="navbar-brand">Home</router-link>
      <div class="navbar-nav ml-auto">
        <ul class="navbar-nav ml-auto">
          <li v-if="!isAuthenticated" class="nav-item">
            <router-link to="/AppLogin" class="nav-link">Login</router-link>
          </li>
          <li v-if="!isAuthenticated" class="nav-item">
            <router-link to="/RegistrationPage" class="nav-link"
              >Sign up</router-link
            >
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <router-link to="/UserProfile" class="nav-link"
              >Profile</router-link
            >
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <router-link to="/SearchPage" class="nav-link">Search</router-link>
          </li>
          <li v-if="isSuperuser" class="nav-item">
            <router-link to="/admin" class="nav-link admin-link"
              >Admin Dashboard</router-link
            >
          </li>
          <li v-if="isAuthenticated" class="nav-item">
            <a href="#" @click.prevent="logout" class="nav-link">Logout</a>
          </li>
        </ul>
      </div>

      <div class="navbar-nav ml-auto">
        <div class="nav-item quick-search-wrapper">
          <QuickSearch />
        </div>

        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/searchpage" class="nav-link">
              <i class="fas fa-search"></i> Advanced Search</router-link
            >
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
import api from "@/api/axios.js";
import QuickSearch from "@/components/search/QuickSearch.vue";
export default {
  name: "AppNav",
  data() {
    return {
      isAuthenticated: false,
      isSuperuser: false,
    };
  },
  created() {
    this.checkAuthStatus();
  },
  methods: {
    checkAuthStatus() {
      const token = localStorage.getItem("access_token");
      this.isAuthenticated = !!token;
      if (this.isAuthenticated) {
        this.checkSuperuserStatus();
      }
    },
    async checkSuperuserStatus() {
      try {
        const response = await api.get("api/admin/check-superuser/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        this.isSuperuser = response.data.is_superuser;
      } catch (error) {
        this.isSuperuser = false;
      }
    },
    logout() {
      localStorage.clear();
      this.isAuthenticated = false;
      this.isSuperuser = false;
      this.$router.push("/AppLogin");
    },
  },
  watch: {
    $route() {
      this.checkAuthStatus();
    },
  }
}

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

.admin-link {
  font-weight: bold;
  color: #e74c3c !important;
}
</style>
