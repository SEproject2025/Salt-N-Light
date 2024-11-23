import axios from "axios";
// Axios instance with default configuration
const apiClient = axios.create({
  baseURL: "http://localhost:8000/BaseApp/",
  withCredentials: true, // Include cookies in requests
});
// Function to initialize CSRF token
export const getCsrfToken = async () => {
  try {
    // Make a request to set the CSRF cookieawait apiClient.get('login/');
  } catch (error) {
    console.error("Failed to fetch CSRF token:", error);
  }
};

export default apiClient;
