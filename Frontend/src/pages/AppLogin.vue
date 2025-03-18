<template>
  <div class="login-page-container">
    <div class="login-card">
      <h1>Login</h1>

      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Enter your username"
            required
          />

          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />

          <button type="submit" class="btn-submit">Login</button>
        </div>
      </form>

      <p v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </p>

      <div class="registration-link">
        <p>
          Don't have an account?
          <router-link to="/RegistrationPage">Sign up here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://104.131.171.128/api/token/", {
          username: this.username,
          password: this.password,
        });

        // Store tokens in local storage or Vuex
        localStorage.setItem("access_token", response.data.access);
        localStorage.setItem("refresh_token", response.data.refresh);

        // Redirect to dashboard or another page
        this.$router.push("/SearchPage");
      } catch (error) {
        this.errorMessage = "Invalid credentials. Please try again.";
      }
    },
  },
};
</script>

<style scoped>
@import "../components/registration/styles.css";

.login-page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  background: #f4f7fc;
  padding: 20px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 {
  margin-bottom: 30px;
  color: #333;
  font-weight: 600;
  font-size: 2rem;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 20px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
  outline: none;
}

.btn-submit {
  width: 100%;
  padding: 12px 24px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.btn-submit:hover {
  background-color: #43a047;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 12px 15px;
  margin-top: 20px;
  border-radius: 8px;
  border-left: 4px solid #f44336;
  font-weight: 500;
  text-align: left;
}

.registration-link {
  margin-top: 25px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
}

.registration-link p {
  color: #757575;
}

.registration-link a {
  color: #4caf50;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.registration-link a:hover {
  color: #2e7d32;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .login-card {
    padding: 25px;
  }
}
</style>
