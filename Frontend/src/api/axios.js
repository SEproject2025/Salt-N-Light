import axios from "axios";

// Set the base URL for all API requests
const api = axios.create({
  baseURL: "https://baptist.coffee/",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
