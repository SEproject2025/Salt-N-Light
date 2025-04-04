<template>
  <div class="quick-search" v-click-outside="handleClickOutside">
    <div class="search-input">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search by name, location, or tags..."
        @input="handleSearch"
        @keyup.enter="navigateToSearch"
        @focus="handleFocus"
      />
      <div class="search-icon" @click="navigateToSearch">
        <i class="fas fa-search"></i>
      </div>
    </div>
    <!-- Temporarily commented out filters modal
     <div class="quick-filters" v-if="showFilters">
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
           :options="availableTagsList"
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
               <span class="custom-tag-remove" @click="remove(option)">&times;</span>
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
     -->
    <QuickSearchResults
      v-if="showResults && searchResults.length > 0 && searchQuery.trim()"
      :results="searchResults"
      @view-all="navigateToSearch"
      @select-profile="handleProfileSelect"
    />
  </div>
</template>

<script>
import QuickSearchResults from "./QuickSearchResults.vue";
import { searchService } from "@/services/searchService";

export default {
  name: "QuickSearch",
  components: {
    QuickSearchResults,
  },
  directives: {
    clickOutside: {
      mounted(el, binding) {
        el.clickOutsideEvent = function (event) {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value(event);
          }
        };
        document.addEventListener("click", el.clickOutsideEvent);
      },
      unmounted(el) {
        document.removeEventListener("click", el.clickOutsideEvent);
      },
    },
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
    this.loadAllTags();
    // Add route change listener
    this.$router.beforeEach((to, from, next) => {
      this.closeModal();
      next();
    });
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
    async loadAllTags() {
      try {
        this.availableTags = await searchService.getAllTags();
      } catch (error) {
        console.error("Error loading all tags:", error);
      }
    },
    async performSearch() {
      // Don't perform search if query is empty
      if (
        !this.searchQuery.trim() &&
        !this.userType &&
        !this.location &&
        this.selectedTags.length === 0
      ) {
        this.showResults = false;
        this.searchResults = [];
        return;
      }
      const params = {
        q: this.searchQuery,
        user_type: this.userType,
        location: this.location,
        tags: this.selectedTags.map((tag) => tag.tag_name),
        page_size: 5, // Limit results for quick search
      };
      try {
        const response = await searchService.searchProfiles(params);
        this.searchResults = response.results;
        this.showResults = true;
      } catch (error) {
        console.error("Search error:", error);
        this.searchResults = [];
        this.showResults = false;
      }
    },
    handleClickOutside() {
      this.closeModal();
    },
    closeModal() {
      this.showFilters = false;
      this.showResults = false;
    },
    handleFocus() {
      // If there's existing text, trigger a search
      if (this.searchQuery) {
        this.handleSearch();
      }
      this.showFilters = true;
    },
    handleProfileSelect(profile) {
      this.$router.push(`/profile/${profile.user.id}`);
      this.closeModal();
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
      this.closeModal();
    },
  },
  computed: {
    // Convert Set of tag strings back to objects for the multiselect
    availableTagsList() {
      return Array.from(this.availableTags).map((tagStr) => JSON.parse(tagStr));
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
</style>
