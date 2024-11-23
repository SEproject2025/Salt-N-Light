<template>
  <div class="advanced-search-page">
    <h1>Advanced Search</h1>

    <!-- Search Form -->
    <form class="search-form" @submit.prevent="fetchSearchResults">
      <!-- Role Filter -->
      <div class="form-group">
        <label for="user_type">Role</label>
        <select id="user_type" v-model="filters.user_type">
          <option value="">All</option>
          <option value="Missionary">Missionary</option>
          <option value="Supporter">Supporter</option>
        </select>
      </div>

      <!-- Contains Field -->
      <div class="form-group">
        <label for="contains">Contains</label>
        <input
          type="text"
          id="contains"
          placeholder="Search for emails, descriptions, or phone numbers"
          v-model="filters.contains"
        />
      </div>

      <!--  Future placeholder = Search for names, places, or interests-->
      <!-- Denomination Field (Commented Out) -->
      <!--
      <div class="form-group">
        <label for="denomination">Denomination</label>
        <select id="denomination" v-model="filters.denomination">
          <option value="">-Select a denomination-</option>
          <option value="Catholic">Catholic</option>
          <option value="Protestant">Protestant</option>
          <option value="Non-Denominational">Non-Denominational</option>
        </select>
      </div>
      -->

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
      <button type="submit" class="search-button">Search</button>
    </form>

    <!-- Results Section -->
    <div class="results">
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
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchPage",
  data() {
    return {
      filters: {
        user_type: "", // Role filter (Missionary or Supporter)
        contains: "", // General search field for names, places, or interests
        // denomination: "", // Commented out
        // missionField: "", // Commented out
      },
      searchResults: [], // Combined API results
      isLoading: false, // Loading state indicator
      error: null, // Error message if request fails
    };
  },

  methods: {
    async fetchSearchResults() {
      this.isLoading = true;
      this.error = null;
      this.searchResults = [];

      try {
        // Fetch data from API endpoints
        const [usersResponse, supportersResponse, missionariesResponse] =
          await Promise.all([
            axios.get("http://127.0.0.1:8000/user/"),
            axios.get("http://127.0.0.1:8000/supporter/"),
            axios.get("http://127.0.0.1:8000/missionary/"),
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

          // const matchesDenomination =
          //   !this.filters.denomination ||
          //   (user.denomination && user.denomination === this.filters.denomination);

          // const matchesMissionField =
          //   !this.filters.missionField ||
          //   (user.mission_field && user.mission_field === this.filters.missionField);

          return matchesContains && matchesRole; // && matchesDenomination && matchesMissionField
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
</style>
