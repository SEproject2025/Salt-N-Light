<template>
  <div class="form-step">
    <h2 class="step-title">Additional Information</h2>
    <div class="form-group">
      <label for="description">Description:</label>
      <textarea
        id="description"
        v-model="localData.description"
        placeholder="Tell us about yourself and your mission"
        rows="4"
        @input="updateData"
      ></textarea>

      <label for="tags">Select Tags:</label>
      <div class="tags-container">
        <select
          id="tags"
          v-model="localData.tags_ids"
          multiple
          @change="updateData"
        >
          <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
            {{ tag.tag_name }}
          </option>
        </select>
        <p class="helper-text">
          Hold Ctrl (or Cmd on Mac) to select multiple tags
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios.js";

export default {
  name: "AdditionalInfoStep",
  props: {
    additionalData: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:additionalData"],
  data() {
    return {
      localData: {
        description: this.additionalData.description || "",
        profile_picture: null,
        tags_ids: this.additionalData.tags_ids || [],
      },
      availableTags: [],
    };
  },
  mounted() {
    this.fetchTags();
  },
  methods: {
    /* Updates parent with current additional information values */
    updateData() {
      this.$emit("update:additionalData", {
        ...this.additionalData,
        ...this.localData,
        profile_picture: null,
      });
    },

    /* Fetches predefined tags from the backend API */
    async fetchTags() {
      try {
        const response = await api.get(
          "http://127.0.0.1:8000/tag/?tag_is_predefined=true"
        );
        console.log("Raw response:", response);
        console.log("Response data:", response.data);
        this.availableTags = response.data;
      } catch (error) {
        console.error("Failed to fetch tags:", {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
          headers: error.response?.headers,
        });
        this.availableTags = []; // Set empty array as fallback
      }
    },
  },
  watch: {
    /* Syncs local data when parent data changes */
    additionalData: {
      handler(newValue) {
        this.localData = {
          description: newValue.description || "",
          profile_picture: null,
          tags_ids: newValue.tags_ids || [],
        };
      },
      deep: true,
    },
  },
};
</script>
