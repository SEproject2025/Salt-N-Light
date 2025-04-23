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
        @input="handleDescriptionInput"
      ></textarea>
      <div
        class="char-counter"
        :class="{
          'near-limit': localData.description?.length > 800,
          'at-limit': localData.description?.length >= 1000,
        }"
      >
        {{ localData.description?.length || 0 }}/1000
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
  emits: ["update:additionalData", "validation-status"],
  data() {
    return {
      localData: {
        description: this.additionalData.description || "",
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
    handleDescriptionInput() {
      // Ensure the description doesn't exceed 1000 characters
      if (this.localData.description?.length > 1000) {
        this.localData.description = this.localData.description.slice(0, 1000);
      }
      this.updateData();
    },
    /* Updates parent with current additional information values */
    updateData() {
      this.$emit("update:additionalData", {
        ...this.additionalData,
        ...this.localData,
      });
      this.validateForm();
    },
    validateForm() {
      // All fields are optional in this step
      this.$emit("validation-status", true);
    },

    /* Fetches and filters predefined tags from the backend API */
    async fetchTags() {
      try {
        const response = await api.get("tag/", {
          headers: {
            "Content-Type": "application/json",
          },
        });
        this.availableTags = response.data;
      } catch (error) {
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
          tags: newValue.tags || [],
        };
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.char-counter {
  text-align: right;
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.25rem;
}

.char-counter.near-limit {
  color: #ff6b6b;
}

.char-counter.at-limit {
  color: #ff0000;
  font-weight: bold;
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
</style>
