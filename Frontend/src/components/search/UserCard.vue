<template>
  <div class="user-card-row">
    <div class="user-card-col">
      <div class="card">
        <div class="card-header">
          <div class="profile-section">
            <div class="header-content">
              <h2 class="church-name">{{ first_name }} {{ last_name }}</h2>
              <p class="location">{{ formattedLocation }}</p>
              <p class="profile-type">{{ user_type }}</p>
            </div>
          </div>
        </div>

        <div class="card-content">
          <p class="description">{{ description }}</p>

          <div class="tags-container">
            <template v-if="tags && tags.length">
              <span
                v-for="(tag, index) in displayedTags"
                :key="index"
                class="tag"
                :title="tag.tag_description"
              >
                {{ tag.tag_name }}
              </span>
              <div
                v-if="hasMoreTags"
                class="more-tags"
                @click="showAllTags = !showAllTags"
              >
                {{ showAllTags ? "Show less" : `${hiddenTagsCount} more` }}
              </div>
            </template>
            <span v-else class="no-tags">No tags</span>
          </div>

          <button class="view-profile-btn" @click="viewProfile">
            View Profile
          </button>
        </div>
      </div>
    </div>
  </div>

  <div id="ProfileWindow">
    <transition name="fade" appear>
      <div
        class="modal-overlay"
        v-if="showModal"
        @click="showModal = false"
      ></div>
    </transition>
    <transition name="slide" appear>
      <div class="modal" v-if="showModal">
        <div class="avatar">
          <img :src="userImage" alt="profile_image" class="profile_image" />
        </div>
        <h1>
          <span>{{ first_name }} {{ last_name }}</span>
        </h1>
        <p>
          <span>{{ city }}, {{ state }}, {{ country }}</span>
        </p>
        <p>
          {{ description }}
        </p>
        <button class="button" @click="showModal = false">Close Profile</button>
      </div>
    </transition>
  </div>
</template>

<script>
import userImage from "@/assets/pictures/missionaryprof.jpeg";

export default {
  name: "UserCard",
  props: {
    first_name: {
      type: String,
      required: true,
    },
    last_name: {
      type: String,
      required: true,
    },
    city: {
      type: String,
      required: true,
    },
    state: {
      type: String,
      required: true,
    },
    country: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    id: {
      type: Number,
      required: true,
    },
    tags: {
      type: Array,
      default: () => [],
    },
    user_type: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      userImage: userImage,
      showModal: false,
      isBookmarked: false,
      showAllTags: false,
      maxVisibleTags: 3,
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
    formattedLocation() {
      const parts = [];
      if (this.city) parts.push(this.city);
      if (this.state) parts.push(this.state);
      if (this.country) parts.push(this.country);
      return parts.join(", ");
    },
  },
  methods: {
    viewProfile() {
      this.$router.push(`/profile/${this.id}`);
    },
    toggleBookmark() {
      this.isBookmarked = !this.isBookmarked;
      // TODO: Implement bookmark functionality with backend
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "montserrat", sans-serif;
}

.user-card-row {
  display: flex;
  justify-content: flex-start;
  width: 100%;
}

.user-card-col {
  width: 100%;
  max-width: 450px; /* Limit card width to roughly half the header */
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
  overflow: hidden;
  padding: 20px;
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

.profile-section {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  flex: 1;
  min-width: 0;
}

.avatar {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid #eee;
}

.profile_image {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  width: fit-content;
}

.bookmark-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  color: #666;
  padding: 4px;
  transition: color 0.2s;
}

.bookmark-btn:hover {
  color: #333;
}

.card-content {
  padding: 0;
}

.description {
  display: -webkit-box;
  -webkit-line-clamp: 3; /* Limit to 3 lines */
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5;
  max-height: 4.5em; /* 3 lines × 1.5 line height */
  margin-bottom: 1rem;
}

/* Add hover state to show full description */
.description:hover {
  -webkit-line-clamp: unset;
  line-clamp: 3;
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
}

.view-profile-btn:hover {
  background: #1565c0;
}

#UserProfile {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 60vw;
  min-height: 60vh;
  overflow-x: hidden;
}

.button {
  appearance: none;
  outline: none;
  border: none;
  background: none;
  cursor: pointer;
  display: inline-block;
  padding: 10px 15px;
  background-image: linear-gradient(to right, #0a0a0a, #0e0e0e);
  border-radius: 10px;
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  box-shadow: 3px 3px rgba(0, 0, 0, 0.4);
  transition: 0.4s ease-out;
}

.button:hover {
  box-shadow: 6px 6px rgba(0, 0, 0, 0.6);
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 98;
  background-color: rgba(0, 0, 0, 0.3);
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 99;
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 16px;
  padding: 25px;
}

.modal h1 {
  color: #222;
  font-size: 25px;
  font-weight: 900;
  margin-bottom: 15px;
}

.modal p {
  color: #666;
  font-size: 18px;
  font-weight: 400;
  margin-bottom: 15px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s;
}

.slide-enter,
.slide-leave-to {
  transform: translateY(-50%) translateX(100vw);
}
</style>
