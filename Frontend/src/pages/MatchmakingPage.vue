<template>
  <div class="container">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="users.length == 0">
      <h3>
        Once you select tags, users you match with will appear on this page.
      </h3>
    </div>
    <div v-else class="profiles">
      <UserCard
        v-for="user in users"
        :key="user.user.id"
        :id="user.user.id"
        :first_name="user.first_name"
        :last_name="user.last_name"
        :city="user.city"
        :state="user.state"
        :country="user.country"
        :description="user.description"
        :tags="
          user.tags.map((tagId) => ({
            tag_name: tags[tagId],
            tag_description: '',
          }))
        "
        :user_type="user.user_type"
      />
    </div>
  </div>
</template>

<script>
import api from "@/api/axios.js";
import UserCard from "@/components/search/UserCard.vue";

export default {
  components: {
    UserCard,
  },
  data() {
    return {
      users: [],
      tags: {},
      loading: true,
      error: null,
    };
  },
  async mounted() {
    await this.fetchTags();
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers(retry = true) {
      const token = localStorage.getItem("access_token");
      try {
        const response = await api.get("api/profiles/match", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.users = response.data;
        console.log("Length: ", this.users.length);
      } catch (err) {
        if (err.response && err.response.status === 401 && retry) {
          // If 401, try refreshing the token
          await this.refreshToken();
          return this.fetchUsers(false); // Retry once with a new token
        }
        this.error = "Failed to fetch data";
      } finally {
        this.loading = false;
      }
    },
    async fetchTags() {
      try {
        const response = await api.get("tag/");
        this.tags = response.data.reduce((acc, tag) => {
          acc[tag.id] = tag.tag_name;
          return acc;
        }, {});
      } catch (err) {
        this.error = "Failed to fetch tags";
      }
    },

    async refreshToken() {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        this.logout();
        return;
      }

      try {
        const response = await api.post("api/token/refresh/", {
          refresh: refreshToken,
        });

        localStorage.setItem("access_token", response.data.access);
      } catch (err) {
        console.error("Token refresh failed", err);
        this.logout();
      }
    },
    logout() {
      // Clear tokens from localStorage
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      // Redirect to login
      this.$router.push("/");
    },
  },
};
</script>

<style>
body {
  background-color: #f3f4f6;
  font-family: Arial, sans-serif;
}
.container {
  padding: 20px;
}
.profiles {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.profile-card {
  background: white;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 300px;
}
.profile-picture {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
.error {
  color: red;
}
</style>
