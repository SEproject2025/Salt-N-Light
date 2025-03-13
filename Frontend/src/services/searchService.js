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

      const response = await axios.get(
        `${API_URL}/api/profiles/search/?${queryParams.toString()}`
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
      throw error;
    }
  },

  async getTags() {
    try {
      const response = await axios.get(`${API_URL}/tag/`);
      // Sort tags alphabetically by tag_name
      const tags = response.data.sort((a, b) =>
        a.tag_name.localeCompare(b.tag_name)
      );
      return tags;
    } catch (error) {
      console.error("Error fetching tags:", error);
      throw error;
    }
  },
};
