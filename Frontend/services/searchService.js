import api from "@/api/axios";

export default {
  async searchProfiles(params) {
    try {
      const queryParams = new URLSearchParams();

      // Only add non-empty parameters
      if (params.q) queryParams.append("q", params.q.trim());
      if (params.user_type) queryParams.append("user_type", params.user_type);
      if (params.location)
        queryParams.append("location", params.location.trim());
      if (params.tags && params.tags.length) {
        params.tags.forEach((tag) => queryParams.append("tags", tag));
        if (params.tag_match_type) {
          queryParams.append("tag_match_type", params.tag_match_type);
        }
      }
      if (params.page) queryParams.append("page", params.page);
      if (params.sort) queryParams.append("sort", params.sort);
      if (params.page_size) queryParams.append("page_size", params.page_size);

      // Get the auth token from localStorage
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      // Add debug logging
      console.log("Search params:", Object.fromEntries(queryParams));

      const response = await api.get(
        `/api/profiles/search/?${queryParams.toString()}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          timeout: 30000,
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

      // Handle timeout error specifically
      if (error.code === "ECONNABORTED") {
        throw new Error("Search request timed out. Please try again.");
      }

      if (error.response?.status === 401) {
        // Try to refresh the token
        try {
          const refreshToken = localStorage.getItem("refresh_token");
          if (refreshToken) {
            const response = await api.post(`/api/token/refresh/`, {
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

  async getAllTags() {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await api.get("/tag/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        timeout: 30000,
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
            const response = await api.post(`/api/token/refresh/`, {
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