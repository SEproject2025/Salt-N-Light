<template>
  <!--
   <div class="advanced-search-page">
     <h1>Advanced Search</h1>
 -->
  <!-- Search Form -->
  <!--<form class="search-form" @submit.prevent="fetchSearchResults">
       Role Filter -->
  <!--<div class="form-group">
         <label for="user_type">Role</label>
         <select id="user_type" v-model="filters.user_type">
           <option value="">All</option>
           <option value="Missionary">Missionary</option>
           <option value="Supporter">Supporter</option>
         </select>
       </div>
 
        Contains Field -->
  <!--<div class="form-group">
         <label for="contains">Contains</label>
         <input
           type="text"
           id="contains"
           placeholder="Search for emails, descriptions, or phone numbers"
           v-model="filters.contains"
         />
       </div>
 -->
  <!--  Future placeholder = Search for names, places, or interests-->

  <!-- Mission Field (Commented Out) -->
  <!--
       <div class="form-group">
         <label for="missionField">Mission Field</label>
         <select id="missionField" v-model="filters.missionField">
           <option value="">-Select a field-</option>
           <option value="Youth">Youth</option>
           <option value="Education">Education</option>
           <option value="Medical">Medical</option>
         </select>
       </div>
       -->

  <!-- Search Button -->
  <!--      <button type="submit" class="search-button">Search</button>
     </form>
 -->
  <!-- Results Section -->
  <!--<div class="results">
       <h2>Search Results</h2>
       <p v-if="isLoading">Loading...</p>
       <p v-if="error">{{ error }}</p>
       <ul v-if="searchResults.length > 0">
         <li v-for="result in searchResults" :key="result.id">
           <strong>{{ result.email }}</strong> - {{ result.user_type }}<br />
           <span>{{ result.description || "No description" }}</span
           ><br />
           <span>{{ result.phone_number || "No phone number" }}</span
           ><br />
           <hr />
         </li>
       </ul>
       <p v-if="!isLoading && searchResults.length === 0">No results found.</p>
     </div>-->
  <!--</div>-->

  <div class="user-list">
    <h2>Users</h2>
    <div class="card-container">
      <!-- Loop through the users array and pass data to the Card component -->
      <UserCard
        v-for="user in users"
        :key="user.id"
        :id="user.user.id"
        :first_name="user.first_name"
        :last_name="user.last_name"
        :city="user.city"
        :state="user.state"
        :country="user.country"
        :description="user.description"
      />
    </div>
  </div>
</template>

<script>
import api from "@/api/axios.js";
import UserCard from "@/components/search/UserCard.vue";

export default {
  name: "SearchPage" & "UserList",
  components: {
    UserCard,
  },
  data() {
    return {
      users: [],
      filters: {
        user_type: "", // Role filter (Missionary or Supporter)
        contains: "", // General search field for names, places, or interests
        // missionField: "", // Commented out
      },
      searchResults: [], // Combined API results
      isLoading: false, // Loading state indicator
      error: null, // Error message if request fails
    };
  },
  mounted() {
    this.fetchUsers();
  },

  methods: {
    async fetchUsers() {
      try {
        const response = await api.get("api/profiles");
        console.log("API Response:", response.data);
        this.users = response.data;
        console.log("First user data:", this.users[0]);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    async fetchSearchResults() {
      this.isLoading = true;
      this.error = null;
      this.searchResults = [];

      try {
        // Fetch data from API endpoints
        const [usersResponse, supportersResponse, missionariesResponse] =
          await Promise.all([
            api.get("api/profiles"),
            api.get("api/profiles"),
            api.get("api/profiles/"),
          ]);

        const users = usersResponse.data;
        const supporters = supportersResponse.data;
        const missionaries = missionariesResponse.data;

        // Combine user data with supporter or missionary details
        const mergedResults = users.map((user) => {
          if (user.user_type === "Supporter") {
            const supporter = supporters.find((s) => s.user === user.id);
            return { ...user, ...supporter };
          } else if (user.user_type === "Missionary") {
            const missionary = missionaries.find((m) => m.user === user.id);
            return { ...user, ...missionary };
          } else {
            return user;
          }
        });

        // Apply filters
        const filteredResults = mergedResults.filter((user) => {
          // Exclude non-relevant user types (e.g., Admin roles)
          if (
            user.user_type !== "Missionary" &&
            user.user_type !== "Supporter"
          ) {
            return false;
          }
          const matchesContains =
            !this.filters.contains ||
            (user.description &&
              user.description
                .toLowerCase()
                .includes(this.filters.contains.toLowerCase())) ||
            (user.phone_number &&
              user.phone_number.includes(this.filters.contains)) ||
            (user.email &&
              user.email
                .toLowerCase()
                .includes(this.filters.contains.toLowerCase()));

          const matchesRole =
            !this.filters.user_type ||
            user.user_type === this.filters.user_type;

          return matchesContains && matchesRole;
        });

        this.searchResults = filteredResults;
      } catch (error) {
        this.error = "Failed to load search results.";
        console.error("API Error:", error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.advanced-search-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  border-radius: 10px;
  border: 1px solid #ddd;
}

h1 {
  font-size: 1.8em;
  margin-bottom: 20px;
  text-align: center;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input,
select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1em;
}

.search-button {
  padding: 10px;
  font-weight: bold;
  color: #fff;
  background-color: #000;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.search-button:hover {
  background-color: #444;
}

.results {
  margin-top: 20px;
}

.results h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px 0;
}

hr {
  border: 0;
  border-top: 1px solid #ddd;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
}

.user-card {
  width: 300px;
  height: auto;
  width: 90%;
}
</style>
