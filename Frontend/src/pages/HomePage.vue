<template>
  <div class="home-page">
    <!-- Complete Profile Banner -->
    <div v-if="!isProfileComplete" class="profile-completion-banner">
      <div class="banner-content">
        <span class="banner-icon">⭕</span>
        <span
          >Almost There! Let's Complete Your Profile ({{
            profileCompletion.completed
          }}/{{ profileCompletion.total }})</span
        >
        <div
          v-if="profileCompletion.missingFields.length > 0"
          class="missing-fields"
        >
          Missing: {{ profileCompletion.missingFields.join(", ") }}
        </div>
      </div>
      <button class="finish-profile-btn" @click="finishProfile">
        Finish Your Profile
      </button>
    </div>

    <div class="main-content">
      <!-- Left Column - Profile Summary -->
      <div class="left-column">
        <div v-if="isLoading.profile" class="loading-state">
          Loading profile...
        </div>
        <div v-else-if="error.profile" class="error-state">
          {{ error.profile }}
        </div>
        <UserCard
          v-else
          :first_name="userProfile.first_name"
          :last_name="userProfile.last_name"
          :city="userProfile.city"
          :state="userProfile.state"
          :country="userProfile.country"
          :description="userProfile.description"
          :id="userProfile.id"
          :tags="userProfile.tags"
          :user_type="userProfile.role"
        />

        <!-- Recent Events Section -->
        <div class="recent-events-card">
          <div class="recent-events">
            <h3>Recent Events</h3>
            <div v-if="isLoading.notifications" class="loading-state">
              Loading events...
            </div>
            <div v-else-if="error.notifications" class="error-state">
              {{ error.notifications }}
            </div>
            <div v-else-if="recentEvents.length === 0" class="no-events">
              No recent events
            </div>
            <div v-else>
              <div
                v-for="event in recentEvents"
                :key="event.id"
                class="event-item"
              >
                <span class="event-icon">🔔</span>
                <p class="event-text">{{ event.description }}</p>
                <span class="event-date">{{
                  new Date(event.date).toLocaleDateString()
                }}</span>
              </div>
              <a href="#" class="see-all-link">See all</a>
            </div>
          </div>

          <button class="start-exploring-btn" @click="startExploring">
            Start Exploring
          </button>
        </div>

        <!-- Friends Section -->
        <div class="friends-card">
          <div class="friends">
            <h3>Your Friends</h3>
            <div v-if="isLoading.friends" class="loading-state">
              Loading friends...
            </div>
            <div v-else-if="error.friends" class="error-state">
              {{ error.friends }}
            </div>
            <div v-else-if="friends.length === 0" class="no-friends">
              No friends yet
            </div>
            <div v-else class="friends-list">
              <UserCard
                v-for="friend in friends"
                :key="friend.id"
                :first_name="friend.name"
                :last_name="''"
                :city="friend.city"
                :state="friend.state"
                :country="friend.country"
                :description="friend.description"
                :id="friend.id"
                :tags="
                  friend.tags.map((tag) => ({
                    ...tag,
                    tag_name: tag.tag_name || tag.name || 'Unknown Tag',
                  }))
                "
                :user_type="'Friend'"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column - Recommendations -->
      <div class="right-column">
        <!-- Recommendations Section -->
        <section class="recommendations">
          <h2>Recommended for You</h2>
          <div v-if="isLoading.recommendations" class="loading-state">
            Loading recommendations...
          </div>
          <div v-else-if="error.recommendations" class="error-state">
            {{ error.recommendations }}
          </div>
          <div v-else class="church-cards-grid">
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
              :tags="
                church.tags.map((tag) => ({
                  ...tag,
                  tag_name: tag.tag_name || tag.name || 'Unknown Tag',
                }))
              "
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
import api from "@/api/axios.js";
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
    const profileCompletion = ref({
      total: 0,
      completed: 0,
      missingFields: [],
    });
    const isLoading = ref({
      profile: false,
      recommendations: false,
      notifications: false,
      friends: false,
    });
    const error = ref({
      profile: null,
      recommendations: null,
      notifications: null,
      friends: null,
    });
    const recentEvents = ref([]);
    const friends = ref([]);

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
        isLoading.value.profile = true;
        error.value.profile = null;

        const response = await api.get("api/profiles/me/");

        if (!response.data) {
          throw new Error("No data received from server");
        }

        // Update user profile with actual data
        userProfile.value = {
          first_name: response.data.first_name || "",
          last_name: response.data.last_name || "",
          city: response.data.city || "",
          state: response.data.state || "",
          country: response.data.country || "",
          description: response.data.description || "",
          role: response.data.role || "",
          id: response.data.id,
          tags: response.data.tags || [],
          image:
            response.data.profile_image || "/assets/images/default-avatar.png",
        };

        // Check profile completion based on database fields
        const requiredFields = [
          { name: "first_name", label: "First Name" },
          { name: "last_name", label: "Last Name" },
          { name: "email", label: "Email" },
          { name: "role", label: "Role" },
          { name: "city", label: "City" },
          { name: "country", label: "Country" },
          { name: "description", label: "Bio" },
        ];

        // Count completed fields (non-null and non-empty)
        const completedFields = requiredFields.filter((field) => {
          const value = response.data[field.name];
          return (
            value !== null &&
            value !== undefined &&
            value.toString().trim() !== ""
          );
        });

        // Update profile completion status
        profileCompletion.value = {
          total: requiredFields.length,
          completed: completedFields.length,
          missingFields: requiredFields
            .filter((field) => {
              const value = response.data[field.name];
              return (
                value === null ||
                value === undefined ||
                value.toString().trim() === ""
              );
            })
            .map((field) => field.label),
        };

        // Profile is considered complete if at least 4 fields are filled
        isProfileComplete.value = completedFields.length >= 4;
      } catch (err) {
        console.error("Error loading user profile:", err);
        error.value.profile =
          err.message || "Failed to load profile. Please try again later.";
      } finally {
        isLoading.value.profile = false;
      }
    };

    const loadRecommendations = async () => {
      try {
        isLoading.value.recommendations = true;
        error.value.recommendations = null;

        const response = await api.get("api/profiles/match");

        if (!response.data) {
          throw new Error("No data received from server");
        }

        // Transform the API response with enhanced fallbacks
        recommendations.value = response.data.map((profile) => ({
          id: profile.id,
          name:
            profile.user_type === "Church"
              ? profile.church_name ||
                profile.organization_name ||
                "Unnamed Church"
              : `${profile.first_name || "Anonymous"} ${
                  profile.last_name || ""
                }`,
          location:
            profile.city && profile.country
              ? `${profile.city}, ${profile.country}`
              : "Location not specified",
          description: profile.description || "No description available",
          image: profile.profile_image || "/assets/images/default-church.png",
          tags: profile.tags
            ? profile.tags.map((tag) => ({
                tag_name: tag.tag_name || "Untagged",
                tag_description:
                  tag.description || tag.tag_name || "No description",
              }))
            : [],
        }));
      } catch (err) {
        console.error("Error loading recommendations:", err);
        error.value.recommendations =
          err.message ||
          "Failed to load recommendations. Please try again later.";
        recommendations.value = [];
      } finally {
        isLoading.value.recommendations = false;
      }
    };

    const loadNotifications = async () => {
      try {
        isLoading.value.notifications = true;
        error.value.notifications = null;

        const response = await api.get("api/notifications/");

        if (!response.data) {
          throw new Error("No data received from server");
        }

        // Transform notifications into events format
        recentEvents.value = response.data.slice(0, 3).map((notification) => ({
          id: notification.id,
          description: notification.message,
          type: notification.notification_type,
          date: notification.created_at,
        }));
      } catch (err) {
        console.error("Error loading notifications:", err);
        error.value.notifications =
          err.message ||
          "Failed to load notifications. Please try again later.";
        recentEvents.value = []; // Clear events on error
      } finally {
        isLoading.value.notifications = false;
      }
    };

    const loadFriends = async () => {
      try {
        isLoading.value.friends = true;
        error.value.friends = null;

        const response = await api.get("friendships/");

        if (!response.data) {
          throw new Error("No data received from server");
        }

        // Filter accepted friendships and get friend profiles
        const acceptedFriendships = response.data.filter(
          (friendship) => friendship.status === "accepted"
        );

        // Get friend profiles
        const friendProfiles = await Promise.all(
          acceptedFriendships.map(async (friendship) => {
            const friendId =
              friendship.sender === userProfile.value.id
                ? friendship.receiver
                : friendship.sender;

            try {
              const profileResponse = await api.get(
                `api/profiles/${friendId}/`
              );
              return {
                id: profileResponse.data.id,
                name: `${profileResponse.data.first_name} ${profileResponse.data.last_name}`,
                city: profileResponse.data.city || "",
                state: profileResponse.data.state || "",
                country: profileResponse.data.country || "",
                description:
                  profileResponse.data.description ||
                  "No description available",
                image:
                  profileResponse.data.profile_image ||
                  "/assets/images/default-avatar.png",
                tags: profileResponse.data.tags || [],
              };
            } catch (err) {
              console.error(`Error loading friend profile ${friendId}:`, err);
              return null;
            }
          })
        );

        friends.value = friendProfiles.filter((profile) => profile !== null);
      } catch (err) {
        console.error("Error loading friends:", err);
        error.value.friends =
          err.message || "Failed to load friends. Please try again later.";
        friends.value = [];
      } finally {
        isLoading.value.friends = false;
      }
    };

    const startExploring = () => {
      router.push("/explore");
    };

    const finishProfile = () => {
      router.push("/UserProfile");
    };

    const navigateToMatchmaking = () => {
      router.push("/matchmaking");
    };

    onMounted(async () => {
      await loadUserProfile();
      await loadRecommendations();
      await loadNotifications();
      await loadFriends();
    });

    return {
      userProfile,
      isProfileComplete,
      profileCompletion,
      recentEvents,
      recommendations,
      supportingChurches,
      startExploring,
      finishProfile,
      navigateToMatchmaking,
      getCity,
      getCountry,
      isLoading,
      error,
      friends,
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
  padding: 0.5rem;
  border-radius: 0.25rem;
  background: #f8f9fa;
}

.event-item:hover {
  background: #f1f3f5;
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

.loading-state {
  padding: 1rem;
  text-align: center;
  color: #666;
  background: #f5f5f5;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.error-state {
  padding: 1rem;
  text-align: center;
  color: #dc3545;
  background: #fff5f5;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.missing-fields {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}

.event-date {
  font-size: 0.75rem;
  color: #666;
  margin-left: auto;
}

.no-events {
  text-align: center;
  color: #666;
  padding: 1rem;
  font-style: italic;
}

.friends-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
}

.friends-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.no-friends {
  text-align: center;
  color: #666;
  padding: 1rem;
  font-style: italic;
}
</style>
