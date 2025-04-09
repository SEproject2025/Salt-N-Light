<template>
  <div class="quick-search">
    <div class="search-input-wrapper">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Quick search..."
        @input="handleInput"
        @focus="showResults = true"
        @blur="handleBlur"
      />
      <div class="search-icon">
        <i class="fas fa-search"></i>
      </div>
    </div>

    <div
      v-if="showResults && searchResults.length > 0"
      class="results-dropdown"
    >
      <div
        v-for="result in searchResults"
        :key="result.user.id"
        class="result-item"
        @click="handleResultSelect(result)"
      >
        <div class="result-content">
          <div class="name">{{ result.first_name }} {{ result.last_name }}</div>
          <div class="details">
            <span class="type">{{ result.user_type }}</span>
            <span v-if="result.city" class="location">
              {{ result.city }}, {{ result.state || result.country }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { debounce } from "lodash";
import searchService from "@/services/searchService";

export default {
  name: "QuickSearch",
  data() {
    return {
      searchQuery: "",
      searchResults: [],
      isLoading: false,
      showResults: false,
      searchTimeout: null,
    };
  },
  methods: {
    handleInput: debounce(async function () {
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        return;
      }

      this.isLoading = true;
      try {
        const response = await searchService.searchProfiles({
          q: this.searchQuery,
          page_size: 5,
        });

        console.log("QuickSearch - API Response:", response);
        this.searchResults = response.results || [];
        console.log("QuickSearch - Updated searchResults:", this.searchResults);
      } catch (error) {
        console.error("Quick search error:", error);
        this.searchResults = [];
      } finally {
        this.isLoading = false;
      }
    }, 300),

    handleBlur() {
      setTimeout(() => {
        this.showResults = false;
      }, 200);
    },

    handleResultSelect(profile) {
      console.log("QuickSearch - Selected profile:", profile);
      this.$router.push(`/profile/${profile.user.id}`);
      this.searchQuery = "";
      this.searchResults = [];
      this.showResults = false;
    },
  },
};
</script>

<style scoped>
.quick-search {
  position: relative;
  width: 300px;
}

.search-input-wrapper {
  position: relative;
}

.search-input-wrapper input {
  width: 100%;
  padding: 8px 32px 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
}

.search-input-wrapper input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.search-icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  pointer-events: none;
}

.results-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 4px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
}

.result-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.result-item:hover {
  background-color: #f5f5f5;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.name {
  font-weight: 500;
  color: #333;
}

.details {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #666;
}

.type {
  text-transform: capitalize;
}

.location {
  color: #666;
}
</style>
