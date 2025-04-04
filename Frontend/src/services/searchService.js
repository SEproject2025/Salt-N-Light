import api from "../api/axios";

export const searchService = {
  async searchProfiles(params) {
    try {
      // Get the auth token from localStorage
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      // Add debug logging
      console.log("Search params:", params);

      const response = await api.get("/api/profiles/search/", {
        params,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // Add some debug logging
      console.log("Search response:", {
        total: response.data.count,
        pageSize: params.page_size,
        currentPage: params.page,
        results: response.data.results?.length,
      });

      return response.data;
    } catch (error) {
      console.error("Error searching profiles:", error);

      // Handle timeout error specifically
      if (error.code === "ECONNABORTED") {
        throw new Error("Search request timed out. Please try again.");
      }

      if (error.response?.status === 401) {
        // Try to refresh the token
        try {
          const refreshToken = localStorage.getItem("refresh_token");
          if (refreshToken) {
            const response = await api.post("/api/token/refresh/", {
              refresh: refreshToken,
            });
            localStorage.setItem("access_token", response.data.access);
            // Retry the search with the new token
            return this.searchProfiles(params);
          }
        } catch (refreshError) {
          console.error("Token refresh failed:", refreshError);
        }
        // If refresh fails or no refresh token, redirect to login
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/AppLogin";
      }

      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error("Error response:", error.response.data);
        throw new Error(
          error.response.data.error || "Failed to search profiles"
        );
      } else if (error.request) {
        // The request was made but no response was received
        console.error("No response received:", error.request);
        throw new Error("No response received from server");
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error("Error setting up request:", error.message);
        throw error;
      }
    }
  },

  async getAllTags() {
    try {
      // Get the auth token from localStorage
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await api.get("/api/tag/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // Sort tags alphabetically by tag_name
      return response.data.sort((a, b) => a.tag_name.localeCompare(b.tag_name));
    } catch (error) {
      console.error("Error fetching all tags:", error);
      if (error.response?.status === 401) {
        // Try to refresh the token
        try {
          const refreshToken = localStorage.getItem("refresh_token");
          if (refreshToken) {
            const response = await api.post("/api/token/refresh/", {
              refresh: refreshToken,
            });
            localStorage.setItem("access_token", response.data.access);
            // Retry the tags fetch with the new token
            return this.getAllTags();
          }
        } catch (refreshError) {
          console.error("Token refresh failed:", refreshError);
        }
        // If refresh fails or no refresh token, redirect to login
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/AppLogin";
      }
      throw error;
    }
  },
};
