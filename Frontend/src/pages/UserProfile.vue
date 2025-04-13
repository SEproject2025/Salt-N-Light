<template>
  <div class="profile-container">
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
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

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
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

        this.profile.tags = profileResponse.data.tags.map((tag) => {
          const matchedTag = this.availableTags.find((t) => t.id === tag.id);
          return (
            matchedTag || {
              id: tag.id,
              name: tag.tag_name || "Unknown Tag",
            }
          );
        });
      } catch (err) {
        console.error("Profile fetch error:", err);
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
            console.error("Token refresh error:", refreshError);
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
      try {
        const profileId = this.profile.user.id;
        const changedFields = this.getChangedFields(formData);

        if (Object.keys(changedFields).length === 0) {
          this.editing = false;
          return;
        }

        try {
          await this.sendProfileUpdate(profileId, changedFields);
          alert("Profile updated successfully!");
          this.editing = false;
          this.fetchProfile();
        } catch (err) {
          if (err.response?.status === 401 && (await this.refreshToken())) {
            await this.sendProfileUpdate(profileId, changedFields);
            alert("Profile updated successfully!");
            this.editing = false;
            this.fetchProfile();
          } else {
            this.error =
              err.response?.status === 401
                ? "Session expired. Please log in again."
                : "Failed to update profile.";
          }
        }
      } catch (err) {
        this.error = "Failed to update profile.";
      }
    },

    async sendProfileUpdate(profileId, data) {
      return api.patch(`api/profiles/${profileId}/`, data, {
        headers: this.getAuthHeader(),
      });
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
      ];

      fieldsToCheck.forEach((field) => {
        if (formData[field] !== this.originalProfile[field]) {
          changedFields[field] = formData[field];
        }
      });

      // Compare tag IDs for changes
      const originalTagIds = this.originalProfile.tags.map((tag) => tag.id);
      const newTagIds = formData.tags.map((tag) => tag.id);

      if (
        JSON.stringify([...newTagIds].sort()) !==
        JSON.stringify([...originalTagIds].sort())
      ) {
        changedFields.tags = newTagIds; // Send just the IDs
      }

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
        console.error("Token refresh failed:", err);
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
