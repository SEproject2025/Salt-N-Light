import api from "@/api/axios";

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

      console.log("Search API Request:", {
        url: `/api/search/?${queryParams.toString()}`,
        params: params,
      });

      const response = await api.get(`/api/search/?${queryParams.toString()}`);

      console.log("Search API Response:", {
        status: response.status,
        data: response.data,
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
