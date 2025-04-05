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
        maxlength="1000"
        @input="validateDescription"
      ></textarea>
      <div
        class="char-counter"
        :class="{ 'near-limit': localData.description.length > 900 }"
      >
        {{ localData.description.length }}/1000 characters
      </div>

      <label for="tags">Select Tags:</label>
      <div class="tags-container">
        <select
          id="tags"
          v-model="localData.tags"
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
        tags: this.additionalData.tags || [],
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

    validateDescription() {
      if (this.localData.description.length > 1000) {
        this.localData.description = this.localData.description.substring(
          0,
          1000
        );
      }
      this.updateData();
    },

    /* Fetches and filters predefined tags from the backend API */
    async fetchTags() {
      try {
        const response = await api.get("tag/", {
          headers: {
            "Content-Type": "application/json",
          },
        });
        console.log("Tags response:", response.data); // Add logging to debug
        this.availableTags = response.data;
      } catch (error) {
        console.error(
          "Failed to fetch tags:",
          error.response?.data || error.message
        );
        this.availableTags = []; // Ensure we reset to empty array on error
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
          tags: newValue.tags || [],
        };
      },
      deep: true,
    },
  },
};
</script>
