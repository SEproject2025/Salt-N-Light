<template>
  <div>
    <!-- Profile Completion Banner -->
    <div v-if="!isProfileComplete" class="profile-completion-banner">
      <span
        >Almost There! Let's Complete Your Profile {{ getCompletionText }}</span
      >
      <button class="finish-profile-btn" @click="finishProfile">
        Finish Your Profile
      </button>
    </div>

    <div class="home-page">
      <!-- Profile Section -->
      <div class="profile-section">
        <div class="profile-card">
          <img :src="userImage" alt="Profile Picture" class="profile-picture" />
          <h2>{{ profileName }}</h2>
          <p class="role">{{ userType }}</p>

          <!-- Recent Events -->
          <div class="recent-events">
            <h3>Recent Events</h3>
            <div
              v-for="(event, index) in recentEvents"
              :key="index"
              class="event"
            >
              <img :src="event.icon" alt="Event Icon" class="event-icon" />
              <p>{{ event.description }}</p>
            </div>
          </div>

          <button class="start-exploring-btn" @click="startExploring">
            Start Exploring
          </button>
        </div>
      </div>

      <!-- Main Content Section -->
      <div class="main-content">
        <!-- Recommendations Section -->
        <div class="recommendations">
          <h2>Recommended for You</h2>
          <div class="recommendation-cards">
            <UserCard
              v-for="org in limitedRecommendations"
              :key="org.id"
              :first_name="org.first_name"
              :last_name="org.last_name"
              :city="org.city"
              :state="org.state"
              :country="org.country"
              :description="org.description"
              :id="org.id"
            />
            <button
              v-if="hasMoreRecommendations"
              class="view-more-btn"
              @click="viewMore"
            >
              <i class="fas fa-plus"></i>
              <span>View More</span>
            </button>
          </div>
        </div>

        <!-- Support Section -->
        <div class="support-section">
          <h2>Churches Looking to Support</h2>
          <div class="support-cards">
            <UserCard
              v-for="org in limitedSupportOrgs"
              :key="org.id"
              :first_name="org.first_name"
              :last_name="org.last_name"
              :city="org.city"
              :state="org.state"
              :country="org.country"
              :description="org.description"
              :id="org.id"
            />
            <button
              v-if="hasMoreSupportOrgs"
              class="view-more-btn"
              @click="viewMore"
            >
              <i class="fas fa-plus"></i>
              <span>View More</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios.js";
import UserCard from "@/components/search/UserCard.vue";

export default {
  name: "HomePage",
  components: {
    UserCard,
  },
  setup() {
    const router = useRouter();
    const profileName = ref("");
    const userType = ref("");
    const userImage = ref("https://via.placeholder.com/120");
    const recentEvents = ref([]);
    const recommendedOrgs = ref([]);
    const supportOrgs = ref([]);
    const profileFields = ref({});
    const isProfileComplete = ref(true);
    const completionRatio = ref(0);

    // Required profile fields
    const requiredFields = [
      "first_name",
      "last_name",
      "user_type",
      "denomination",
      "phone_number",
      "street_address",
      "city",
      "state",
      "country",
      "description",
    ];

    // Computed properties for limited display
    const limitedRecommendations = computed(() => {
      return recommendedOrgs.value.slice(0, 3);
    });

    const limitedSupportOrgs = computed(() => {
      return supportOrgs.value.slice(0, 3);
    });

    const hasMoreRecommendations = computed(() => {
      return recommendedOrgs.value.length > 3;
    });

    const hasMoreSupportOrgs = computed(() => {
      return supportOrgs.value.length > 3;
    });

    const getCompletionText = computed(() => {
      if (completionRatio.value === 0) return "";
      return `(${Math.round(completionRatio.value * 100)}% Complete)`;
    });

    const calculateProfileCompletion = (profile) => {
      const filledFields = requiredFields.filter((field) => {
        return profile[field] && profile[field].toString().trim() !== "";
      });

      completionRatio.value = filledFields.length / requiredFields.length;
      isProfileComplete.value = completionRatio.value === 1;
    };

    const fetchUserProfile = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await api.get("api/profiles/me/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const profile = response.data;
        profileName.value = `${profile.first_name} ${profile.last_name}`;
        userType.value = profile.user_type;
        userImage.value =
          profile.profile_image || "https://via.placeholder.com/120";
        profileFields.value = profile;
        calculateProfileCompletion(profile);
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    };

    const fetchRecommendations = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await api.get("api/profiles/match", {
          headers: { Authorization: `Bearer ${token}` },
        });
        recommendedOrgs.value = response.data.map((org) => ({
          id: org.user.id,
          first_name: org.first_name,
          last_name: org.last_name,
          city: org.city,
          state: org.state,
          country: org.country,
          description: org.description || "No description available",
        }));
        supportOrgs.value = [...recommendedOrgs.value];
      } catch (error) {
        console.error("Error fetching recommendations:", error);
      }
    };

    onMounted(() => {
      fetchUserProfile();
      fetchRecommendations();
    });

    const startExploring = () => {
      router.push("/SearchPage");
    };

    const finishProfile = () => {
      router.push("/UserProfile");
    };

    const viewMore = () => {
      router.push("/Matchmaking");
    };

    return {
      profileName,
      userType,
      userImage,
      recentEvents,
      limitedRecommendations,
      limitedSupportOrgs,
      hasMoreRecommendations,
      hasMoreSupportOrgs,
      isProfileComplete,
      getCompletionText,
      startExploring,
      finishProfile,
      viewMore,
    };
  },
};
</script>

<style scoped>
.profile-completion-banner {
  position: fixed;
  top: 64px; /* Adjust based on your header height */
  left: 0;
  right: 0;
  background: #2196f3;
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
}

.finish-profile-btn {
  background: white;
  color: #2196f3;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.home-page {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  margin-top: 64px; /* Add margin to account for fixed banner */
}

.profile-section {
  width: 300px;
  flex-shrink: 0;
}

.profile-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-picture {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin: 0 auto 1rem;
  display: block;
  object-fit: cover;
}

.role {
  color: #666;
  text-align: center;
  margin-bottom: 2rem;
}

.recent-events {
  margin-top: 2rem;
}

.event {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.event-icon {
  width: 24px;
  height: 24px;
}

.start-exploring-btn {
  width: 100%;
  padding: 0.75rem;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  margin-top: 1rem;
}

.main-content {
  flex-grow: 1;
}

.recommendations,
.support-section {
  margin-bottom: 3rem;
}

.recommendation-cards,
.support-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.view-more-btn {
  background: #f5f5f5;
  border: none;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #666;
  height: 100%;
}

.view-more-btn i {
  font-size: 1.5rem;
}

@media (max-width: 1024px) {
  .home-page {
    flex-direction: column;
  }

  .profile-section {
    width: 100%;
  }
}
</style>
