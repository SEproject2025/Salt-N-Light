<template>
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
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.quick-search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
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
