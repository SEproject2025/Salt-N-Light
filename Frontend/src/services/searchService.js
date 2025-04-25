import api from "@/api/axios";

// Helper function to get user ID from JWT token
function getUserIdFromToken() {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  try {
    // JWT tokens are base64 encoded and have 3 parts separated by dots
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const payload = JSON.parse(window.atob(base64));
    return payload.user_id;
  } catch (error) {
    console.error("Error parsing JWT token:", error);
    return null;
  }
}

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
      if (params.page_size && params.page_size !== "all") {
        queryParams.append("page_size", params.page_size);
      }

      const response = await api.get(`/api/search/?${queryParams.toString()}`);

      // Get current user's ID from JWT token
      const currentUserId = getUserIdFromToken();

      if (Array.isArray(response.data)) {
        // Filter out anonymous profiles, profiles without names, and current user's profile
        const filteredResults = response.data.filter(
          (profile) =>
            !profile.is_anonymous &&
            (!currentUserId || profile.user.id !== currentUserId) &&
            (profile.first_name || profile.last_name)
        );
        return {
          count: filteredResults.length,
          next: null,
          previous: null,
          results: filteredResults,
        };
      } else {
        // Filter out anonymous profiles, profiles without names, and current user's profile
        const filteredResults = (response.data.results || []).filter(
          (profile) =>
            !profile.is_anonymous &&
            (!currentUserId || profile.user.id !== currentUserId) &&
            (profile.first_name || profile.last_name)
        );
        return {
          count: filteredResults.length,
          next: response.data.next,
          previous: response.data.previous,
          results: filteredResults,
        };
      }
    } catch (error) {
      console.error("Error searching profiles:", error);
      throw error;
    }
  },

  async getAllTags() {
    try {
      const response = await api.get("/tag/");
      return response.data;
    } catch (error) {
      console.error("Error fetching tags:", error);
      throw error;
    }
  },

  // Alias for getAllTags for backward compatibility
  getTags() {
    return this.getAllTags();
  },
};
