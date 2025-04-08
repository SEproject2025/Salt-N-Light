import axios from "axios";

// Set the base URL for all API requests
const api = axios.create({
  baseURL: "https://api.evangelium.app/", // Add your root API URL
  timeout: 30000, // Optional: Set a timeout (in ms)
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
