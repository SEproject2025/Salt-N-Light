<template>
  <div class="profile-card">
    <div class="profile-header">
      <h1>{{ profile.first_name }} {{ profile.last_name }}</h1>
      <button @click="$emit('edit')" class="edit-btn">
        <i class="fas fa-edit"></i> Edit Profile
      </button>
    </div>

    <div class="profile-content">
      <div class="profile-section">
        <h3>Personal Information</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Username</span>
            <span class="value">{{ profile.user?.username }}</span>
          </div>
          <div class="info-item">
            <span class="label">Email</span>
            <span class="value">{{ profile.user?.email }}</span>
          </div>
          <div class="info-item">
            <span class="label">User Type</span>
            <span class="value">{{ profile.user_type }}</span>
          </div>
          <div class="info-item">
            <span class="label">Phone</span>
            <span class="value">{{ profile.phone_number }}</span>
          </div>
          <div class="info-item">
            <span class="label">Years of Experience</span>
            <span class="value">{{ profile.years_of_experience }}</span>
          </div>
        </div>
      </div>

      <div class="profile-section">
        <h3>Location</h3>
        <div class="address">
          <p>{{ profile.street_address }}</p>
          <p>{{ profile.city }}, {{ profile.state }}</p>
          <p>{{ profile.country }}</p>
        </div>
      </div>

      <div class="profile-section">
        <h3>Tags</h3>
        <div class="tags">
          <span v-for="tag in profile.tags" :key="tag.id" class="tag">
            {{ tag.name }}
          </span>
        </div>
      </div>

      <div class="profile-section">
        <h3>Description</h3>
        <p class="description">{{ profile.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileView",
  props: {
    profile: {
      type: Object,
      required: true,
    },
  },
  emits: ["edit"],
};
</script>

<style scoped>
.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.profile-header h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.8rem;
}

.profile-section {
  margin-bottom: 2rem;
}

.profile-section h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.3rem;
}

.value {
  font-size: 1.1rem;
  color: #2c3e50;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #e1f5fe;
  color: #0288d1;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.description {
  line-height: 1.6;
  color: #2c3e50;
}

.edit-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
  background: #3498db;
  color: white;
}

.edit-btn:hover {
  background: #2980b9;
}

@media (max-width: 1024px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    max-width: 100%;
  }
}
</style>