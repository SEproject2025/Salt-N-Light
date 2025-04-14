<template>
<<<<<<< HEAD
  <div class="quick-search-results" v-if="results.length > 0">
    <div class="results-header">
      <h3>Quick Results</h3>
      <button class="view-all" @click="$emit('view-all')">View All</button>
    </div>
    <ul class="results-list">
      <li v-for="profile in results" :key="profile.user.id" class="result-item">
        <div class="result-content">
          <div class="user-info">
            <h4>{{ profile.first_name }} {{ profile.last_name }}</h4>
            <p class="location">
              {{ profile.city }}{{ profile.state ? ", " + profile.state : ""
              }}{{ profile.country ? ", " + profile.country : "" }}
            </p>
            <div class="tags" v-if="profile.tags && profile.tags.length > 0">
              <span
                v-for="tag in profile.tags.slice(0, 2)"
                :key="tag.id"
                class="tag"
              >
                {{ tag.tag_name }}
              </span>
              <span v-if="profile.tags.length > 2" class="more-tags">
                +{{ profile.tags.length - 2 }} more
              </span>
            </div>
          </div>
          <button
            class="view-profile"
            @click="$emit('select-profile', profile)"
          >
            View Profile
          </button>
        </div>
      </li>
    </ul>
=======
  <div class="quick-search-results">
    <div class="results-container">
      <div v-if="isLoading" class="loading">
        <div class="loading-spinner"></div>
        <span>Searching...</span>
      </div>
      <div v-else class="results-list">
        <div
          v-for="result in results"
          :key="result.user.id"
          class="result-item"
          @click="$emit('select-result', result)"
        >
          <div class="result-content">
            <div class="name">
              {{ result.first_name }} {{ result.last_name }}
            </div>
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
>>>>>>> 1133bde2919c72394fd207d82de3c4aa82b2a6d4
  </div>
</template>

<script>
export default {
  name: "QuickSearchResults",
  props: {
    results: {
      type: Array,
      required: true,
    },
<<<<<<< HEAD
=======
    isLoading: {
      type: Boolean,
      default: false,
    },
>>>>>>> 1133bde2919c72394fd207d82de3c4aa82b2a6d4
  },
};
</script>

<style scoped>
.quick-search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
<<<<<<< HEAD
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 8px;
  z-index: 1000;
  max-height: 400px;
  overflow-y: auto;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
}

.results-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.view-all {
  background: none;
  border: none;
  color: #1976d2;
  font-size: 14px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.view-all:hover {
  background: #e3f2fd;
}

.results-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.result-item {
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
  cursor: default;
}

.result-item:last-child {
  border-bottom: none;
=======
  margin-top: 4px;
  z-index: 1000;
}

.results-container {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-height: 300px;
  overflow-y: auto;
}

.loading {
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #1976d2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.results-list {
  padding: 4px 0;
}

.result-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.result-item:hover {
  background-color: #f5f5f5;
>>>>>>> 1133bde2919c72394fd207d82de3c4aa82b2a6d4
}

.result-content {
  display: flex;
<<<<<<< HEAD
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.user-info {
  flex: 1;
}

.user-info h4 {
  margin: 0 0 4px;
  font-size: 14px;
=======
  flex-direction: column;
  gap: 4px;
}

.name {
>>>>>>> 1133bde2919c72394fd207d82de3c4aa82b2a6d4
  font-weight: 500;
  color: #333;
}

<<<<<<< HEAD
.location {
  margin: 0 0 8px;
  font-size: 12px;
  color: #666;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 2px 8px;
  border-radius: 100px;
  font-size: 12px;
}

.more-tags {
  color: #666;
  font-size: 12px;
}

.view-profile {
  background: #1976d2;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.view-profile:hover {
  background: #1565c0;
=======
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
>>>>>>> 1133bde2919c72394fd207d82de3c4aa82b2a6d4
}
</style>
