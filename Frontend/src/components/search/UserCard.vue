<template>
  <div class="user-card-row" role="article">
    <div class="user-card-col">
      <div class="card" :class="{ 'is-loading': isLoading }">
        <div class="card-header">
          <div class="header-content">
            <h2 class="church-name">{{ first_name }} {{ last_name }}</h2>
            <p class="location">{{ city }}, {{ country }}</p>
            <p class="profile-type">{{ user_type }}</p>
          </div>
          <button
            class="bookmark-btn"
            @click="toggleBookmark"
            :aria-label="isBookmarked ? 'Remove bookmark' : 'Add bookmark'"
            :title="isBookmarked ? 'Remove bookmark' : 'Add bookmark'"
          >
            <font-awesome-icon
              :icon="['far', 'bookmark']"
              v-if="!isBookmarked"
            />
            <font-awesome-icon :icon="['fas', 'bookmark']" v-else />
          </button>
        </div>

        <div class="card-content">
          <p class="description" :title="description">{{ description }}</p>

          <div class="tags-container" role="list" aria-label="Profile tags">
            <template v-if="tags && tags.length">
              <span
                v-for="(tag, index) in displayedTags"
                :key="index"
                class="tag"
                :title="tag.tag_description || tag.description"
                role="listitem"
              >
                {{ tag.tag_name || tag.name || "Untagged" }}
              </span>
              <button
                v-if="hasMoreTags"
                class="more-tags"
                @click="showAllTags = !showAllTags"
                :aria-expanded="showAllTags"
                :aria-label="
                  showAllTags
                    ? 'Show fewer tags'
                    : `Show ${hiddenTagsCount} more tags`
                "
              >
                {{ showAllTags ? "Show less" : `${hiddenTagsCount} more` }}
              </button>
            </template>
            <span v-else class="no-tags" role="listitem">No tags</span>
          </div>

          <button
            class="view-profile-btn"
            @click="viewProfile"
            :disabled="isLoading"
            :aria-busy="isLoading"
          >
            <span
              v-if="isLoading"
              class="loading-spinner"
              aria-hidden="true"
            ></span>
            <span v-else>View Profile</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserCard",
  props: {
    first_name: {
      type: String,
      required: true,
      validator: (value) => value.trim().length > 0,
    },
    last_name: {
      type: String,
      required: true,
      validator: (value) => value.trim().length > 0,
    },
    city: {
      type: String,
      default: "",
    },
    state: {
      type: String,
      default: "",
    },
    country: {
      type: String,
      default: "",
    },
    description: {
      type: String,
      default: "",
    },
    id: {
      type: Number,
      required: true,
      validator: (value) => value > 0,
    },
    tags: {
      type: Array,
      default: () => [],
      validator: (value) => Array.isArray(value),
    },
    user_type: {
      type: String,
      default: "",
      validator: (value) =>
        ["Church", "Missionary", "Supporter", ""].includes(value),
    },
    user: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      isBookmarked: false,
      showAllTags: false,
      maxVisibleTags: 3,
      isLoading: false,
    };
  },
  computed: {
    displayedTags() {
      if (!this.tags) return [];
      return this.showAllTags
        ? this.tags
        : this.tags.slice(0, this.maxVisibleTags);
    },
    hasMoreTags() {
      return this.tags && this.tags.length > this.maxVisibleTags;
    },
    hiddenTagsCount() {
      return this.tags ? this.tags.length - this.maxVisibleTags : 0;
    },
  },
  methods: {
    async viewProfile() {
      if (this.isLoading) return;

      this.isLoading = true;
      try {
        const userId = this.id ?? this.user?.id;
        if (!userId) {
          console.warn("No valid ID for profile navigation.");
          return;
        }
        await this.$router.push(`/profile/${userId}`);
      } catch (error) {
        console.error("Navigation failed:", error);
        // You could emit an event here to show a toast notification
        this.$emit("error", "Failed to navigate to profile");
      } finally {
        this.isLoading = false;
      }
    },
    async toggleBookmark() {
      if (this.isLoading) return;

      this.isLoading = true;
      try {
        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 500));
        this.isBookmarked = !this.isBookmarked;
        this.$emit("bookmark-toggled", {
          id: this.id,
          isBookmarked: this.isBookmarked,
        });
      } catch (error) {
        console.error("Bookmark toggle failed:", error);
        this.$emit("error", "Failed to update bookmark");
      } finally {
        this.isLoading = false;
      }
    },
  },
  emits: ["error", "bookmark-toggled"],
};
</script>

<style scoped>
.user-card-row {
  display: flex;
  justify-content: flex-start;
  width: 100%;
}

.user-card-col {
  width: 100%;
  max-width: 450px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
  overflow: hidden;
  padding: 20px;
  position: relative;
}

.card.is-loading {
  opacity: 0.7;
  pointer-events: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  width: 100%;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  flex: 1;
}

.church-name {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.location {
  font-size: 16px;
  color: #666;
  margin: 0;
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.profile-type {
  font-size: 14px;
  color: #1976d2;
  margin: 0;
  padding: 2px 8px;
  background: #e3f2fd;
  border-radius: 4px;
  display: inline-block;
  text-transform: capitalize;
}

.bookmark-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  color: #666;
  padding: 4px;
  transition: color 0.2s;
  min-width: 32px;
  min-height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bookmark-btn:hover {
  color: #333;
}

.bookmark-btn:focus {
  outline: 2px solid #1976d2;
  outline-offset: 2px;
}

.card-content {
  padding: 0;
}

.description {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5;
  max-height: 4.5em;
  margin-bottom: 1rem;
  color: #333;
}

.description:hover {
  -webkit-line-clamp: unset;
  line-clamp: unset;
  max-height: none;
  cursor: pointer;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: auto;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  white-space: nowrap;
}

.more-tags {
  color: #666;
  font-size: 12px;
  cursor: pointer;
  white-space: nowrap;
  background: none;
  border: none;
  padding: 4px 8px;
}

.more-tags:hover {
  color: #333;
}

.more-tags:focus {
  outline: 2px solid #1976d2;
  outline-offset: 2px;
}

.view-profile-btn {
  background: #1976d2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
  margin-top: 20px;
  position: relative;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.view-profile-btn:hover:not(:disabled) {
  background: #1565c0;
}

.view-profile-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.view-profile-btn:focus {
  outline: 2px solid #1976d2;
  outline-offset: 2px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
  .user-card-col {
    max-width: 100%;
  }

  .card {
    padding: 16px;
  }

  .church-name {
    font-size: 20px;
  }

  .location {
    font-size: 14px;
  }

  .profile-type {
    font-size: 12px;
  }

  .description {
    font-size: 14px;
  }

  .tag {
    font-size: 11px;
    padding: 3px 10px;
  }

  .view-profile-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}

/* High Contrast Mode */
@media (forced-colors: active) {
  .card {
    border: 1px solid CanvasText;
  }

  .profile-type {
    border: 1px solid CanvasText;
  }

  .tag {
    border: 1px solid CanvasText;
  }

  .view-profile-btn {
    border: 1px solid CanvasText;
  }
}
</style>
