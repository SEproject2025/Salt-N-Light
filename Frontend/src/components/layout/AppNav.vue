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
    </div>
  </nav>
</template>

<script>
import api from "@/api/axios.js";
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
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      this.isAuthenticated = false;
      this.isSuperuser = false;
      this.$router.push("/AppLogin");
    },
  },
  watch: {
    $route() {
      this.checkAuthStatus();
    },
  },
};
</script>
<style scoped>
.auth-wrapper .form-control:focus {
  border-color: #167bff;
  box-shadow: none;
}

auth-wrapper h3 {
  text-align: right;
  margin: 0;
  line-height: 1;
  padding-bottom: 20px;
}

.admin-link {
  font-weight: bold;
  color: #e74c3c !important;
}
</style>
