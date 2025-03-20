<template>
  <div class="notifications-container">
    <h3>Notifications</h3>
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
        :class="['notification-item', { unread: !notification.is_read }]"
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
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.error = "Please log in to view notifications";
          return;
        }

        const response = await api.get("api/notifications", {
          headers: this.getAuthHeader(),
        });

        console.log("Notifications response:", response.data);
        this.notifications = response.data;
      } catch (error) {
        console.error("Error fetching notifications:", error);
        if (error.response?.status === 401) {
          // Try to refresh the token
          try {
            const refreshToken = localStorage.getItem("refresh_token");
            if (!refreshToken) {
              throw new Error("No refresh token");
            }

            const refreshResponse = await api.post("api/token/refresh/", {
              refresh: refreshToken,
            });

            localStorage.setItem("access_token", refreshResponse.data.access);

            // Retry the original request with new token
            const response = await api.get("api/notifications/", {
              headers: {
                Authorization: `Bearer ${refreshResponse.data.access}`,
              },
            });

            this.notifications = response.data;
          } catch (refreshError) {
            console.error("Token refresh failed:", refreshError);
            this.error = "Session expired. Please log in again.";
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
          }
        } else {
          this.error = "Failed to load notifications";
        }
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    console.log("NotificationList component mounted");
    this.fetchNotifications();
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
