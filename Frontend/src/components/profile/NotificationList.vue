<template>
  <div class="notifications-container">
    <h3 class="notifications-title">Notifications</h3>

    <div v-if="loading" class="loading">Loading notifications...</div>
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else class="notification-list">
      <div v-if="notifications.length === 0" class="no-notifications">
        No notifications
      </div>
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="notification-item"
      >
        <div class="notification-content">
          <div class="notification-header">
            <span
              :class="['notification-type', notification.notification_type]"
            >
              {{ formatNotificationType(notification.notification_type) }}
            </span>
            <span class="notification-date">{{
              formatDate(notification.created_at)
            }}</span>
          </div>
          <div class="notification-message">{{ notification.message }}</div>
          <div
            v-if="notification.notification_type === 'friend_request'"
            class="friend-request-actions"
          >
            <template v-if="!respondedRequests.has(notification.id)">
              <button
                class="accept-btn"
                @click="respondToFriendRequest(notification, 'accept')"
              >
                Accept
              </button>
              <button
                class="reject-btn"
                @click="respondToFriendRequest(notification, 'reject')"
              >
                Reject
              </button>
            </template>
            <div
              v-else
              class="expanded-button"
              :class="getResponseClass(notification)"
            >
              {{ getResponseText(notification) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios.js";

export default {
  name: "NotificationList",
  data() {
    return {
      notifications: [],
      loading: false,
      error: null,
      respondedRequests: new Map(),
    };
  },
  methods: {
    formatNotificationType(type) {
      return type
        .split("_")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
    getAuthHeader() {
      const token = localStorage.getItem("access_token");
      return token ? { Authorization: `Bearer ${token}` } : {};
    },
    async fetchNotifications() {
      this.loading = true;
      this.error = null;

      try {
        const response = await api.get("api/notifications", {
          headers: this.getAuthHeader(),
        });
        // Load stored responses first
        const responses = JSON.parse(
          localStorage.getItem("notificationResponses") || "{}"
        );
        // Filter out notifications that have been responded to
        this.notifications = response.data.filter((notification) => {
          if (notification.notification_type === "friend_request") {
            const hasResponded = responses[notification.id];
            if (hasResponded) {
              // Don't show notifications that have been responded to
              this.respondedRequests.set(notification.id, hasResponded);
              return false;
            }
          }
          return true;
        });
      } catch (error) {
        this.error = "Failed to load notifications";
      } finally {
        this.loading = false;
      }
    },
  },
  async respondToFriendRequest(notification, action) {
    try {
      await api.post(
        `api/friendships/${notification.related_object_id}/respond/`,
        { action: action },
        { headers: this.getAuthHeader() }
      );
      // Store the response in localStorage
      const responses = JSON.parse(
        localStorage.getItem("notificationResponses") || "{}"
      );
      responses[notification.id] = action;
      localStorage.setItem("notificationResponses", JSON.stringify(responses));
      this.respondedRequests.set(notification.id, action);
    } catch (error) {
      this.error = "Failed to respond to friend request.";
    }
  },
  getResponseClass(notification) {
    const action = this.respondedRequests.get(notification.id);
    return action === "reject" ? "reject" : "accept";
  },
  getResponseText(notification) {
    const action = this.respondedRequests.get(notification.id);
    return action === "reject" ? "Rejected" : "Accepted";
  },
  mounted() {
    this.fetchNotifications();
    // Load stored responses
    const responses = JSON.parse(
      localStorage.getItem("notificationResponses") || "{}"
    );
    Object.entries(responses).forEach(([id, action]) => {
      this.respondedRequests.set(parseInt(id), action);
    });
  },
};
</script>

<style scoped>
.notifications-container {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.notification-list {
  margin-top: 15px;
}

.loading,
.error-message {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error-message {
  color: #dc3545;
}

.notifications-title {
  font-size: 1.55rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.notification-item {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
  transition: background-color 0.2s;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.notification-type {
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.notification-type.friend_request {
  background-color: #e3f2fd;
  color: #1976d2;
}

.notification-type.general {
  background-color: #f5f5f5;
  color: #616161;
}

.notification-date {
  color: #666;
  font-size: 0.9em;
}

.notification-message {
  color: #333;
  margin-top: 5px;
}

.no-notifications {
  text-align: center;
  color: #666;
  padding: 20px;
  font-style: italic;
}
</style>