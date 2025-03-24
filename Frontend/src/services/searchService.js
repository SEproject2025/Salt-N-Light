import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default {
  async searchProfiles(params) {
    try {
      const queryParams = new URLSearchParams();

      if (params.q) queryParams.append("q", params.q);
      if (params.user_type) queryParams.append("user_type", params.user_type);
      if (params.location) queryParams.append("location", params.location);
      if (params.tags && params.tags.length) {
        params.tags.forEach((tag) => queryParams.append("tags", tag));
      }
      if (params.page) queryParams.append("page", params.page);
      if (params.sort) queryParams.append("sort", params.sort);
      if (params.page_size) queryParams.append("page_size", params.page_size);

      // Get the auth token from localStorage
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await axios.get(
        `${API_URL}/api/profiles/search/?${queryParams.toString()}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // Add some debug logging
      console.log("Search response:", {
        total: response.data.count,
        pageSize: params.page_size,
        currentPage: params.page,
        results: response.data.results?.length,
      });

      return {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        results: response.data.results || [],
      };
    } catch (error) {
      console.error("Error searching profiles:", error);
      if (error.response?.status === 401) {
        // Try to refresh the token
        try {
          const refreshToken = localStorage.getItem("refresh_token");
          if (refreshToken) {
            const response = await axios.post(`${API_URL}/api/token/refresh/`, {
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
      throw error;
    }
  },

  async getTags() {
    try {
      // Get the auth token from localStorage
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await axios.get(`${API_URL}/api/tags/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      // Sort tags alphabetically by tag_name
      const tags = response.data.sort((a, b) =>
        a.tag_name.localeCompare(b.tag_name)
      );
      return tags;
    } catch (error) {
      console.error("Error fetching tags:", error);
      if (error.response?.status === 401) {
        // Try to refresh the token
        try {
          const refreshToken = localStorage.getItem("refresh_token");
          if (refreshToken) {
            const response = await axios.post(`${API_URL}/api/token/refresh/`, {
              refresh: refreshToken,
            });
            localStorage.setItem("access_token", response.data.access);
            // Retry the getTags with the new token
            return this.getTags();
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
