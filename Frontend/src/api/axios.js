import axios from "axios";

// Set the base URL for all API requests
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || "http://127.0.0.1:8000",
  timeout: 10000, // Optional: Set a timeout (in ms)
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
