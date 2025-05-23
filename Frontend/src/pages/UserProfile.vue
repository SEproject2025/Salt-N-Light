<template>
  <div class="profile-container">
    <div v-if="loading">
      <p>Loading...</p>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="profile-layout">
      <div class="content-wrapper">
        <div class="main-content">
          <transition name="fade" mode="out-in">
            <ProfileView
              v-if="!editing"
              :profile="profile"
              @edit="editing = true"
              key="view"
            >
              <div class="tag-section">
                <div class="tag-header">
                  <h3>Tags</h3>
                  <button class="plus-button" @click="showTagDialog = true">
                    <span class="plus-icon">+</span>
                  </button>
                </div>
                <div class="tags-list">
                  <div
                    v-for="tag in profile.tags"
                    :key="tag.id"
                    class="tag-chip"
                  >
                    {{ tag.name }}
                  </div>
                </div>
              </div>
            </ProfileView>
            <ProfileEdit
              v-else
              :profile="profile"
              :available-tags="availableTags"
              :selected-tags="selectedTags"
              @cancel="editing = false"
              @submit="updateProfile"
              key="edit"
            />
          </transition>
        </div>
        <aside class="side-panel">
          <div class="notification-card">
            <NotificationList />
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  min-height: 100vh;
}

.profile-layout {
  position: relative;
}

.content-wrapper {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
  align-items: flex-start;
}

.main-content {
  flex: 3;
  padding: 20px;
}

.side-panel {
  flex: 1;
  max-width: 350px;
  position: sticky;
  top: 20px;
}

.notification-card {
  padding: 20px;
}

.error {
  background: #fee;
  color: #e74c3c;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 1200px) {
  .content-wrapper {
    flex-direction: column;
  }

  .side-panel {
    width: 100%;
    max-width: none;
    position: static;
  }

  .main-content,
  .notification-card {
    padding: 15px;
  }
}

@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
}

.tag-section {
  margin-top: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.tag-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.tag-header h3 {
  margin: 0;
  color: #2c3e50;
}

.plus-button {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #2ecc71;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: transform 0.2s ease;
}

.plus-button:hover {
  transform: scale(1.1);
  background-color: #27ae60;
}

.plus-button:active {
  transform: scale(0.95);
}

.plus-icon {
  color: white;
  font-size: 18px;
  font-weight: bold;
  line-height: 1;
  user-select: none;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-chip {
  background-color: #3498db;
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 14px;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background-color: white;
  padding: 24px;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dialog-content h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #3498db;
  outline: none;
}

.tag-select {
  background-color: white;
  cursor: pointer;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-button,
.submit-button {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.cancel-button {
  background-color: #f1f2f6;
  color: #2c3e50;
}

.submit-button {
  background-color: #2ecc71;
  color: white;
}

.cancel-button:hover {
  background-color: #dcdde1;
}

.submit-button:hover {
  background-color: #27ae60;
}
</style>

<script>
import api from "@/api/axios.js";
import ProfileView from "@/components/profile/ProfileView.vue";
import ProfileEdit from "@/components/profile/ProfileEdit.vue";
import NotificationList from "@/components/profile/NotificationList.vue";

export default {
  name: "UserProfile",
  components: {
    ProfileView,
    ProfileEdit,
    NotificationList,
  },
  data() {
    return {
      profile: {},
      originalProfile: {},
      loading: true,
      error: null,
      editing: false,
      selectedTags: [],
      availableTags: [],
      showTagDialog: false,
    };
  },
  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("access_token");
      return { Authorization: `Bearer ${token}` };
    },

    async fetchProfile(retry = true) {
      try {
        // Check for token before making the request
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.error = "Please log in to view your profile.";
          this.$router.push("/AppLogin");
          return;
        }

        const [profileResponse, tagResponse] = await Promise.all([
          api.get(`api/profiles/me/`, {
            headers: this.getAuthHeader(),
          }),
          api.get(`tag/`),
        ]);

        if (!profileResponse.data || !profileResponse.data.user) {
          throw new Error("Invalid profile data received");
        }

        this.profile = profileResponse.data;
        this.originalProfile = JSON.parse(JSON.stringify(profileResponse.data));
        this.selectedTags = profileResponse.data.tags.map((tag) => tag.id);

        this.availableTags = tagResponse.data.map((tag) => ({
          id: tag.id,
          name: tag.tag_name,
        }));

        this.profile.tags = profileResponse.data.tags.map(
          (tagId) =>
            this.availableTags.find((tag) => tag.id === tagId) || {
              id: tagId,
              name: "Unknown Tag",
            }
        );
      } catch (err) {
        if (err.response?.status === 401 && retry) {
          try {
            const refreshed = await this.refreshToken();
            if (refreshed) {
              return this.fetchProfile(false);
            } else {
              this.error = "Session expired. Please log in again.";
              this.$router.push("/AppLogin");
            }
          } catch (refreshError) {
            this.error = "Session expired. Please log in again.";
            this.$router.push("/AppLogin");
          }
        } else {
          this.error = "Failed to load profile data.";
        }
      } finally {
        this.loading = false;
      }
    },

    async updateProfile(formData) {
      console.log("Updating profile with data:", formData);

      try {
        // Get the profile ID from the user object
        const profileId = this.profile.user.id;
        if (!profileId) {
          throw new Error("Profile ID not found");
        }

        console.log("Profile ID:", profileId);

        // Make the API call to update the profile
        const response = await api.patch(
          `api/profiles/${profileId}/`,
          formData,
          {
            headers: this.getAuthHeader(),
          }
        );

        if (response.status === 200) {
          // Update was successful
          this.editing = false;
          await this.fetchProfile(); // Refresh the profile data
          alert("Profile updated successfully!");
        } else {
          console.error("Unexpected response status:", response.status);
          throw new Error("Failed to update profile");
        }
      } catch (error) {
        console.error("Error updating profile:", error);

        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.error("Error response data:", error.response.data);
          console.error("Error response status:", error.response.status);

          if (error.response.status === 401) {
            // Token might be expired, try to refresh
            try {
              const refreshed = await this.refreshToken();
              if (refreshed) {
                // Retry the update with the new token
                return this.updateProfile(formData);
              } else {
                this.error = "Session expired. Please log in again.";
                this.$router.push("/AppLogin");
              }
            } catch (refreshError) {
              this.error = "Session expired. Please log in again.";
              this.$router.push("/AppLogin");
            }
          } else if (error.response.status === 400) {
            // Bad request - show the error message from the server
            const errorMessage =
              error.response.data.detail ||
              "Invalid data provided. Please check your input.";
            this.error = errorMessage;
          } else {
            this.error = "Failed to update profile. Please try again.";
          }
        } else if (error.request) {
          // The request was made but no response was received
          console.error("No response received:", error.request);
          this.error = "No response from server. Please try again.";
        } else {
          // Something happened in setting up the request that triggered an Error
          console.error("Error setting up request:", error.message);
          this.error = "An error occurred. Please try again.";
        }
      }
    },

    getChangedFields(formData) {
      const changedFields = {};
      const fieldsToCheck = [
        "first_name",
        "last_name",
        "user_type",
        "phone_number",
        "street_address",
        "city",
        "state",
        "country",
        "years_of_experience",
        "description",
        "tags",
      ];

      fieldsToCheck.forEach((field) => {
        const newValue = formData[field];
        const oldValue = this.originalProfile[field];

        // Handle arrays (like tags) differently
        if (Array.isArray(newValue)) {
          if (
            JSON.stringify([...newValue].sort()) !==
            JSON.stringify([...oldValue].sort())
          ) {
            changedFields[field] = newValue;
          }
        } else if (newValue !== oldValue) {
          changedFields[field] = newValue;
        }
      });

      return changedFields;
    },

    async refreshToken() {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        return false;
      }

      try {
        const response = await api.post("/api/token/refresh/", {
          refresh: refreshToken,
        });
        localStorage.setItem("access_token", response.data.access);
        return true;
      } catch (err) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        return false;
      }
    },

    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      this.$router.push("/");
    },
  },
  created() {
    this.fetchProfile();
  },
};
</script>
