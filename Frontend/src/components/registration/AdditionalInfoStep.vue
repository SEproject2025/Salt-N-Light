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

      <div class="anonymous-option">
        <label class="checkbox-label">
          <input
            type="checkbox"
            v-model="localData.is_anonymous"
            @change="updateData"
          />
          <span>Make my profile anonymous</span>
        </label>
        <p class="helper-text">
          Anonymous profiles will not appear in search results or matchmaking
        </p>
      </div>

      <label for="tags">Select some tags that describe your ministry:</label>
      <div class="tags-container">
        <div class="tags-grid">
          <div
            v-for="tag in availableTags"
            :key="tag.id"
            class="tag-option"
            :class="{ selected: localData.tags.includes(tag.id) }"
            @click="toggleTag(tag.id)"
          >
            {{ tag.tag_name }}
          </div>
        </div>
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
        is_anonymous: this.additionalData.is_anonymous || false,
        tags: this.additionalData.tags || [],
      },
      availableTags: [],
    };
  },
  mounted() {
    this.fetchTags();
  },
  methods: {
    toggleTag(tagId) {
      const index = this.localData.tags.indexOf(tagId);
      if (index === -1) {
        this.localData.tags.push(tagId);
      } else {
        this.localData.tags.splice(index, 1);
      }
      this.updateData();
    },
    /* Updates parent with current additional information values */
    updateData() {
      this.$emit("update:additionalData", {
        ...this.additionalData,
        ...this.localData,
      });
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
          is_anonymous: newValue.is_anonymous || false,
          tags: newValue.tags || [],
        };
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.anonymous-option {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
  margin-top: 10px;
}

.tag-option {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s ease;
}

.tag-option:hover {
  background-color: #f0f0f0;
}

.tag-option.selected {
  background-color: #e3f2fd;
  border-color: #2196f3;
  color: #1976d2;
}

.helper-text {
  margin-top: 5px;
  font-size: 0.9rem;
  color: #666;
}
</style>
