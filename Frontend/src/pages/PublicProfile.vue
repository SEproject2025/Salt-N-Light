<template>
  <div class="profile-container">
    <div v-if="showSpinner" class="loading-spinner">
      <div class="spinner"></div>
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
import axios from "axios";
import PublicProfileView from "@/components/profile/PublicProfileView.vue";
import ProfileVotingSection from "@/components/profile/ProfileVotingSection.vue";
import { jwtDecode } from "jwt-decode";

const API_BASE_URL = "http://127.0.0.1:8000";

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
      showSpinner: false,
      spinnerTimeout: null,
      error: null,
      redirecting: false,
    };
  },
  watch: {
    loading(newVal) {
      if (newVal) {
        // Clear any existing timeout
        if (this.spinnerTimeout) {
          clearTimeout(this.spinnerTimeout);
        }
        // Set a new timeout to show spinner after 300ms
        this.spinnerTimeout = setTimeout(() => {
          if (this.loading) {
            this.showSpinner = true;
          }
        }, 300);
      } else {
        // Clear timeout and hide spinner when loading is done
        if (this.spinnerTimeout) {
          clearTimeout(this.spinnerTimeout);
        }
        this.showSpinner = false;
      }
    },
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
    async fetchProfile(profileId = null) {
      try {
        // Use provided profileId or get from current route
        const id = profileId || this.$route.params.id;
        const currentUserId = this.getCurrentUserId();

        // If the profile being viewed belongs to the current user, redirect to UserProfile
        if (currentUserId && parseInt(id) === currentUserId) {
          this.redirecting = true; // Set redirecting flag
          this.loading = false; // Stop loading
          await this.$router.push("/UserProfile");
          return;
        }

        const response = await axios.get(`${API_BASE_URL}/api/profiles/${id}/`);
        this.profile = response.data;
        this.loading = false;
      } catch (error) {
        console.error("Error fetching profile:", error);
        this.error = "Failed to load profile. Please try again.";
        this.loading = false;
      }
    },
  },
  beforeRouteUpdate(to, from, next) {
    // Reset loading state and fetch new profile data using the new route parameters
    this.loading = true;
    this.error = null;
    this.profile = {};
    this.fetchProfile(to.params.id);
    next();
  },
  async created() {
    try {
      // First try to get the current user's profile
      const token = localStorage.getItem("access_token");
      if (token) {
        const response = await axios.get(`${API_BASE_URL}/api/profiles/me/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const currentUserId = response.data.user.id;
        const profileId = this.$route.params.id;

        // If the profile being viewed belongs to the current user, redirect to UserProfile
        if (currentUserId === parseInt(profileId)) {
          this.redirecting = true;
          this.loading = false;
          await this.$router.push("/UserProfile");
          return;
        }
      }
      // If the /me/ endpoint fails, just try to fetch the profile
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
  align-items: center;
  justify-content: center;
  width: 100%;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
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
