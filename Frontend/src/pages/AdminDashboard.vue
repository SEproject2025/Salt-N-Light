<script>
import api from "@/api/axios.js";

export default {
  name: "AdminDashboard",
  data() {
    return {
      isLoading: true,
      isSuperuser: false,
      activeTab: "profiles",
      profiles: [],
      comments: [],
      profileSearchQuery: "",
      commentSearchQuery: "",
      filteredProfiles: [],
      filteredComments: [],
      showDeleteModal: false,
      deleteType: null,
      itemToDelete: null,
      deleteModalMessage: "",

      // Details modals
      showProfileDetailsModal: false,
      showCommentDetailsModal: false,
      selectedProfile: null,
      selectedComment: null,

      // Loading states for pagination
      profilesLoading: false,
      commentsLoading: false,

      // Pagination data for profiles
      profilesCurrentPage: 1,
      profilesTotalPages: 1,
      profilesTotalCount: 0,

      // Pagination data for comments
      commentsCurrentPage: 1,
      commentsTotalPages: 1,
      commentsTotalCount: 0,

      // Items per page
      itemsPerPage: 20,
    };
  },
  mounted() {
    this.checkSuperuserStatus();
  },
  methods: {
    async checkSuperuserStatus() {
      this.isLoading = true;
      const token = localStorage.getItem("access_token");

      if (!token) {
        this.isLoading = false;
        this.isSuperuser = false;
        return;
      }

      try {
        // Check if user is superuser
        const response = await api.get("api/admin/check-superuser/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        this.isSuperuser = response.data.is_superuser;

        if (this.isSuperuser) {
          await this.loadData();
        }
      } catch (error) {
        this.isSuperuser = false;
      } finally {
        this.isLoading = false;
      }
    },

    async loadData() {
      try {
        // Only load data for the active tab
        if (this.activeTab === "profiles") {
          await this.loadProfiles();
        } else if (this.activeTab === "comments") {
          await this.loadComments();
        }
      } catch (error) {}
    },

    async loadProfiles() {
      try {
        this.profilesLoading = true;
        // Clear previous results while loading
        this.profiles = [];
        this.filteredProfiles = [];

        const profilesResponse = await api.get("api/admin/profiles/", {
          params: {
            page: this.profilesCurrentPage,
            page_size: this.itemsPerPage,
          },
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        // Extract pagination information
        this.profiles = profilesResponse.data.results;
        this.profilesTotalCount = profilesResponse.data.count;
        this.profilesTotalPages = Math.ceil(
          this.profilesTotalCount / this.itemsPerPage
        );

        // Apply any existing search filter
        this.filterProfiles();
      } catch (error) {
      } finally {
        this.profilesLoading = false;
      }
    },

    async loadComments() {
      try {
        this.commentsLoading = true;
        // Clear previous results while loading
        this.comments = [];
        this.filteredComments = [];

        const commentsResponse = await api.get("api/admin/comments/", {
          params: {
            page: this.commentsCurrentPage,
            page_size: this.itemsPerPage,
          },
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });

        // Extract pagination information
        this.comments = commentsResponse.data.results;
        this.commentsTotalCount = commentsResponse.data.count;
        this.commentsTotalPages = Math.ceil(
          this.commentsTotalCount / this.itemsPerPage
        );

        // Apply any existing search filter
        this.filterComments();
      } catch (error) {
      } finally {
        this.commentsLoading = false;
      }
    },

    async changePage(type, newPage) {
      if (type === "profiles") {
        this.profilesCurrentPage = newPage;
        await this.loadProfiles();
      } else if (type === "comments") {
        this.commentsCurrentPage = newPage;
        await this.loadComments();
      }
    },

    filterProfiles() {
      const query = this.profileSearchQuery.toLowerCase();
      if (!query) {
        this.filteredProfiles = [...this.profiles];
        return;
      }

      this.filteredProfiles = this.profiles.filter((profile) => {
        const username = profile.user.username.toLowerCase();
        const firstName = (profile.first_name || "").toLowerCase();
        const lastName = (profile.last_name || "").toLowerCase();
        const userType = (profile.user_type || "").toLowerCase();
        const email = (profile.user.email || "").toLowerCase();
        const phone = (profile.phone_number || "").toLowerCase();
        const address = (profile.street_address || "").toLowerCase();
        const city = (profile.city || "").toLowerCase();
        const state = (profile.state || "").toLowerCase();
        const country = (profile.country || "").toLowerCase();
        const denomination = (profile.denomination || "").toLowerCase();
        const description = (profile.description || "").toLowerCase();

        return (
          username.includes(query) ||
          firstName.includes(query) ||
          lastName.includes(query) ||
          userType.includes(query) ||
          email.includes(query) ||
          phone.includes(query) ||
          address.includes(query) ||
          city.includes(query) ||
          state.includes(query) ||
          country.includes(query) ||
          denomination.includes(query) ||
          description.includes(query)
        );
      });
    },

    filterComments() {
      const query = this.commentSearchQuery.toLowerCase();
      if (!query) {
        this.filteredComments = [...this.comments];
        return;
      }

      this.filteredComments = this.comments.filter((comment) => {
        const commentText = (comment.comment || "").toLowerCase();
        const commenterUsername = comment.commenter
          ? comment.commenter.username.toLowerCase()
          : "";
        const profileUsername =
          comment.profile_detail && comment.profile_detail.user
            ? comment.profile_detail.user.username.toLowerCase()
            : "";

        return (
          commentText.includes(query) ||
          commenterUsername.includes(query) ||
          profileUsername.includes(query)
        );
      });
    },

    viewProfileDetails(profile) {
      this.selectedProfile = profile;
      this.showProfileDetailsModal = true;
    },

    viewCommentDetails(comment) {
      this.selectedComment = comment;
      this.showCommentDetailsModal = true;
    },

    confirmDelete(type, item) {
      this.deleteType = type;
      this.itemToDelete = item;

      if (type === "profile") {
        const username = item.user ? item.user.username : "Unknown user";
        this.deleteModalMessage = `Are you sure you want to delete the profile for ${username}? This will also delete all related data.`;
      } else if (type === "comment") {
        const username = item.commenter
          ? item.commenter.username
          : "Unknown user";
        const profileUsername =
          item.profile_detail && item.profile_detail.user
            ? item.profile_detail.user.username
            : "Unknown user";
        this.deleteModalMessage = `Are you sure you want to delete the comment by ${username} on ${profileUsername}'s profile?`;
      }

      this.showDeleteModal = true;
    },

    async performDelete() {
      try {
        if (this.deleteType === "profile") {
          await api.delete(`api/admin/profiles/${this.itemToDelete.user.id}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          });

          // Reload current page after deletion
          await this.loadProfiles();
        } else if (this.deleteType === "comment") {
          await api.delete(`api/admin/comments/${this.itemToDelete.id}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          });

          // Reload current page after deletion
          await this.loadComments();
        }

        this.showDeleteModal = false;
        this.deleteType = null;
        this.itemToDelete = null;
      } catch (error) {
        alert("An error occurred while deleting. Please try again.");
      }
    },

    formatDate(dateString) {
      if (!dateString) return "-";
      const date = new Date(dateString);
      return date.toLocaleDateString() + " " + date.toLocaleTimeString();
    },

    // Method to handle tab changes
    async changeTab(tabName) {
      if (tabName === this.activeTab) {
        return; // No change needed if it's the same tab
      }

      this.activeTab = tabName;

      // Always load data when switching tabs to ensure fresh data
      if (tabName === "profiles") {
        await this.loadProfiles();
      } else if (tabName === "comments") {
        await this.loadComments();
      }
    },
  },
};
</script>

<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>

    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Loading admin dashboard...</p>
    </div>

    <div v-else-if="!isSuperuser" class="unauthorized">
      <h2>Unauthorized</h2>
      <p>You must be a superuser to access this page.</p>
      <button @click="$router.push('/')" class="primary-btn">
        Return to Home
      </button>
    </div>

    <div v-else class="dashboard-content">
      <div class="tabs">
        <button
          :class="{ active: activeTab === 'profiles' }"
          @click="changeTab('profiles')"
        >
          Profiles
        </button>
        <button
          :class="{ active: activeTab === 'comments' }"
          @click="changeTab('comments')"
        >
          Comments
        </button>
      </div>

      <div class="tab-content">
        <!-- Profiles Tab -->
        <div v-if="activeTab === 'profiles'" class="profiles-tab">
          <div class="search-box">
            <input
              type="text"
              v-model="profileSearchQuery"
              placeholder="Search profiles..."
              @input="filterProfiles"
            />
          </div>

          <div v-if="profilesLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
            <p>Loading profiles...</p>
          </div>

          <div v-else-if="filteredProfiles.length === 0" class="no-results">
            <p>No profiles found</p>
          </div>

          <table v-else>
            <thead>
              <tr>
                <th width="60">Details</th>
                <th>username</th>
                <th>user_type</th>
                <th>first_name / last_name</th>
                <th>email / phone_number</th>
                <th>location</th>
                <th>denomination</th>
                <th>years_of_experience</th>
                <th>description</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="profile in filteredProfiles" :key="profile.user.id">
                <td>
                  <button class="view-btn" @click="viewProfileDetails(profile)">
                    View
                  </button>
                </td>
                <td>{{ profile.user.username }}</td>
                <td>{{ profile.user_type || "-" }}</td>
                <td>
                  {{ profile.first_name || "" }} {{ profile.last_name || "" }}
                </td>
                <td>
                  <div>{{ profile.user.email || "-" }}</div>
                  <div>{{ profile.phone_number || "-" }}</div>
                </td>
                <td>
                  <div>{{ profile.street_address || "-" }}</div>
                  <div>
                    {{ profile.city || ""
                    }}{{ profile.city && profile.state ? ", " : ""
                    }}{{ profile.state || "" }}
                  </div>
                  <div>{{ profile.country || "-" }}</div>
                </td>
                <td>{{ profile.denomination || "-" }}</td>
                <td>
                  {{
                    profile.years_of_experience
                      ? profile.years_of_experience + " years"
                      : "-"
                  }}
                </td>
                <td class="description-cell">
                  <div class="truncate-text">
                    {{ profile.description || "-" }}
                  </div>
                </td>
                <td>
                  <button
                    class="delete-btn"
                    @click="confirmDelete('profile', profile)"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination Controls for Profiles -->
          <div
            v-if="!profilesLoading && filteredProfiles.length > 0"
            class="pagination-controls"
          >
            <button
              :disabled="profilesCurrentPage === 1 || profilesLoading"
              @click="changePage('profiles', profilesCurrentPage - 1)"
              class="pagination-btn"
            >
              Previous
            </button>
            <span class="page-info"
              >Page {{ profilesCurrentPage }} of {{ profilesTotalPages }}</span
            >
            <button
              :disabled="
                profilesCurrentPage === profilesTotalPages ||
                profilesTotalPages === 0 ||
                profilesLoading
              "
              @click="changePage('profiles', profilesCurrentPage + 1)"
              class="pagination-btn"
            >
              Next
            </button>
          </div>
        </div>

        <!-- Comments Tab -->
        <div v-if="activeTab === 'comments'" class="comments-tab">
          <div class="search-box">
            <input
              type="text"
              v-model="commentSearchQuery"
              placeholder="Search comments..."
              @input="filterComments"
            />
          </div>

          <div v-if="commentsLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
            <p>Loading comments...</p>
          </div>

          <div v-else-if="filteredComments.length === 0" class="no-results">
            <p>No comments found</p>
          </div>

          <table v-else>
            <thead>
              <tr>
                <th width="60">Details</th>
                <th>comment</th>
                <th>commenter</th>
                <th>profile</th>
                <th>created_at</th>
                <th>updated_at</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="comment in filteredComments" :key="comment.id">
                <td>
                  <button class="view-btn" @click="viewCommentDetails(comment)">
                    View
                  </button>
                </td>
                <td class="description-cell">
                  <div class="truncate-text">{{ comment.comment }}</div>
                </td>
                <td>
                  {{
                    comment.commenter ? comment.commenter.username : "Unknown"
                  }}
                </td>
                <td>
                  {{
                    comment.profile_detail && comment.profile_detail.user
                      ? comment.profile_detail.user.username
                      : "Unknown"
                  }}
                </td>
                <td>{{ formatDate(comment.created_at) }}</td>
                <td>{{ formatDate(comment.updated_at) }}</td>
                <td>
                  <button
                    class="delete-btn"
                    @click="confirmDelete('comment', comment)"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination Controls for Comments -->
          <div
            v-if="!commentsLoading && filteredComments.length > 0"
            class="pagination-controls"
          >
            <button
              :disabled="commentsCurrentPage === 1 || commentsLoading"
              @click="changePage('comments', commentsCurrentPage - 1)"
              class="pagination-btn"
            >
              Previous
            </button>
            <span class="page-info"
              >Page {{ commentsCurrentPage }} of {{ commentsTotalPages }}</span
            >
            <button
              :disabled="
                commentsCurrentPage === commentsTotalPages ||
                commentsTotalPages === 0 ||
                commentsLoading
              "
              @click="changePage('comments', commentsCurrentPage + 1)"
              class="pagination-btn"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="delete-modal">
      <div class="modal-content">
        <h3>Confirm Deletion</h3>
        <p>{{ deleteModalMessage }}</p>
        <div class="modal-actions">
          <button @click="performDelete" class="confirm-btn">Delete</button>
          <button @click="showDeleteModal = false" class="cancel-btn">
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Profile Details Modal -->
    <div v-if="showProfileDetailsModal" class="details-modal">
      <div class="details-modal-content">
        <div class="details-modal-header">
          <h3>Profile Details</h3>
          <button class="close-btn" @click="showProfileDetailsModal = false">
            &times;
          </button>
        </div>
        <div class="details-modal-body" v-if="selectedProfile">
          <div class="detail-row">
            <div class="detail-label">User ID:</div>
            <div class="detail-value">{{ selectedProfile.user.id }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Username:</div>
            <div class="detail-value">{{ selectedProfile.user.username }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Email:</div>
            <div class="detail-value">
              {{ selectedProfile.user.email || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">User Type:</div>
            <div class="detail-value">
              {{ selectedProfile.user_type || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">First Name:</div>
            <div class="detail-value">
              {{ selectedProfile.first_name || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Last Name:</div>
            <div class="detail-value">
              {{ selectedProfile.last_name || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Denomination:</div>
            <div class="detail-value">
              {{ selectedProfile.denomination || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Street Address:</div>
            <div class="detail-value">
              {{ selectedProfile.street_address || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">City:</div>
            <div class="detail-value">{{ selectedProfile.city || "N/A" }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">State:</div>
            <div class="detail-value">{{ selectedProfile.state || "N/A" }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Country:</div>
            <div class="detail-value">
              {{ selectedProfile.country || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Phone Number:</div>
            <div class="detail-value">
              {{ selectedProfile.phone_number || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Years of Experience:</div>
            <div class="detail-value">
              {{ selectedProfile.years_of_experience || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Profile Picture:</div>
            <div class="detail-value">
              {{ selectedProfile.profile_picture || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Description:</div>
            <div class="detail-value detail-multiline">
              {{ selectedProfile.description || "N/A" }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Tags:</div>
            <div class="detail-value">
              <div
                v-if="selectedProfile.tags && selectedProfile.tags.length > 0"
              >
                <span
                  v-for="tag in selectedProfile.tags"
                  :key="tag.id"
                  class="tag"
                >
                  {{ tag.tag_name || tag.name }}
                </span>
              </div>
              <div v-else>No tags</div>
            </div>
          </div>
        </div>
        <div class="details-modal-footer">
          <button @click="showProfileDetailsModal = false" class="cancel-btn">
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Comment Details Modal -->
    <div v-if="showCommentDetailsModal" class="details-modal">
      <div class="details-modal-content">
        <div class="details-modal-header">
          <h3>Comment Details</h3>
          <button class="close-btn" @click="showCommentDetailsModal = false">
            &times;
          </button>
        </div>
        <div class="details-modal-body" v-if="selectedComment">
          <div class="detail-row">
            <div class="detail-label">Comment ID:</div>
            <div class="detail-value">{{ selectedComment.id }}</div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Comment Text:</div>
            <div class="detail-value detail-multiline">
              {{ selectedComment.comment }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Commenter:</div>
            <div class="detail-value">
              {{
                selectedComment.commenter
                  ? selectedComment.commenter.username
                  : "Unknown"
              }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Profile:</div>
            <div class="detail-value">
              {{
                selectedComment.profile_detail &&
                selectedComment.profile_detail.user
                  ? selectedComment.profile_detail.user.username
                  : "Unknown"
              }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Created At:</div>
            <div class="detail-value">
              {{ formatDate(selectedComment.created_at) }}
            </div>
          </div>
          <div class="detail-row">
            <div class="detail-label">Updated At:</div>
            <div class="detail-value">
              {{ formatDate(selectedComment.updated_at) }}
            </div>
          </div>
        </div>
        <div class="details-modal-footer">
          <button @click="showCommentDetailsModal = false" class="cancel-btn">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading,
.unauthorized {
  text-align: center;
  margin: 50px 0;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.tabs button {
  padding: 10px 20px;
  margin-right: 5px;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-bottom: none;
  cursor: pointer;
}

.tabs button.active {
  background: #fff;
  border-bottom: 2px solid #fff;
  margin-bottom: -1px;
  font-weight: bold;
}

.search-box {
  margin-bottom: 20px;
}

.search-box input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

table th,
table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  overflow: hidden;
  vertical-align: top;
}

.description-cell {
  max-width: 200px;
}

.truncate-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.view-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

.view-btn:hover {
  background-color: #2980b9;
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn:hover {
  background-color: #c0392b;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.pagination-btn {
  padding: 8px 16px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.page-info {
  margin: 0 10px;
  font-size: 14px;
}

.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 4px;
  border: 1px solid #ddd;
  min-height: 200px;
  width: 100%;
  box-sizing: border-box;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

.loading-overlay p {
  font-size: 16px;
  color: #333;
  margin: 0;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.delete-modal,
.details-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content,
.details-modal-content {
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.modal-content {
  padding: 20px;
  width: 400px;
  max-width: 90%;
}

.details-modal-content {
  width: 700px;
  max-width: 90%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.details-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #ddd;
}

.details-modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #777;
}

.details-modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: calc(90vh - 130px);
}

.detail-row {
  display: flex;
  margin-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
}

.detail-label {
  width: 180px;
  font-weight: bold;
  color: #555;
}

.detail-value {
  flex: 1;
  word-break: break-word;
}

.detail-multiline {
  white-space: pre-wrap;
}

.tag {
  display: inline-block;
  background-color: #e1f5fe;
  color: #0277bd;
  border-radius: 15px;
  padding: 4px 10px;
  margin: 3px;
  font-size: 12px;
  border: 1px solid #b3e5fc;
  transition: all 0.2s ease;
}

.tag:hover {
  background-color: #b3e5fc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.modal-actions button {
  margin-left: 10px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-btn {
  background-color: #e74c3c;
  color: white;
}

.cancel-btn {
  background-color: #7f8c8d;
  color: white;
}

.no-results {
  text-align: center;
  margin: 20px 0;
  color: #777;
}

.primary-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.primary-btn:hover {
  background-color: #2980b9;
}

.details-modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #ddd;
  display: flex;
  justify-content: flex-end;
}
</style>
