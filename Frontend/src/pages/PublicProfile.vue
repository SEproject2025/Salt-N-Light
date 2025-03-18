<template>
  <div class="profile-container">
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="!redirecting" class="profile-layout">
      <div class="content-wrapper">
        <PublicProfileView :profile="profile" />
        <ProfileVotingSection
          :profile="profile"
          @vote-updated="fetchProfile"
          @comment-added="fetchProfile"
        />
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios.js";
import PublicProfileView from "@/components/profile/PublicProfileView.vue";
import ProfileVotingSection from "@/components/profile/ProfileVotingSection.vue";
import { jwtDecode } from "jwt-decode";

export default {
  name: "PublicProfile",
  components: {
    PublicProfileView,
    ProfileVotingSection,
  },
  data() {
    return {
      profile: {},
      loading: true,
      error: null,
      redirecting: false,
    };
  },
  methods: {
    getCurrentUserId() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const decodedToken = jwtDecode(token);
        return decodedToken.user_id;
      }
      return null;
    },
    async fetchProfile() {
      try {
        const profileId = this.$route.params.id;
        const currentUserId = this.getCurrentUserId();

        // If the profile being viewed belongs to the current user, redirect to UserProfile
        if (currentUserId && parseInt(profileId) === currentUserId) {
          this.redirecting = true; // Set redirecting flag
          this.loading = false; // Stop loading
          await this.$router.push("/UserProfile");
          return;
        }

        const [profileResponse, tagResponse] = await Promise.all([
          api.get(`api/profiles/${profileId}/`),
          api.get(`tag/`),
        ]);

        // Get the profile data
        const profileData = profileResponse.data;

        // Map the tags using the tag response data
        const availableTags = tagResponse.data.map((tag) => ({
          id: tag.id,
          name: tag.tag_name,
        }));

        // Map the profile tags to include the full tag information
        profileData.tags = profileData.tags.map(
          (tagId) =>
            availableTags.find((tag) => tag.id === tagId) || {
              id: tagId,
              name: "Unknown Tag",
            }
        );

        this.profile = profileData;
      } catch (err) {
        console.error("Failed to load profile:", err);
        this.error = "Failed to load profile data.";
      } finally {
        if (!this.redirecting) {
          this.loading = false;
        }
      }
    },
  },
  beforeRouteEnter(to, from, next) {
    // Always call next() once and handle the redirect in the component
    next();
  },
  async created() {
    try {
      // Try to get the current user's profile first
      const token = localStorage.getItem("access_token");
      if (token) {
        const response = await api.get(`/api/profiles/me/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        // If the profile ID matches the route param, redirect
        if (response.data.user.id === parseInt(this.$route.params.id)) {
          this.redirecting = true;
          this.loading = false;
          this.$router.push("/UserProfile");
          return;
        }
      }

      // If we get here, either there's no token or it's not the user's profile
      await this.fetchProfile();
    } catch (error) {
      // If the /me/ endpoint fails, just try to fetch the profile
      await this.fetchProfile();
    }
  },
};
</script>

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
}

.back-btn {
  position: absolute;
  top: 0;
  left: 0;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #3498db;
  color: white;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #2980b9;
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

@media (max-width: 1200px) {
  .content-wrapper {
    flex-direction: column;
  }
}
</style>
