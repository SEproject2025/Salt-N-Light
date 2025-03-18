<template>
  <div class="quick-search-results">
    <div class="results-header">
      <h3>Quick Results</h3>
      <button class="view-all" @click="$emit('view-all')">View All</button>
    </div>
    <div v-if="results.length === 0" class="no-results">
      <p>No results found</p>
    </div>
    <ul v-else class="results-list">
      <li
        v-for="profile in results"
        :key="profile.user.id"
        class="result-item"
        @click="handleProfileClick(profile)"
      >
        <button class="result-button">
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
                  @click.stop
                >
                  {{ tag.tag_name }}
                </span>
                <span
                  v-if="profile.tags.length > 2"
                  class="more-tags"
                  @mouseenter.stop="showAllTags(profile)"
                  @mouseleave.stop="hideAllTags(profile)"
                  @click.stop
                >
                  +{{ profile.tags.length - 2 }} more
                </span>
              </div>
              <!-- Hidden tags that appear on hover -->
              <div
                v-if="profile.tags && profile.tags.length > 2"
                class="hidden-tags"
                :class="{ show: profile.showAllTags }"
                @click.stop
              >
                <span
                  v-for="tag in profile.tags.slice(2)"
                  :key="tag.id"
                  class="tag"
                >
                  {{ tag.tag_name }}
                </span>
              </div>
            </div>
            <span class="view-profile-text">View Profile</span>
          </div>
        </button>
      </li>
    </ul>
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
  },
  methods: {
    showAllTags(profile) {
      profile.showAllTags = true;
    },
    hideAllTags(profile) {
      profile.showAllTags = false;
    },
    handleProfileClick(profile) {
      this.$emit("select-profile", profile);
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
  padding: 0;
  border-bottom: 1px solid #e0e0e0;
}

.result-item:last-child {
  border-bottom: none;
}

.result-button {
  width: 100%;
  padding: 12px 16px;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.2s ease;
}

.result-button:hover {
  background-color: #f5f5f5;
}

.result-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  width: 100%;
}

.user-info {
  flex: 1;
}

.user-info h4 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.location {
  margin: 0 0 8px;
  font-size: 12px;
  color: #666;
}

.tags {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 2px 8px;
  border-radius: 100px;
  font-size: 12px;
  white-space: nowrap;
}

.more-tags {
  color: #666;
  font-size: 12px;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 100px;
  background: #f5f5f5;
  transition: background-color 0.2s;
  position: relative;
}

.more-tags:hover {
  background: #e0e0e0;
}

.hidden-tags {
  display: none;
  position: fixed;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 9999;
  max-width: 200px;
  flex-wrap: wrap;
  gap: 4px;
  pointer-events: none;
}

.hidden-tags.show {
  display: flex;
  pointer-events: auto;
}

.view-profile-text {
  color: #1976d2;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.no-results {
  padding: 16px;
  text-align: center;
  color: #666;
  font-size: 14px;
}
</style>
