<template>
  <div class="background-image">
    <div class="auth-wrapper">
      <div class="auth-inner">
        <h3>Login</h3>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>Email</label>
            <input
              type="email"
              class="form-control"
              placeholder="Email"
              v-model="email"
              required
            />
          </div>

          <div class="form-group">
            <label>Password</label>
            <input
              type="password"
              class="form-control"
              placeholder="Password"
              v-model="password"
              required
            />
          </div>

          <button class="btn btn-primary btn-block" type="submit">Login</button>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AppLogin",
  data() {
    return {
      email: "",
      password: "",
      errorMessage: null,
    };
  },
  methods: {
    async fetchCSRFToken() {
      try {
        // Fetch the CSRF token
        await axios.get("http://127.0.0.1:8000/login/");
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
      }
    },
    async handleLogin() {
      try {
        // Send login request with credentials and CSRF token
        const response = await axios.post(
          "http://127.0.0.1:8000/login/",
          {
            email: this.email,
            password: this.password,
          },
          {
            headers: {
              "X-CSRFToken": this.getCookie("csrftoken"),
            },
          }
        );
        console.log("Login successful:", response.data);
        this.$router.push("/SearchPage"); // Navigate to dashboard after login
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Login failed.";
      }
    },
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
    },
  },
  created() {
    this.fetchCSRFToken(); // Ensure CSRF token is fetched when the component is created
  },
};
</script>

<style scoped>
.background-image {
  background-image: url("@/assets/pictures/world.jpg");
  background-size: cover;
  background-position: center;
  height: 100vh;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.auth-wrapper {
  display: flex;
  justify-content: center;
  flex-direction: column;
  text-align: left;
}
.auth-inner {
  width: 450px;
  margin: auto;
  background: #828282;
  box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.3);
  padding: 40px 55px 45px 55px;
  border-radius: 15px;
  transition: all 0.3s;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>
