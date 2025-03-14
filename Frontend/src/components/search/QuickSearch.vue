<template>
  <div class="quick-search" @mousedown.stop>
    <div class="search-input">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search by name, location, or tags..."
        @input="handleSearch"
        @keyup.enter="navigateToSearch"
        @focus="showFilters = true"
        @blur="handleBlur"
      />
      <div class="search-icon" @click="navigateToSearch">
        <i class="fas fa-search"></i>
      </div>
    </div>
    <div class="quick-filters" v-if="showFilters" @mousedown.stop>
      <div class="filter-group">
        <label>Role</label>
        <select v-model="userType" @change="handleSearch">
          <option value="">All Roles</option>
          <option value="missionary">Missionary</option>
          <option value="supporter">Supporter</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Location</label>
        <input
          type="text"
          v-model="location"
          placeholder="Street, City, State, or Country"
          @input="handleSearch"
        />
      </div>
      <div class="filter-group">
        <label>Tags</label>
        <multiselect
          v-model="selectedTags"
          :options="availableTags"
          :multiple="true"
          :close-on-select="false"
          :clear-on-select="false"
          :preserve-search="true"
          placeholder="Select tags"
          label="tag_name"
          track-by="tag_name"
          @input="handleSearch"
          :max-height="200"
          :show-labels="false"
        >
          <template #tag="{ option, remove }">
            <span class="custom-tag">
              {{ option.tag_name }}
              <span class="custom-tag-remove" @click="remove(option)"
                >&times;</span
              >
            </span>
          </template>
        </multiselect>
      </div>
      <div class="search-actions">
        <button class="advanced-search" @click="navigateToSearch">
          Advanced Search
        </button>
      </div>
    </div>
    <QuickSearchResults
      v-if="showResults && searchResults.length > 0"
      :results="searchResults"
      @view-all="navigateToSearch"
      @select-profile="handleProfileSelect"
      @mousedown.stop
    />
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import searchService from "@/services/searchService";
import QuickSearchResults from "./QuickSearchResults.vue";

export default {
  name: "QuickSearch",
  components: {
    Multiselect,
    QuickSearchResults,
  },
  data() {
    return {
      searchQuery: "",
      userType: "",
      location: "",
      selectedTags: [],
      availableTags: [],
      showFilters: false,
      showResults: false,
      searchResults: [],
      searchTimeout: null,
    };
  },
  created() {
    this.loadTags();
  },
  methods: {
    debounce(func, wait) {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        func.apply(this);
      }, wait);
    },
    handleSearch() {
      this.debounce(this.performSearch, 300);
    },
    async loadTags() {
      try {
        this.availableTags = await searchService.getTags();
      } catch (error) {
        console.error("Error loading tags:", error);
      }
    },
    async performSearch() {
      const params = {
        q: this.searchQuery,
        user_type: this.userType,
        location: this.location,
        tags: this.selectedTags.map((tag) => tag.tag_name),
        tag_match_type: "any",
        page_size: 5, // Limit results for quick search
      };

      try {
        const response = await searchService.searchProfiles(params);
        this.searchResults = response.results || [];
        this.showResults = true;
      } catch (error) {
        console.error("Search error:", error);
      }
    },
    navigateToSearch() {
      // Build query parameters for the search page
      const params = new URLSearchParams();
      if (this.searchQuery) params.append("q", this.searchQuery);
      if (this.userType) params.append("user_type", this.userType);
      if (this.location) params.append("location", this.location);
      if (this.selectedTags.length > 0) {
        this.selectedTags.forEach((tag) => params.append("tags", tag.tag_name));
      }

      // Navigate to search page with parameters
      this.$router.push({
        path: "/searchpage",
        query: Object.fromEntries(params),
      });
    },
    handleProfileSelect(profile) {
      this.$router.push(`/profile/${profile.user.id}`);
      this.showResults = false;
      this.showFilters = false;
    },
    handleBlur(event) {
      // Check if the related target is within the quick-search component
      if (!event.relatedTarget || !this.$el.contains(event.relatedTarget)) {
        setTimeout(() => {
          this.showFilters = false;
          this.showResults = false;
        }, 200);
      }
    },
    clearSearch() {
      this.searchQuery = "";
      this.userType = "";
      this.location = "";
      this.selectedTags = [];
      this.handleSearch();
    },
  },
  beforeUnmount() {
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
    }
  },
};
</script>

<style scoped>
@import "vue-multiselect/dist/vue-multiselect.css";

.quick-search {
  position: relative;
  width: 100%;
  max-width: 600px;
}

.search-input {
  position: relative;
  width: 100%;
}

.search-input input {
  width: 100%;
  padding: 8px 36px 8px 12px;
  font-size: 14px;
  border: 2px solid #e0e0e0;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.search-input input:focus {
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
  outline: none;
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  cursor: pointer;
}

.quick-filters {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 8px;
  z-index: 1000;
}

.filter-group {
  margin-bottom: 12px;
}

.filter-group label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: #666;
  margin-bottom: 4px;
}

.filter-group select,
.filter-group input {
  width: 100%;
  padding: 6px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
}

.search-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
}

.advanced-search {
  background: #1976d2;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.advanced-search:hover {
  background: #1565c0;
}

/* Custom multiselect styling */
.multiselect {
  min-height: 36px;
}

.multiselect__tags {
  min-height: 36px;
  padding: 4px 40px 0 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.multiselect__tag {
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 100px;
  padding: 2px 20px 2px 8px;
  margin: 2px;
}

.custom-tag {
  display: inline-flex;
  align-items: center;
  font-size: 12px;
}

.custom-tag-remove {
  margin-left: 4px;
  cursor: pointer;
  font-size: 14px;
}
</style>
