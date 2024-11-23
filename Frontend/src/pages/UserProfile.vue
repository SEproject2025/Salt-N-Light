<<<<<<< HEAD
<template>
   <div class="background-image">
     <div class="profile-page">
       <!-- Profile Header -->
       <header class="profile-header">
         <img :src="profile.profile_picture || defaultImage" class="profile-image" alt="Profile Picture" />
         <div class="profile-details">
           <h2>{{ profile.name || "Missionary Name" }}</h2>
           <p class="title">{{ profile.title || "Role/Ministry Focus" }}</p>
           <p class="location">{{ profile.location || "Location Not Provided" }}</p>
           <p>{{ profile.followers }} Followers</p>
           <button v-if="isFollowing" @click="unfollow" class="btn btn-outline-secondary">Unfollow</button>
           <button v-else @click="follow" class="btn btn-primary">Follow</button>
           <button v-if="!isEditing" @click="toggleEdit" class="btn btn-outline-primary">Edit Profile</button>
         </div>
       </header>
 
       <!-- Profile Form for Editing -->
       <div v-if="isEditing" class="edit-form">
         <form @submit.prevent="saveProfile">
           <div class="form-group">
             <label for="name">Full Name</label>
             <input type="text" id="name" v-model="profile.name" class="form-control" />
           </div>
 
           <div class="form-group">
             <label for="title">Title/Ministry Focus</label>
             <input type="text" id="title" v-model="profile.title" class="form-control" />
           </div>
 
           <div class="form-group">
             <label for="location">Location</label>
             <input type="text" id="location" v-model="profile.location" class="form-control" />
           </div>
 
           <div class="form-group">
             <label for="description">Description</label>
             <textarea id="description" v-model="profile.description" class="form-control"></textarea>
           </div>
 
           <div class="form-group">
             <label for="profile-picture">Profile Picture</label>
             <input type="file" @change="onFileChange" class="form-control-file" />
           </div>
 
           <button type="submit" class="btn btn-success">Save</button>
           <button type="button" @click="toggleEdit" class="btn btn-secondary">Cancel</button>
         </form>
       </div>
 
       <!-- About Section (View Mode) -->
       <section v-else class="about-section">
         <h3>About</h3>
         <p>{{ profile.description || "This missionary has not provided a bio." }}</p>
       </section>
 
       <!-- Activity Section -->
       <section class="activity-section">
         <h3>Recent Activity</h3>
         <div v-if="activity.length > 0">
           <div v-for="post in activity" :key="post.id" class="activity-post">
             <p>{{ post.text }}</p>
           </div>
         </div>
         <p v-else>No recent activity available.</p>
       </section>
 
       <!-- Connections Section -->
       <section class="connections-section">
         <h3>People You May Know</h3>
         <div class="connections-list">
           <div v-for="connection in connections" :key="connection.id" class="connection-card">
             <img :src="connection.profile_picture || defaultImage" class="connection-image" />
             <p>{{ connection.name }}</p>
             <button class="btn btn-outline-primary btn-sm" @click="connect(connection.id)">Connect</button>
           </div>
         </div>
       </section>
 
       <!-- Contact Information -->
       <section class="contact-info-section">
         <h3>Contact Information</h3>
         <p>Email: {{ profile.email || "Not provided" }}</p>
         <p>Website: <a :href="profile.website">{{ profile.website || "Not provided" }}</a></p>
       </section>
     </div>
   </div>
 </template>
 
 <script>
 import axios from "axios";
 
 export default {
  name: "UserProfile",
   data() {
     return {
       profile: {
         profile_picture: "",
         name: "",
         title: "",
         location: "",
         followers: 0,
         description: "",
         email: "",
         website: ""
       },
       activity: [],
       connections: [],
       isFollowing: false,
       isEditing: false,
       defaultImage: require("@/assets/pictures/defaultProfilePicture.png")
     };
   },
   methods: {
     async fetchProfile() {
       try {
         const response = await axios.get("http://127.0.0.1:8000/userprofile/");
         this.profile = response.data;
       } catch (error) {
         console.error("Error fetching profile:", error);
       }
     },
     async saveProfile() {
       try {
         const formData = new FormData();
         formData.append("name", this.profile.name);
         formData.append("title", this.profile.title);
         formData.append("location", this.profile.location);
         formData.append("description", this.profile.description);
         if (this.profile.profile_picture instanceof File) {
           formData.append("profile_picture", this.profile.profile_picture);
         }
         await axios.put("http://127.0.0.1:8000/userprofile/", formData);
         this.isEditing = false;
         this.fetchProfile();
       } catch (error) {
         console.error("Error saving profile:", error);
       }
     },
     toggleEdit() {
       this.isEditing = !this.isEditing;
     },
     async fetchActivity() {
       try {
         const response = await axios.get("http://127.0.0.1:8000/useractivity/");
         this.activity = response.data;
       } catch (error) {
         console.error("Error fetching activity:", error);
       }
     },
     async fetchConnections() {
       try {
         const response = await axios.get("http://127.0.0.1:8000/userconnections/");
         this.connections = response.data;
       } catch (error) {
         console.error("Error fetching connections:", error);
       }
     },
     async follow() {
       try {
         await axios.post(`http://127.0.0.1:8000/follow/${this.profile.id}`);
         this.isFollowing = true;
         this.profile.followers += 1;
       } catch (error) {
         console.error("Error following user:", error);
       }
     },
     async unfollow() {
       try {
         await axios.post(`http://127.0.0.1:8000/unfollow/${this.profile.id}`);
         this.isFollowing = false;
         this.profile.followers -= 1;
       } catch (error) {
         console.error("Error unfollowing user:", error);
       }
     },
     onFileChange(event) {
       this.profile.profile_picture = event.target.files[0];
     }
   },
   mounted() {
     this.fetchProfile();
     this.fetchActivity();
     this.fetchConnections();
   }
 };
 </script>
 
 <style scoped>
 .background-image {
  background-image: url("@/assets/pictures/defaultBackground.jpg");
   background-size: cover;
   background-position: center;
   min-height: 100vh;
   display: flex;
   justify-content: center;
   align-items: center;
 }
 .profile-page {
   max-width: 800px;
   padding: 20px;
   background: #ffffff;
   border-radius: 8px;
   box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
   color: #333;
   font-family: Arial, sans-serif;
 }
 .profile-header {
   display: flex;
   align-items: center;
   margin-bottom: 20px;
   border-bottom: 1px solid #eaeaea;
   padding-bottom: 15px;
 }
 .profile-image {
   width: 100px;
   height: 100px;
   border-radius: 50%;
   object-fit: cover;
   margin-right: 20px;
   box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
 }
 .profile-details h2 {
   margin: 0;
   font-size: 24px;
   color: #333;
 }
 .profile-details .title,
 .profile-details .location,
 .profile-details p {
   margin: 5px 0;
   color: #666;
   font-size: 14px;
 }
 .about-section, .activity-section, .connections-section, .contact-info-section {
   margin-top: 20px;
 }
 .about-section h3,
 .activity-section h3,
 .connections-section h3,
 .contact-info-section h3 {
   font-size: 18px;
   color: #333;
   border-bottom: 2px solid #0073b1;
   padding-bottom: 5px;
 }
 .edit-form .form-group {
   margin-bottom: 15px;
 }
 .connection-card {
   display: flex;
   align-items: center;
   margin-bottom: 10px;
 }
 .connection-image {
   width: 50px;
   height: 50px;
   border-radius: 50%;
   object-fit: cover;
   margin-right: 10px;
   box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
 }
 .btn {
   font-size: 14px;
   padding: 5px 10px;
 }
 .btn-primary {
   background-color: #0073b1;
   border-color: #0073b1;
   color: #fff;
 }
 .btn-outline-primary {
   border-color: #0073b1;
   color: #0073b1;
 }
 .btn-outline-secondary {
   border-color: #777;
   color: #777;
 }
 .btn-success {
   background-color: #28a745;
   border-color: #28a745;
 }
 </style>
 
=======
<template>
  <div class="background-image">
    <div class="profile-page">
      <!-- Profile Header -->
      <header class="profile-header">
        <img
          :src="profile.profile_picture || defaultImage"
          class="profile-image"
          alt="Profile Picture"
        />
        <div class="profile-details">
          <h2>{{ profile.name || "Missionary Name" }}</h2>
          <p class="title">{{ profile.title || "Role/Ministry Focus" }}</p>
          <p class="location">
            {{ profile.location || "Location Not Provided" }}
          </p>
          <p>{{ profile.followers }} Followers</p>
          <button
            v-if="isFollowing"
            @click="unfollow"
            class="btn btn-outline-secondary"
          >
            Unfollow
          </button>
          <button v-else @click="follow" class="btn btn-primary">Follow</button>
          <button
            v-if="!isEditing"
            @click="toggleEdit"
            class="btn btn-outline-primary"
          >
            Edit Profile
          </button>
        </div>
      </header>

      <!-- Profile Form for Editing -->
      <div v-if="isEditing" class="edit-form">
        <form @submit.prevent="saveProfile">
          <div class="form-group">
            <label for="name">Full Name</label>
            <input
              type="text"
              id="name"
              v-model="profile.name"
              class="form-control"
            />
          </div>

          <div class="form-group">
            <label for="title">Title/Ministry Focus</label>
            <input
              type="text"
              id="title"
              v-model="profile.title"
              class="form-control"
            />
          </div>

          <div class="form-group">
            <label for="location">Location</label>
            <input
              type="text"
              id="location"
              v-model="profile.location"
              class="form-control"
            />
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="profile.description"
              class="form-control"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="profile-picture">Profile Picture</label>
            <input
              type="file"
              @change="onFileChange"
              class="form-control-file"
            />
          </div>

          <button type="submit" class="btn btn-success">Save</button>
          <button type="button" @click="toggleEdit" class="btn btn-secondary">
            Cancel
          </button>
        </form>
      </div>

      <!-- About Section (View Mode) -->
      <section v-else class="about-section">
        <h3>About</h3>
        <p>
          {{ profile.description || "This missionary has not provided a bio." }}
        </p>
      </section>

      <!-- Activity Section -->
      <section class="activity-section">
        <h3>Recent Activity</h3>
        <div v-if="activity.length > 0">
          <div v-for="post in activity" :key="post.id" class="activity-post">
            <p>{{ post.text }}</p>
          </div>
        </div>
        <p v-else>No recent activity available.</p>
      </section>

      <!-- Connections Section -->
      <section class="connections-section">
        <h3>People You May Know</h3>
        <div class="connections-list">
          <div
            v-for="connection in connections"
            :key="connection.id"
            class="connection-card"
          >
            <img
              :src="connection.profile_picture || defaultImage"
              class="connection-image"
            />
            <p>{{ connection.name }}</p>
            <button
              class="btn btn-outline-primary btn-sm"
              @click="connect(connection.id)"
            >
              Connect
            </button>
          </div>
        </div>
      </section>

      <!-- Contact Information -->
      <section class="contact-info-section">
        <h3>Contact Information</h3>
        <p>Email: {{ profile.email || "Not provided" }}</p>
        <p>
          Website:
          <a :href="profile.website">{{ profile.website || "Not provided" }}</a>
        </p>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserProfile",
  data() {
    return {
      profile: {
        profile_picture: "",
        name: "",
        title: "",
        location: "",
        followers: 0,
        description: "",
        email: "",
        website: "",
      },
      activity: [],
      connections: [],
      isFollowing: false,
      isEditing: false,
      defaultImage: require("@/assets/pictures/defaultProfilePicture.png"),
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/userprofile/");
        this.profile = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },
    async saveProfile() {
      try {
        const formData = new FormData();
        formData.append("name", this.profile.name);
        formData.append("title", this.profile.title);
        formData.append("location", this.profile.location);
        formData.append("description", this.profile.description);
        if (this.profile.profile_picture instanceof File) {
          formData.append("profile_picture", this.profile.profile_picture);
        }
        await axios.put("http://127.0.0.1:8000/userprofile/", formData);
        this.isEditing = false;
        this.fetchProfile();
      } catch (error) {
        console.error("Error saving profile:", error);
      }
    },
    toggleEdit() {
      this.isEditing = !this.isEditing;
    },
    async fetchActivity() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/useractivity/");
        this.activity = response.data;
      } catch (error) {
        console.error("Error fetching activity:", error);
      }
    },
    async fetchConnections() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/userconnections/"
        );
        this.connections = response.data;
      } catch (error) {
        console.error("Error fetching connections:", error);
      }
    },
    async follow() {
      try {
        await axios.post(`http://127.0.0.1:8000/follow/${this.profile.id}`);
        this.isFollowing = true;
        this.profile.followers += 1;
      } catch (error) {
        console.error("Error following user:", error);
      }
    },
    async unfollow() {
      try {
        await axios.post(`http://127.0.0.1:8000/unfollow/${this.profile.id}`);
        this.isFollowing = false;
        this.profile.followers -= 1;
      } catch (error) {
        console.error("Error unfollowing user:", error);
      }
    },
    onFileChange(event) {
      this.profile.profile_picture = event.target.files[0];
    },
  },
  mounted() {
    this.fetchProfile();
    this.fetchActivity();
    this.fetchConnections();
  },
};
</script>

<style scoped>
.background-image {
  background-image: url("@/assets/pictures/defaultBackground.jpg");
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.profile-page {
  max-width: 800px;
  padding: 20px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  color: #333;
  font-family: Arial, sans-serif;
}
.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 15px;
}
.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 20px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}
.profile-details h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}
.profile-details .title,
.profile-details .location,
.profile-details p {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
}
.about-section,
.activity-section,
.connections-section,
.contact-info-section {
  margin-top: 20px;
}
.about-section h3,
.activity-section h3,
.connections-section h3,
.contact-info-section h3 {
  font-size: 18px;
  color: #333;
  border-bottom: 2px solid #0073b1;
  padding-bottom: 5px;
}
.edit-form .form-group {
  margin-bottom: 15px;
}
.connection-card {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.connection-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
}
.btn {
  font-size: 14px;
  padding: 5px 10px;
}
.btn-primary {
  background-color: #0073b1;
  border-color: #0073b1;
  color: #fff;
}
.btn-outline-primary {
  border-color: #0073b1;
  color: #0073b1;
}
.btn-outline-secondary {
  border-color: #777;
  color: #777;
}
.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}
</style>
>>>>>>> QA
