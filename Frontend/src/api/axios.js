import axios from "axios";

// Set the base URL for all API requests
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
