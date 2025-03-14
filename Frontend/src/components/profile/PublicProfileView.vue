<template>
  <div class="profile-card">
    <div class="profile-header">
      <h1>{{ profile.first_name }} {{ profile.last_name }}</h1>
    </div>

    <div class="profile-content">
      <div class="profile-section">
        <h3>Personal Information</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Username</span>
            <span class="value">{{ profile.user?.username }}</span>
          </div>
          <div class="info-item">
            <span class="label">Email</span>
            <span class="value">{{ profile.user?.email }}</span>
          </div>
          <div class="info-item">
            <span class="label">User Type</span>
            <span class="value">{{ profile.user_type }}</span>
          </div>
          <div class="info-item">
            <span class="label">Denomination</span>
            <span class="value">{{ profile.denomination }}</span>
          </div>
          <div class="info-item">
            <span class="label">Phone</span>
            <span class="value">{{ profile.phone_number }}</span>
          </div>
          <div class="info-item">
            <span class="label">Years of Experience</span>
            <span class="value">{{ profile.years_of_experience }}</span>
          </div>
        </div>
      </div>

      <div class="profile-section">
        <h3>Location</h3>
        <div class="address">
          <p>{{ profile.street_address }}</p>
          <p>{{ profile.city }}, {{ profile.state }}</p>
          <p>{{ profile.country }}</p>
        </div>
      </div>

      <div class="profile-section">
        <div class="tag-header">
          <h3>Tags</h3>
          <div class="tag-controls">
            <div class="tag-dropdown">
              <button
                v-if="!isOwnProfile"
                class="add-tag-btn"
                @click="toggleTagDropdown"
              >
                <span class="plus-icon">+</span>
              </button>
              <div v-if="showTagDropdown" class="tag-dropdown-menu">
                <div
                  v-for="tag in availableTags"
                  :key="tag.id"
                  class="tag-dropdown-item"
                  @click="handleAddTag(tag.id)"
                >
                  {{ tag.name }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="tags">
          <span
            v-for="tag in displayTags"
            :key="tag.id"
            class="tag"
            :class="{ 'self-added': tag.added_by === profile.user.id }"
            :title="
              tag.added_by === profile.user.id
                ? 'You can only remove tags that you added'
                : ''
            "
          >
            {{ tag.name }}
            <button
              v-if="isOwnProfile && tag.added_by !== profile.user.id"
              class="remove-tag-btn"
              @click="handleRemoveTag(tag.id)"
            >
              ×
            </button>
          </span>
        </div>
        <div v-if="error" class="error" role="alert">{{ error }}</div>
      </div>

      <div class="profile-section">
        <h3>Description</h3>
        <p class="description">{{ profile.description }}</p>
      </div>
    </div>

    <!-- Tag Dialog -->
    <div v-if="showTagDialog" class="dialog-overlay" @click="closeTagDialog">
      <div class="dialog" @click.stop>
        <h3>Add Tag</h3>
        <div class="dialog-content">
          <div class="form-group">
            <label>Select Tag:</label>
            <select v-model="selectedTag" class="tag-select">
              <option value="">Choose a tag...</option>
              <option
                v-for="tag in availableTags"
                :key="tag.id"
                :value="tag.id"
              >
                {{ tag.name }}
              </option>
            </select>
            <div v-if="error" class="error">{{ error }}</div>
          </div>
          <div class="dialog-actions">
            <button class="cancel-btn" @click="closeTagDialog">Cancel</button>
            <button
              class="add-btn"
              @click="handleAddTag"
              :disabled="!selectedTag"
            >
              Add Tag
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PublicProfileView",
  props: {
    profile: {
      type: Object,
      required: true,
    },
    isOwnProfile: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showTagDialog: false,
      selectedTag: "",
      availableTags: [],
      error: null,
      localTags: [],
      showTagDropdown: false,
    };
  },
  computed: {
    displayTags() {
      return this.localTags.length > 0 ? this.localTags : this.profile.tags;
    },
  },
  watch: {
    "profile.tags": {
      immediate: true,
      handler(newTags) {
        this.localTags = [...(newTags || [])];
      },
    },
  },
  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("access_token");
      if (!token) {
        console.error("No access token found in localStorage");
        this.error = "Please log in to manage tags";
        return null;
      }
      return {
        Authorization: `Bearer ${token}`,
      };
    },
    async fetchAvailableTags() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/tag/", {
          headers: this.getAuthHeader(),
        });
        this.availableTags = response.data.map((tag) => ({
          id: tag.id,
          name: tag.tag_name,
          added_by: tag.added_by,
        }));
      } catch (error) {
        console.error("Error fetching tags:", error);
      }
    },
    closeTagDialog() {
      this.showTagDialog = false;
      this.selectedTag = "";
    },
    toggleTagDropdown() {
      this.showTagDropdown = !this.showTagDropdown;
    },
    async handleAddTag(tagId) {
      try {
        const headers = this.getAuthHeader();
        if (!headers) {
          return; // Error message already set in getAuthHeader
        }

        // First verify the token is still valid
        try {
          await axios.get("http://127.0.0.1:8000/api/profiles/me/", {
            headers,
          });
        } catch (verifyError) {
          if (verifyError.response?.status === 401) {
            localStorage.removeItem("access_token"); // Clear invalid token
            this.error = "Your session has expired. Please log in again.";
            return;
          }
        }

        const addResponse = await axios.post(
          "http://127.0.0.1:8000/tag/add-to-profile/",
          {
            profile_id: this.profile.user.id,
            tag_id: tagId,
          },
          {
            headers: {
              ...headers,
              "Content-Type": "application/json",
            },
          }
        );
        this.$emit("tag-added", addResponse.data);
        this.showTagDropdown = false; // Close the dropdown after adding
        this.$emit("refresh");
        this.error = null;
      } catch (error) {
        console.error("Error adding tag:", error.response || error);
        if (error.response?.status === 401) {
          localStorage.removeItem("access_token"); // Clear invalid token
          this.error = "Your session has expired. Please log in again.";
        } else if (
          error.response?.data?.error?.includes("UNIQUE constraint failed")
        ) {
          this.error = "You already added this tag!";
        } else {
          this.error =
            error.response?.data?.message ||
            error.response?.data?.error ||
            "Error adding tag";
        }
      }
    },
    async handleRemoveTag(tagId) {
      try {
        const headers = this.getAuthHeader();
        if (!headers) {
          return; // Error message already set in getAuthHeader
        }

        await axios.post(
          "http://127.0.0.1:8000/tag/remove-from-profile/",
          {
            profile_id: this.profile.user.id,
            tag_id: tagId,
          },
          {
            headers: {
              ...headers,
              "Content-Type": "application/json",
            },
          }
        );

        // Update the UI immediately by filtering out the removed tag
        const updatedTags = this.profile.tags.filter((tag) => tag.id !== tagId);
        this.$emit("update:profile", {
          ...this.profile,
          tags: updatedTags,
        });

        // Still emit events for parent component
        this.$emit("tag-removed", {
          tagId,
          profileId: this.profile.user.id,
        });
        this.$emit("refresh");
        this.error = null;
      } catch (error) {
        console.error("Error removing tag:", error.response || error);
        if (error.response?.status === 401) {
          localStorage.removeItem("access_token"); // Clear invalid token
          this.error = "Your session has expired. Please log in again.";
        } else if (error.response?.status === 404) {
          this.error = "You can only remove tags that you added!";
        } else {
          this.error =
            error.response?.data?.message ||
            error.response?.data?.error ||
            "Error removing tag";
        }
      }
    },
  },
  mounted() {
    this.fetchAvailableTags();
  },
};
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.profile-header h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.8rem;
}

.profile-section {
  margin-bottom: 2rem;
}

.profile-section h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.3rem;
}

.value {
  font-size: 1.1rem;
  color: #2c3e50;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #e1f5fe;
  color: #0288d1;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  transition: all 0.2s ease;
}

.tag.self-added {
  background: #f8f8f8;
  color: #666;
  cursor: help;
  border: 1px solid #e0e0e0;
}

.tag.self-added:hover {
  background: #f0f0f0;
}

.tag:not(.self-added) {
  background: #e1f5fe;
  color: #0288d1;
}

.tag:not(.self-added):hover {
  background: #b3e5fc;
}

.description {
  line-height: 1.6;
  color: #2c3e50;
}

@media (max-width: 1024px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    max-width: 100%;
  }
}

.tag-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.tag-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tag-select {
  padding: 0.3rem 0.8rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
  max-height: 200px;
  overflow-y: auto;
}

.tag-select option {
  padding: 0.5rem;
}

/* For Webkit browsers like Chrome/Safari */
.tag-select::-webkit-scrollbar {
  width: 8px;
}

.tag-select::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.tag-select::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.tag-select::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* For Firefox */
.tag-select {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

.tag-dropdown {
  position: relative;
}

.tag-dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
  min-width: 150px;
  margin-top: 0.5rem;
}

.tag-dropdown-item {
  padding: 0.5rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.tag-dropdown-item:hover {
  background-color: #f5f5f5;
}

.add-tag-btn {
  background: #000000;
  color: white;
  border: none;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.add-tag-btn:hover {
  background: #333333;
  transform: scale(1.05);
}

.plus-icon {
  font-size: 24px;
  line-height: 1;
  font-weight: 300;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dialog h3 {
  margin: 0 0 1rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.cancel-btn,
.add-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.cancel-btn {
  background: #f1f1f1;
  color: #666;
}

.add-btn {
  background: #3498db;
  color: white;
}

.add-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.remove-tag-btn {
  background: none;
  border: none;
  color: #0288d1;
  font-size: 1.2rem;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.remove-tag-btn:hover {
  background-color: rgba(2, 136, 209, 0.1);
}

.error {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.3rem;
  margin-top: 0.5rem;

  opacity: 5;
  transition: opacity 0.5s;
}
</style>
