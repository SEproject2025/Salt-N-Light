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
            />
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
        "denomination",
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

      const originalTagIds = this.originalProfile.tags.map((tag) => tag.id);
      if (
        JSON.stringify([...formData.tags].sort()) !==
        JSON.stringify([...originalTagIds].sort())
      ) {
        changedFields.tags = formData.tags;
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
