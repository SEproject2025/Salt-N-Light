import axios from "axios";
//import router from "@/router/router.js";

// Set the base URL for all API requests
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || "http://localhost:8000",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor to add the auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If the error status is 401 and there's no originalRequest._retry flag,
    // it means the token has expired and we need to refresh it
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) {
          // If no refresh token, this is a login error
          if (originalRequest.url.includes("api/token/")) {
            return Promise.reject(error);
          }
          // For other requests, redirect to login
          window.location.href = "/AppLogin";
          return Promise.reject(error);
        }

        const response = await axios.post(
          `${
            process.env.VUE_APP_API_URL || "http://localhost:8000"
          }/api/token/refresh/`,
          { refresh: refreshToken }
        );

        if (response.status === 200) {
          localStorage.setItem("access_token", response.data.access);
          localStorage.setItem("refresh_token", response.data.refresh);

          // Retry the original request
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/AppLogin";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
