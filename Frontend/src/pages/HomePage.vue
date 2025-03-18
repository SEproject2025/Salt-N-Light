<template>
  <div class="home-page">
    <!-- Complete Profile Banner -->
    <div v-if="!isProfileComplete" class="profile-completion-banner">
      <div class="banner-content">
        <span class="banner-icon">⭕</span>
        <span>Almost There! Let's Complete Your Profile (2/4)</span>
      </div>
      <button class="finish-profile-btn" @click="finishProfile">
        Finish Your Profile
      </button>
    </div>

    <div class="main-content">
      <!-- Left Column - Profile Summary -->
      <div class="left-column">
        <UserCard
          :first_name="userProfile.first_name"
          :last_name="userProfile.last_name"
          :city="userProfile.city || 'Unknown'"
          :state="userProfile.state || ''"
          :country="userProfile.country || ''"
          :description="userProfile.description || 'No description available'"
          :id="userProfile.id"
          :tags="userProfile.tags || []"
          :user_type="userProfile.role"
        />

        <!-- Recent Events Section -->
        <div class="recent-events-card">
          <div class="recent-events">
            <h3>Recent Events</h3>
            <div
              v-for="event in recentEvents"
              :key="event.id"
              class="event-item"
            >
              <span class="event-icon">🔔</span>
              <p class="event-text">{{ event.description }}</p>
            </div>
            <a href="#" class="see-all-link">See all</a>
          </div>

          <button class="start-exploring-btn" @click="startExploring">
            Start Exploring
          </button>
        </div>
      </div>

      <!-- Right Column - Recommendations -->
      <div class="right-column">
        <!-- Recommendations Section -->
        <section class="recommendations">
          <h2>Recommended for You</h2>
          <div class="church-cards-grid">
            <UserCard
              v-for="church in recommendations"
              :key="church.id"
              :first_name="church.name"
              :last_name="''"
              :city="getCity(church.location)"
              :state="''"
              :country="getCountry(church.location)"
              :description="church.description"
              :id="church.id"
              :tags="church.tags"
              :user_type="'Church'"
            />
          </div>
          <button class="view-more-btn" @click="navigateToMatchmaking">
            <span class="view-more-icon">+</span>
            <span>View More</span>
          </button>
        </section>

        <!-- Churches Looking to Support Section -->
        <section class="support-section">
          <h2>Churches Looking to Support</h2>
          <div class="church-cards-grid">
            <UserCard
              v-for="church in supportingChurches"
              :key="church.id"
              :first_name="church.name"
              :last_name="''"
              :city="getCity(church.location)"
              :state="''"
              :country="getCountry(church.location)"
              :description="church.description"
              :id="church.id"
              :tags="church.tags"
              :user_type="'Church'"
            />
          </div>
          <button class="view-more-btn" @click="navigateToMatchmaking">
            <span class="view-more-icon">+</span>
            <span>View More</span>
          </button>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import UserCard from "@/components/search/UserCard.vue";

export default {
  name: "HomePage",
  components: {
    UserCard,
  },
  setup() {
    const router = useRouter();
    const userProfile = ref({
      first_name: "",
      last_name: "",
      city: "",
      state: "",
      country: "",
      description: "",
      role: "",
      id: null,
      tags: [],
      image: null,
    });

    const isProfileComplete = ref(false);
    const recentEvents = ref([
      {
        id: 1,
        description:
          "Grace Fellowship Church celebrated 50 years in the ministry",
      },
      {
        id: 2,
        description: "David Cho celebrated 5 years of service in Amman, Jordan",
      },
      {
        id: 3,
        description:
          "Hope Community Church celebrated 25 years in the ministry",
      },
    ]);

    const recommendations = ref([]);
    const supportingChurches = ref([]);

    const getCity = (location) => {
      return location ? location.split(", ")[0] : "";
    };

    const getCountry = (location) => {
      return location ? location.split(", ")[1] : "";
    };

    const loadUserProfile = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/user/profile/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        // Update user profile with actual data
        userProfile.value = {
          first_name: response.data.first_name || "",
          last_name: response.data.last_name || "",
          city: response.data.city || "",
          state: response.data.state || "",
          country: response.data.country || "",
          description: response.data.description || "",
          role: response.data.role || "Missionary",
          id: response.data.id,
          tags: response.data.tags || [],
          image: response.data.profile_image || null,
        };

        // Check profile completion
        const requiredFields = ["first_name", "last_name", "email", "role"];
        const completedFields = requiredFields.filter(
          (field) => response.data[field]
        );
        isProfileComplete.value =
          completedFields.length === requiredFields.length;
      } catch (error) {
        console.error("Error loading user profile:", error);
      }
    };

    const loadRecommendations = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/profiles/match",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        // Transform the API response to match our UserCard component props
        recommendations.value = response.data.map((profile) => ({
          id: profile.id,
          name:
            profile.user_type === "Church"
              ? profile.church_name || profile.organization_name
              : `${profile.first_name} ${profile.last_name}`,
          location: `${profile.city}, ${profile.country}`,
          description: profile.description || "No description available",
          image: profile.profile_image,
          tags: profile.tags
            ? profile.tags.map((tag) => ({
                tag_name: tag.tag_name,
                tag_description: tag.description || tag.tag_name,
              }))
            : [],
        }));

        // For now, use the same data for supporting churches
        // In the future, this could be a different endpoint
        supportingChurches.value = recommendations.value.filter(
          (profile) => profile.user_type === "Church"
        );
      } catch (error) {
        console.error("Error loading recommendations:", error);
        // Set empty arrays if the request fails
        recommendations.value = [];
        supportingChurches.value = [];
      }
    };

    const startExploring = () => {
      router.push("/explore");
    };

    const finishProfile = () => {
      router.push("/profile/edit");
    };

    const viewProfile = (church) => {
      router.push(`/church/${church.id}`);
    };

    const toggleSave = (church) => {
      // Implement save functionality
      church.saved = !church.saved;
    };

    const navigateToMatchmaking = () => {
      router.push("/matchmaking");
    };

    onMounted(async () => {
      await loadUserProfile();
      await loadRecommendations();
    });

    return {
      userProfile,
      isProfileComplete,
      recentEvents,
      recommendations,
      supportingChurches,
      startExploring,
      finishProfile,
      viewProfile,
      toggleSave,
      navigateToMatchmaking,
      getCity,
      getCountry,
    };
  },
};
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.main-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  margin-top: 1rem;
}

.profile-completion-banner {
  background: #007bff;
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.finish-profile-btn {
  background: white;
  color: #007bff;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.left-column {
  position: sticky;
  top: 1rem;
  height: fit-content;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recent-events-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.recent-events {
  text-align: left;
  margin-bottom: 1rem;
}

.recent-events h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.event-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0.5rem 0;
  font-size: 0.875rem;
}

.see-all-link {
  color: #007bff;
  text-decoration: none;
  font-size: 0.875rem;
  display: block;
  margin-top: 0.5rem;
}

.start-exploring-btn {
  background: #007bff;
  color: white;
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
  width: 100%;
  margin-top: 1rem;
}

.right-column section {
  margin-bottom: 2rem;
}

section h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.church-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.view-more-btn {
  background: none;
  border: none;
  color: #007bff;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin: 0.5rem 0;
  padding: 0.5rem;
  font-size: 0.875rem;
}

.view-more-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  background: #f0f0f0;
  border-radius: 50%;
}
</style>
