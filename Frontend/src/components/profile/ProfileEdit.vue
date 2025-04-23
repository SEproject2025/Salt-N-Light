<template>
  <div class="profile-card edit-mode">
    <div class="profile-header">
      <h1>Edit Profile</h1>
      <button @click="$emit('cancel')" class="cancel-btn">
        <i class="fas fa-times"></i> Cancel
      </button>
    </div>

    <form @submit.prevent="handleSubmit" class="edit-form">
      <div class="form-grid">
        <div class="form-group">
          <label for="firstName">First Name:</label>
          <input
            id="firstName"
            name="firstName"
            v-model="formData.first_name"
            type="text"
            maxlength="35"
            placeholder="Enter your first name"
          />
        </div>

        <div class="form-group">
          <label for="lastName">Last Name:</label>
          <input
            id="lastName"
            name="lastName"
            v-model="formData.last_name"
            type="text"
            maxlength="35"
            placeholder="Enter your last name"
          />
        </div>

        <div class="form-group">
          <label for="userType">User Type:</label>
          <select id="userType" name="userType" v-model="formData.user_type">
            <option value="" disabled selected>
              Select user type (optional)
            </option>
            <option value="supporter">Supporter</option>
            <option value="missionary">Missionary</option>
          </select>
        </div>

        <div class="form-group">
          <label for="phoneNumber">Phone Number:</label>
          <input
            id="phoneNumber"
            name="phoneNumber"
            v-model="formData.phone_number"
            type="text"
            @input="validatePhoneNumber"
            @keypress="validatePhoneDigits"
            placeholder="Enter your phone number"
          />
          <p v-if="phoneNumberError" class="error-message">
            {{ phoneNumberError }}
          </p>
        </div>

        <div class="form-group">
          <label for="streetAddress">Street Address</label>
          <input
            id="streetAddress"
            name="streetAddress"
            v-model="formData.street_address"
            type="text"
            placeholder="Enter your street address"
          />
        </div>

        <div class="form-group">
          <label for="city">City</label>
          <input
            id="city"
            name="city"
            v-model="formData.city"
            type="text"
            placeholder="Enter your city"
          />
        </div>

        <div class="form-group">
          <label for="state">State</label>
          <input
            id="state"
            name="state"
            v-model="formData.state"
            type="text"
            placeholder="Enter your state"
          />
        </div>

        <div class="form-group">
          <label for="country">
            <span class="required">*</span> Country:
            <span class="required-text">required</span>
          </label>
          <input
            id="country"
            name="country"
            v-model="formData.country"
            type="text"
            required
            placeholder="Enter your country"
          />
        </div>

        <div class="form-group">
          <label for="yearsOfExperience"
            >Years in Ministry:
            <span class="required-text"
              >If it's less than one year, please leave this field blank</span
            ></label
          >
          <input
            id="yearsOfExperience"
            name="yearsOfExperience"
            v-model="formData.years_of_experience"
            type="number"
            min="0"
            max="500"
            @input="validateYearsOfExperience"
            @keypress="validateDigits"
            placeholder="Enter the # of years in the ministry"
          />
          <p v-if="yearsError" class="error-message">{{ yearsError }}</p>
        </div>
      </div>

      <div class="form-group full-width">
        <label for="tags">Select some tags that describe your ministry:</label>
        <div class="tag-selection-container">
          <div class="tag-list">
            <div
              v-for="tag in availableTags"
              :key="tag.id"
              class="tag-item"
              :class="{ selected: formData.selectedTags.includes(tag.id) }"
              @click="toggleTag(tag.id)"
            >
              {{ tag.name }}
            </div>
          </div>
        </div>
      </div>

      <div class="form-group full-width">
        <label for="description">Description</label>
        <textarea
          id="description"
          name="description"
          v-model="formData.description"
          rows="4"
          maxlength="1000"
          placeholder="Tell us about yourself and your mission"
          @input="handleDescriptionInput"
        ></textarea>
        <div
          class="char-counter"
          :class="{
            'near-limit': formData.description?.length > 800,
            'at-limit': formData.description?.length >= 1000,
          }"
        >
          {{ formData.description?.length || 0 }}/1000
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="save-btn" :disabled="!isFormValid">
          <i class="fas fa-save"></i> Save Changes
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "ProfileEdit",
  props: {
    profile: {
      type: Object,
      required: true,
    },
    availableTags: {
      type: Array,
      required: true,
    },
    selectedTags: {
      type: Array,
      required: true,
    },
  },
  emits: ["cancel", "submit"],
  data() {
    return {
      formData: {
        first_name: "",
        last_name: "",
        user_type: "",
        phone_number: "",
        street_address: "",
        city: "",
        state: "",
        country: "",
        years_of_experience: "",
        description: "",
        selectedTags: [],
      },
      yearsError: "",
      phoneNumberError: "",
    };
  },
  computed: {
    isFormValid() {
      // Check if there are any validation errors
      const hasErrors = this.yearsError || this.phoneNumberError;

      // Only check if country is filled
      const hasRequiredFields = this.formData.country?.trim();

      // Form is valid if there are no errors and country is filled
      return !hasErrors && hasRequiredFields;
    },
  },
  created() {
    // Initialize form data with profile data
    Object.keys(this.formData).forEach((key) => {
      if (key !== "selectedTags") {
        this.formData[key] = this.profile[key] || "";
      }
    });
    this.formData.selectedTags = [...this.selectedTags];
  },
  methods: {
    validateDigits(event) {
      // Allow only digits and control keys
      if (
        !/[0-9]/.test(event.key) &&
        event.key !== "Backspace" &&
        event.key !== "Delete" &&
        event.key !== "ArrowLeft" &&
        event.key !== "ArrowRight" &&
        event.key !== "Tab"
      ) {
        event.preventDefault();
      }
    },
    validateYearsOfExperience() {
      const years = this.formData.years_of_experience;
      if (years === null || years === "") {
        this.yearsError = "";
        return;
      }

      const numYears = Number(years);
      if (isNaN(numYears) || numYears < 0) {
        this.yearsError = "Please enter a valid number";
      } else if (!Number.isInteger(numYears)) {
        this.yearsError = "Please enter a whole number";
      } else if (numYears > 500) {
        this.yearsError = "Years of experience cannot exceed 500";
      } else {
        this.yearsError = "";
      }
    },
    validatePhoneDigits(event) {
      // Allow only digits and control keys
      if (
        !/[0-9]/.test(event.key) &&
        event.key !== "Backspace" &&
        event.key !== "Delete" &&
        event.key !== "ArrowLeft" &&
        event.key !== "ArrowRight" &&
        event.key !== "Tab"
      ) {
        event.preventDefault();
      }
    },
    validatePhoneNumber() {
      const value = this.formData.phone_number;
      // Remove any non-digit characters
      const digitsOnly = value.replace(/\D/g, "");

      // Update the input value to only contain digits
      this.formData.phone_number = digitsOnly;

      // If the field is empty, no validation needed
      if (!digitsOnly) {
        this.phoneNumberError = "";
      } else if (digitsOnly.length < 10) {
        this.phoneNumberError = "Phone number must be at least 10 digits";
      } else if (digitsOnly.length > 15) {
        this.phoneNumberError = "Phone number must not exceed 15 digits";
      } else {
        this.phoneNumberError = "";
      }
    },
    handleSubmit() {
      // Only proceed if there are no validation errors
      if (this.yearsError || this.phoneNumberError) {
        return;
      }

      // Filter out any undefined or null values from selectedTags
      const validTags = this.formData.selectedTags.filter(
        (tag) => tag !== undefined && tag !== null
      );

      const formDataToSubmit = {
        first_name: this.formData.first_name,
        last_name: this.formData.last_name,
        user_type: this.formData.user_type.toLowerCase(),
        phone_number: this.formData.phone_number || null,
        street_address: this.formData.street_address || null,
        city: this.formData.city || null,
        state: this.formData.state || null,
        country: this.formData.country || null,
        years_of_experience: this.formData.years_of_experience || 0,
        description: this.formData.description || null,
        tags: validTags,
      };

      console.log("Submitting form data:", formDataToSubmit);
      this.$emit("submit", formDataToSubmit);
    },
    toggleTag(tagId) {
      const index = this.formData.selectedTags.indexOf(tagId);
      if (index === -1) {
        this.formData.selectedTags.push(tagId);
      } else {
        this.formData.selectedTags.splice(index, 1);
      }
    },
    handleDescriptionInput() {
      // Ensure the description doesn't exceed 1000 characters
      if (this.formData.description?.length > 1000) {
        this.formData.description = this.formData.description.slice(0, 1000);
      }
    },
  },
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #3498db;
  outline: none;
}

.tag-selection-container {
  padding: 10px;
  background: white;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  max-height: 200px;
  overflow-y: auto;
  padding: 5px;
}

.tag-item {
  padding: 6px 12px;
  border-radius: 16px;
  background-color: #f0f0f0;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.tag-item:hover {
  background-color: #e0e0e0;
}

.tag-item.selected {
  background-color: #3498db;
  color: white;
}

.tag-item.selected:hover {
  background-color: #2980b9;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.save-btn,
.cancel-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.save-btn {
  background: #2ecc71;
  color: white;
}

.save-btn:hover {
  background: #27ae60;
}

.save-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
  opacity: 0.7;
}

.cancel-btn {
  background: #e74c3c;
  color: white;
}

.cancel-btn:hover {
  background: #c0392b;
}

.error-message {
  color: #e74c3c;
  font-size: 0.85rem;
  border-radius: 1px;
}

.char-counter {
  text-align: right;
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.25rem;
}

.char-counter.near-limit {
  color: #ff6b6b;
}

.char-counter.at-limit {
  color: #ff0000;
  font-weight: bold;
}

.required {
  color: #e74c3c;
  margin-right: 4px;
}

.required-text {
  color: #666;
  font-size: 0.8rem;
  margin-left: 4px;
  font-style: italic;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    max-width: 100%;
  }
}
</style>
