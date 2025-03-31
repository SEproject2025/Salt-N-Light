<template>
  <div class="search-page">
    <div class="search-container">
      <!-- Search Form -->
      <div class="search-form">
        <div class="search-input">
          <input
            type="text"
            v-model="searchParams.q"
            placeholder="Search by name, location, description, or tags..."
            @input="handleSearch"
          />
          <div class="search-icon">
            <i class="fas fa-search"></i>
          </div>
        </div>

        <div class="filters">
          <div class="filter-group">
            <label>Role</label>
            <select v-model="searchParams.user_type" @change="handleSearch">
              <option value="">All Roles</option>
              <option value="missionary">Missionary</option>
              <option value="supporter">Supporter</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Location</label>
            <input
              type="text"
              v-model="searchParams.location"
              placeholder="Street, City, State, or Country"
              @input="handleSearch"
            />
          </div>

          <div class="filter-group tags-select">
            <label>Tags</label>
            <div class="tags-control">
              <multiselect
                v-model="selectedTags"
                :options="availableTags"
                :multiple="true"
                :close-on-select="false"
                :clear-on-select="false"
                :preserve-search="true"
                placeholder="Select interests, skills, or ministries"
                label="tag_name"
                track-by="tag_name"
                @input="handleSearch"
                :max-height="300"
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
                <template #option="{ option }">
                  <div class="tag-option">
                    <span class="tag-name">{{ option.tag_name }}</span>
                    <small
                      v-if="option.tag_description"
                      class="tag-description"
                    >
                      {{ option.tag_description }}
                    </small>
                  </div>
                </template>
              </multiselect>
              <div class="tag-match-type" v-if="selectedTags.length > 0">
                <!-- Temporarily commented out match type selector
                <label>Match:</label>
                <select v-model="tagMatchType" @change="handleSearch">
                  <option value="any">Any Tag (OR)</option>
                  <option value="all">All Tags (AND)</option>
                </select>
                -->
              </div>
            </div>
          </div>
        </div>

        <div class="active-filters" v-if="hasActiveFilters">
          <span class="filter-label">Active Filters:</span>
          <div class="filter-tags">
            <span v-if="searchParams.q" class="filter-tag">
              Search: {{ searchParams.q }}
              <button @click="clearSearch">&times;</button>
            </span>
            <span v-if="searchParams.user_type" class="filter-tag">
              Role: {{ searchParams.user_type }}
              <button @click="clearUserType">&times;</button>
            </span>
            <span v-if="searchParams.location" class="filter-tag">
              Location: {{ searchParams.location }}
              <button @click="clearLocation">&times;</button>
            </span>
            <span v-for="tag in selectedTags" :key="tag.id" class="filter-tag">
              Tag: {{ tag.tag_name }}
              <button @click="removeTag(tag)">&times;</button>
            </span>
            <button
              v-if="hasActiveFilters"
              class="clear-all"
              @click="clearAllFilters"
            >
              Clear All Filters
            </button>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div class="search-results">
        <div v-if="isLoading" class="loading">
          <div class="loading-spinner"></div>
          <p>Finding profiles...</p>
        </div>
        <div v-else-if="error" class="error">
          {{ error }}
          <button @click="retrySearch" class="retry-button">Try Again</button>
        </div>
        <div v-else>
          <div class="results-header" v-if="totalResults > 0">
            <h2>
              {{ totalResults }} Profile{{ totalResults !== 1 ? "s" : "" }}
              Found
            </h2>
            <div class="controls">
              <div class="sort-controls">
                <label>Sort by:</label>
                <select v-model="sortBy" @change="handleSort">
                  <option value="recent">Most Recent</option>
                  <option value="name">Name (A-Z)</option>
                  <option value="location">Location</option>
                </select>
              </div>
              <div class="page-size-controls">
                <label>Show:</label>
                <select v-model="pageSize" @change="handlePageSizeChange">
                  <option value="all">Show All</option>
                  <option value="12">12 per page</option>
                  <option value="24">24 per page</option>
                  <option value="48">48 per page</option>
                </select>
              </div>
            </div>
          </div>
          <div
            v-if="!searchResults || searchResults.length === 0"
            class="no-results"
          >
            <h3>No profiles found</h3>
            <p>Try adjusting your search criteria or clearing some filters</p>
          </div>
          <div v-else class="results-grid">
            <UserCard
              v-for="profile in searchResults"
              :key="profile.user.id"
              :id="profile.user.id"
              :first_name="profile.first_name"
              :last_name="profile.last_name"
              :city="profile.city"
              :state="profile.state"
              :country="profile.country"
              :description="profile.description"
              :tags="profile.tags || []"
              :user_type="profile.user_type"
              class="user-card"
            />
          </div>
          <div class="pagination" v-if="totalPages > 1">
            <button
              :disabled="currentPage === 1"
              @click="changePage(currentPage - 1)"
              class="page-button"
            >
              Previous
            </button>
            <span class="page-info"
              >Page {{ currentPage }} of {{ totalPages }}</span
            >
            <button
              :disabled="currentPage === totalPages"
              @click="changePage(currentPage + 1)"
              class="page-button"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserCard from "@/components/search/UserCard.vue";
import searchService from "@/services/searchService";
import Multiselect from "vue-multiselect";

export default {
  name: "SearchPage",
  components: {
    UserCard,
    Multiselect,
  },
  data() {
    return {
      searchParams: {
        q: "",
        user_type: "",
        location: "",
      },
      selectedTags: [],
      tagMatchType: "any",
      availableTags: [],
      searchResults: [],
      isLoading: false,
      error: null,
      searchTimeout: null,
      currentPage: 1,
      totalPages: 1,
      totalResults: 0,
      sortBy: "recent",
      pageSize: 12,
      isInitialLoad: true,
      tagsLoaded: false,
    };
  },
  computed: {
    hasActiveFilters() {
      return (
        this.searchParams.q ||
        this.searchParams.user_type ||
        this.searchParams.location ||
        this.selectedTags.length > 0
      );
    },
  },
  async created() {
    if (!this.tagsLoaded) {
      await this.loadTags();
      this.tagsLoaded = true;
    }
    this.initializeFromQuery();
    // Always perform initial search, even with empty fields
    await this.performSearch();
  },
  methods: {
    debounce(func, wait) {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        func.apply(this);
      }, wait);
    },
    handleSearch() {
      if (this.isLoading) return;

      this.currentPage = 1; // Reset to first page on new search
      this.debounce(this.performSearch, 500);
    },
    handleSort() {
      if (this.isLoading) return;
      this.currentPage = 1;
      this.performSearch();
    },
    handlePageSizeChange() {
      if (this.isLoading) return;
      this.currentPage = 1;
      this.performSearch();
    },
    async loadTags() {
      try {
        this.availableTags = await searchService.getAllTags();
      } catch (error) {
        console.error("Error loading tags:", error);
      }
    },
    async performSearch() {
      if (this.isLoading) return;

      this.isLoading = true;
      this.error = null;

      try {
        // Create a clean params object with only non-empty values
        const params = {
          page: this.currentPage,
          sort: this.sortBy,
          page_size: this.pageSize,
        };

        // Only add non-empty search parameters
        if (this.searchParams.q) params.q = this.searchParams.q;
        if (this.searchParams.user_type)
          params.user_type = this.searchParams.user_type;
        if (this.searchParams.location)
          params.location = this.searchParams.location;

        // Add tags if any are selected
        if (this.selectedTags.length > 0) {
          params.tags = this.selectedTags.map((tag) => tag.tag_name);
          params.tag_match_type = this.tagMatchType;
        }

        console.log("Search params:", params); // Debug log

        const response = await searchService.searchProfiles(params);
        this.searchResults = response.results || [];
        this.totalResults = response.count || 0;
        this.totalPages = Math.ceil((response.count || 0) / this.pageSize);

        // Update URL with current search parameters
        this.updateURL(params);
      } catch (error) {
        if (error.response?.status === 401) {
          this.error = "Please log in to continue";
          setTimeout(() => {
            this.$router.push("/AppLogin");
          }, 2000);
        } else {
          this.error = "An error occurred while searching. Please try again.";
          console.error("Search error:", error);
        }
        this.searchResults = [];
        this.totalPages = 1;
        this.totalResults = 0;
      } finally {
        this.isLoading = false;
      }
    },
    updateURL(params) {
      const query = {};
      if (params.q) query.q = params.q;
      if (params.user_type) query.user_type = params.user_type;
      if (params.location) query.location = params.location;
      if (params.tags) query.tags = params.tags;
      if (params.tag_match_type) query.tag_match_type = params.tag_match_type;
      if (params.sort) query.sort = params.sort;
      if (params.page_size) query.page_size = params.page_size;

      this.$router.replace({
        query: query,
      });
    },
    initializeFromQuery() {
      const query = this.$route.query;

      // Set search parameters from query
      if (query.q) this.searchParams.q = query.q;
      if (query.user_type) this.searchParams.user_type = query.user_type;
      if (query.location) this.searchParams.location = query.location;

      // Set tags from query
      if (query.tags) {
        const tagNames = Array.isArray(query.tags) ? query.tags : [query.tags];
        this.selectedTags = tagNames.map((tagName) => ({
          tag_name: tagName,
          id: tagName,
        }));
      }

      // Set other parameters
      if (query.sort) this.sortBy = query.sort;
      if (query.page_size) this.pageSize = parseInt(query.page_size);
      if (query.tag_match_type) this.tagMatchType = query.tag_match_type;
    },
    changePage(page) {
      this.currentPage = page;
      this.performSearch();
      this.$nextTick(() => {
        this.$el
          .querySelector(".search-results")
          .scrollIntoView({ behavior: "smooth" });
      });
    },
    clearSearch() {
      this.searchParams.q = "";
      this.handleSearch();
    },
    clearUserType() {
      this.searchParams.user_type = "";
      this.handleSearch();
    },
    clearLocation() {
      this.searchParams.location = "";
      this.handleSearch();
    },
    removeTag(tag) {
      this.selectedTags = this.selectedTags.filter((t) => t.id !== tag.id);
      this.handleSearch();
    },
    clearAllFilters() {
      this.searchParams.q = "";
      this.searchParams.user_type = "";
      this.searchParams.location = "";
      this.selectedTags = [];
      this.$router.replace({
        path: this.$route.path,
      });
      this.handleSearch();
    },
    retrySearch() {
      this.performSearch();
    },
  },
  watch: {
    // Consolidate all search parameter watchers into a single watcher
    searchParams: {
      handler(newVal, oldVal) {
        // Only trigger search if values actually changed
        if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
          this.handleSearch();
        }
      },
      deep: true,
    },
    selectedTags: {
      handler(newVal, oldVal) {
        // Only trigger search if values actually changed
        if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
          this.handleSearch();
        }
      },
      deep: true,
    },
    tagMatchType: {
      handler(newVal, oldVal) {
        // Only trigger search if value actually changed
        if (newVal !== oldVal) {
          this.handleSearch();
        }
      },
    },
  },
  beforeUnmount() {
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
    }
  },
  beforeRouteUpdate(to, from, next) {
    if (to.path !== from.path) {
      this.tagsLoaded = false;
    }
    next();
  },
};
</script>

<style>
@import "vue-multiselect/dist/vue-multiselect.css";

.search-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-form {
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.search-input {
  position: relative;
  margin-bottom: 24px;
}

.search-input input {
  width: 100%;
  padding: 12px 40px 12px 16px;
  font-size: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
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
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  font-weight: 500;
  color: #666;
}

.filter-group select,
.filter-group input {
  padding: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.filter-group select:focus,
.filter-group input:focus {
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
  outline: none;
}

.active-filters {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.filter-label {
  font-size: 14px;
  font-weight: 500;
  color: #666;
  margin-right: 12px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 500;
}

.filter-tag button {
  background: none;
  border: none;
  margin-left: 8px;
  cursor: pointer;
  color: #1976d2;
  font-size: 16px;
  padding: 0 4px;
}

.clear-all {
  background: none;
  border: 2px solid #e0e0e0;
  padding: 6px 12px;
  border-radius: 100px;
  color: #666;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.clear-all:hover {
  border-color: #dc3545;
  color: #dc3545;
}

.search-results {
  margin-top: 20px;
  padding: 0 20px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.results-header h2 {
  font-size: 20px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.controls {
  display: flex;
  align-items: center;
  gap: 20px;
}

.sort-controls,
.page-size-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-controls label,
.page-size-controls label {
  font-size: 14px;
  color: #666;
}

.sort-controls select,
.page-size-controls select {
  padding: 6px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
  min-width: 120px;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  padding: 20px 0;
  width: 100%;
}

.user-card {
  width: 100%;
  min-height: 200px;
  margin: 0;
}

.loading {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1976d2;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
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
  text-align: center;
  padding: 40px;
  color: #dc3545;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.retry-button {
  background: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background: #c82333;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
}

.no-results h3 {
  margin: 0 0 8px;
  font-size: 18px;
  font-weight: 500;
}

.no-results p {
  margin: 0;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
}

.page-button {
  padding: 8px 16px;
  border: 2px solid #1976d2;
  background: white;
  color: #1976d2;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.page-button:disabled {
  border-color: #e0e0e0;
  color: #999;
  cursor: not-allowed;
}

.page-button:not(:disabled):hover {
  background: #1976d2;
  color: white;
}

.page-info {
  font-size: 14px;
  color: #666;
}

.tag-option {
  padding: 4px 0;
}

.tag-name {
  font-weight: 500;
}

.tag-description {
  display: block;
  color: #666;
  font-size: 12px;
  margin-top: 2px;
}

.multiselect {
  min-height: 42px;
}

.multiselect__tags {
  min-height: 42px;
  padding: 8px 40px 0 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
}

.multiselect__tags:hover {
  border-color: #1976d2;
}

.multiselect__tag {
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 100px;
  padding: 4px 26px 4px 12px;
}

.multiselect__option--highlight {
  background: #e3f2fd;
  color: #1976d2;
}

.multiselect__option--selected.multiselect__option--highlight {
  background: #dc3545;
  color: white;
}

.text-muted {
  color: #666;
  font-size: 12px;
  margin-left: 4px;
}

.tags-control {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tag-match-type {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}

.tag-match-type label {
  font-size: 12px;
  color: #666;
}

.tag-match-type select {
  padding: 4px 8px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
  background-color: #f5f5f5;
}

.tag-match-type select:hover {
  border-color: #1976d2;
}

@media (max-width: 1024px) {
  .results-grid {
    grid-template-columns: 1fr;
    max-width: 600px;
  }
}

@media (max-width: 768px) {
  .search-results {
    padding: 0 10px;
  }
}
</style>
