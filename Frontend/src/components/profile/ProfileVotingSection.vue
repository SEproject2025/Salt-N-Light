<template>
  <div class="voting-section">
    <div class="voting-card">
      <h2>Profile Rating</h2>

      <div class="vote-count">
        <span class="score">{{ profile.vote_count || 0 }}</span>
        <span class="label">Total Score</span>
      </div>

      <div class="vote-buttons" v-if="canVote">
        <button
          :class="['vote-btn', 'upvote', { active: currentUserVote === true }]"
          @click="vote(true)"
        >
          <font-awesome-icon icon="thumbs-up" />
        </button>
        <button
          :class="[
            'vote-btn',
            'downvote',
            { active: currentUserVote === false },
          ]"
          @click="vote(false)"
        >
          <font-awesome-icon icon="thumbs-down" />
        </button>
      </div>

      <div v-if="canVote">
        <div v-if="showVoteMessage" class="info-message">
          Please vote before adding a comment
        </div>

        <div v-if="showCommentForm" class="comment-section">
          <h3>Add a Comment</h3>
          <textarea
            v-model="newComment"
            placeholder="Share your thoughts..."
          ></textarea>
          <button
            class="submit-comment"
            @click="submitComment"
            :disabled="!newComment.trim()"
          >
            Submit Comment
          </button>
        </div>
      </div>

      <div class="comments-list">
        <h3>Comments</h3>
        <div v-if="profile.comments && profile.comments.length > 0">
          <div
            v-for="comment in profile.comments"
            :key="comment.id"
            class="comment"
          >
            <div class="comment-header">
              <span class="commenter">{{ comment.commenter_username }}</span>
              <div class="comment-actions">
                <span class="date">{{ formatDate(comment.created_at) }}</span>
                <button
                  v-if="isCommentOwner(comment)"
                  class="edit-btn"
                  @click="startEditing(comment)"
                >
                  <font-awesome-icon icon="edit" /> Edit
                </button>
              </div>
            </div>
            <div v-if="editingCommentId === comment.id" class="edit-comment">
              <textarea
                v-model="editedComment"
                class="edit-textarea"
              ></textarea>
              <div class="edit-actions">
                <button class="save-btn" @click="saveEdit(comment)">
                  Save
                </button>
                <button class="cancel-btn" @click="cancelEdit">Cancel</button>
              </div>
            </div>
            <p v-else class="comment-text">{{ comment.comment }}</p>
          </div>
        </div>
        <div v-else class="no-comments">No comments yet</div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios.js";
import { jwtDecode } from "jwt-decode";

export default {
  name: "ProfileVotingSection",
  props: {
    profile: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      currentUserVote: null,
      newComment: "",
      hasCommented: false,
      hasVoted: false,
      editingCommentId: null,
      editedComment: "",
      currentUser: null,
    };
  },
  computed: {
    canVote() {
      const currentUserId = this.getCurrentUserId();
      return currentUserId && currentUserId !== this.profile.user.id;
    },
    showCommentForm() {
      return this.canVote && this.hasVoted && !this.hasCommented;
    },
    showVoteMessage() {
      return this.canVote && !this.hasVoted && !this.hasCommented;
    },
  },
  watch: {
    profile: {
      immediate: true,
      handler(newProfile) {
        if (newProfile && newProfile.user) {
          this.updateUserState(newProfile);
        }
      },
    },
  },
  methods: {
    async fetchCurrentUser() {
      try {
        const response = await api.get(`api/profiles/me/`, {
          headers: this.getAuthHeader(),
        });
        this.currentUser = response.data;
        return response.data;
      } catch (error) {
        console.error("Failed to fetch current user:", error);
        return null;
      }
    },

    getCurrentUsername() {
      return this.currentUser?.user?.username || null;
    },

    async updateUserState(profile) {
      if (!profile || !profile.user) return;

      try {
        // Get current user's vote status
        const voteResponse = await api.get(
          `api/profiles/${profile.user.id}/vote-status/`,
          { headers: this.getAuthHeader() }
        );

        this.currentUserVote = voteResponse.data.is_upvote;
        this.hasVoted = voteResponse.data.has_voted;

        // Check if current user has commented
        if (profile.comments) {
          const username = this.getCurrentUsername();
          this.hasCommented = profile.comments.some(
            (comment) => comment.commenter_username === username
          );
        }

        console.log("State updated:", {
          currentUserVote: this.currentUserVote,
          hasVoted: this.hasVoted,
          hasCommented: this.hasCommented,
          username: this.getCurrentUsername() || "Not logged in",
        });
      } catch (error) {
        console.error("Error updating user state:", error);
      }
    },
    async refreshToken() {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        return false;
      }

      try {
        const response = await api.post(`api/token/refresh/`, {
          refresh: refreshToken,
        });
        localStorage.setItem("access_token", response.data.access);
        return true;
      } catch (err) {
        console.error("Token refresh failed", err);
        return false;
      }
    },

    getCurrentUserId() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const decodedToken = jwtDecode(token);
        return decodedToken.user_id;
      }
      return null;
    },

    async vote(isUpvote, retry = true) {
      try {
        const response = await api.post(
          `api/profiles/vote/`,
          {
            profile: this.profile.user.id,
            is_upvote: isUpvote,
          },
          {
            headers: this.getAuthHeader(),
          }
        );

        // Update local state based on response
        this.currentUserVote = response.data.is_upvote;
        this.hasVoted = true;

        // Emit event to refresh profile data
        this.$emit("vote-updated");
      } catch (error) {
        if (error.response?.status === 401 && retry) {
          const refreshed = await this.refreshToken();
          if (refreshed) {
            return this.vote(isUpvote, false);
          }
        }
        console.error("Voting failed:", error);
      }
    },

    async submitComment(retry = true) {
      if (!this.newComment.trim()) return;

      try {
        await api.post(
          `api/profiles/comment/`,
          {
            profile: this.profile.user.id,
            comment: this.newComment.trim(),
          },
          {
            headers: this.getAuthHeader(),
          }
        );
        this.hasCommented = true;
        this.newComment = "";
        this.$emit("comment-added");
      } catch (error) {
        if (error.response?.status === 401 && retry) {
          const refreshed = await this.refreshToken();
          if (refreshed) {
            return this.submitComment(false);
          }
        }
        console.error("Comment submission failed:", error);
      }
    },

    async saveEdit(comment, retry = true) {
      if (!this.editedComment.trim()) return;

      try {
        await api.patch(
          `api/profiles/comment/${comment.id}/`,
          {
            comment: this.editedComment.trim(),
          },
          {
            headers: this.getAuthHeader(),
          }
        );

        // Update the comment locally
        comment.comment = this.editedComment.trim();

        // Reset editing state
        this.editingCommentId = null;
        this.editedComment = "";

        // Emit event to refresh profile data
        this.$emit("comment-added");
      } catch (error) {
        if (error.response?.status === 401 && retry) {
          const refreshed = await this.refreshToken();
          if (refreshed) {
            return this.saveEdit(comment, false);
          }
        }
        console.error("Comment update failed:", error);
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },

    getAuthHeader() {
      const token = localStorage.getItem("access_token");
      return { Authorization: `Bearer ${token}` };
    },

    isCommentOwner(comment) {
      return comment.commenter_username === this.getCurrentUsername();
    },

    startEditing(comment) {
      this.editingCommentId = comment.id;
      this.editedComment = comment.comment;
    },

    cancelEdit() {
      this.editingCommentId = null;
      this.editedComment = "";
    },
  },
  async created() {
    await this.fetchCurrentUser();
    if (this.profile && this.profile.user) {
      this.updateUserState(this.profile);
    }
  },
};
</script>

<style scoped>
.voting-section {
  width: 300px;
  margin-left: 2rem;
}

.voting-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

h2 {
  margin: 0 0 1.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
  text-align: center;
}

.vote-count {
  text-align: center;
  margin-bottom: 1.5rem;
}

.score {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
  display: block;
}

.label {
  color: #666;
  font-size: 0.9rem;
}

.vote-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.vote-btn {
  padding: 0.8rem;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1.2rem;
}

.vote-btn.upvote {
  background: #e8f5e9;
  color: #2e7d32;
}

.vote-btn.downvote {
  background: #ffebee;
  color: #c62828;
}

.vote-btn.active {
  transform: scale(1.1);
}

.vote-btn.upvote.active {
  background: #2e7d32;
  color: white;
}

.vote-btn.downvote.active {
  background: #c62828;
  color: white;
}

.comment-section {
  margin-top: 2rem;
}

.comment-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 1rem;
  resize: vertical;
  min-height: 100px;
}

.submit-comment {
  width: 100%;
  padding: 0.8rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-comment:hover {
  background: #2980b9;
}

.submit-comment:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}

.comments-list {
  margin-top: 2rem;
}

.comment {
  border-bottom: 1px solid #eee;
  padding: 1rem 0;
}

.comment:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.commenter {
  font-weight: bold;
  color: #2c3e50;
}

.date {
  color: #666;
  font-size: 0.9rem;
}

.comment-text {
  margin: 0;
  line-height: 1.4;
}

.no-comments {
  color: #666;
  text-align: center;
  padding: 1rem 0;
}

.info-message {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  color: #666;
  text-align: center;
  margin-bottom: 1rem;
}

.comment-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.edit-btn {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background: #f8f9fa;
}

.edit-btn i {
  font-size: 0.8rem;
}

.edit-comment {
  margin-top: 0.5rem;
}

.edit-textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  resize: vertical;
  min-height: 60px;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-actions button {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.edit-actions .save-btn {
  background: #2ecc71;
  color: white;
}

.edit-actions .save-btn:hover {
  background: #27ae60;
}

.edit-actions .cancel-btn {
  background: #e74c3c;
  color: white;
}

.edit-actions .cancel-btn:hover {
  background: #c0392b;
}

@media (max-width: 1200px) {
  .voting-section {
    width: 100%;
    margin-left: 0;
    margin-top: 2rem;
  }
}
</style>
