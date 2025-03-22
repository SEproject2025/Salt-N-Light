import axios from "axios";

// Set the base URL for all API requests
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/", // Add your root API URL
  timeout: 10000, // Optional: Set a timeout (in ms)
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
