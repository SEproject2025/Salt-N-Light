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
          <label>First Name</label>
          <input v-model="formData.first_name" type="text" maxlength="35" />
          <span class="error-message" v-if="errors.first_name">{{
            errors.first_name
          }}</span>
        </div>

        <div class="form-group">
          <label>Last Name</label>
          <input v-model="formData.last_name" type="text" maxlength="35" />
          <span class="error-message" v-if="errors.last_name">{{
            errors.last_name
          }}</span>
        </div>

        <div class="form-group">
          <label>User Type</label>
          <select v-model="formData.user_type">
            <option value="">Select User Type (optional)</option>
            <option value="Missionary">Missionary</option>
            <option value="Supporter">Supporter</option>
          </select>
        </div>

        <div class="form-group">
          <label>Phone Number</label>
          <input
            v-model="formData.phone_number"
            type="tel"
            placeholder="Enter your phone number"
            @input="validatePhoneNumber"
            @keypress="validatePhoneDigits"
          />
          <span class="error-message" v-if="errors.phone_number">{{
            errors.phone_number
          }}</span>
        </div>

        <div class="form-group">
          <label>Street Address</label>
          <input v-model="formData.street_address" type="text" maxlength="65" />
          <span class="error-message" v-if="errors.street_address">{{
            errors.street_address
          }}</span>
        </div>

        <div class="form-group">
          <label>City</label>
          <input v-model="formData.city" type="text" maxlength="35" />
          <span class="error-message" v-if="errors.city">{{
            errors.city
          }}</span>
        </div>

        <div class="form-group">
          <label>State</label>
          <input v-model="formData.state" type="text" maxlength="35" />
          <span class="error-message" v-if="errors.state">{{
            errors.state
          }}</span>
        </div>

        <div class="form-group">
          <label>Country</label>
          <select
            v-model="formData.country"
            class="country-select"
            @change="handleCountryChange"
          >
            <option value="">Select your country</option>
            <option
              v-for="country in commonCountries"
              :key="country.code"
              :value="country.name"
            >
              {{ country.name }}
            </option>
            <option value="Other">Other (specify below)</option>
          </select>
          <div v-if="formData.country === 'Other'" class="other-country-input">
            <input
              type="text"
              v-model="formData.other_country"
              placeholder="Enter your country"
            />
          </div>
          <span class="error-message" v-if="errors.country">{{
            errors.country
          }}</span>
        </div>

        <div class="form-group">
          <label
            >Years in Ministry:
            <span class="required-text"
              >If it's less than one year, please leave this field blank</span
            >
          </label>
          <input
            v-model="formData.years_of_experience"
            type="number"
            min="0"
            max="500"
            placeholder="Enter the # of years in the ministry"
            @input="validateYearsOfExperience"
            @keypress="validateDigits"
          />
          <span class="error-message" v-if="errors.years_of_experience">{{
            errors.years_of_experience
          }}</span>
        </div>
      </div>

      <div class="form-group full-width">
        <label>Tags</label>
        <select v-model="formData.selectedTags" multiple class="tag-select">
          <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
            {{ tag.name }}
          </option>
        </select>
      </div>

      <div class="form-group full-width">
        <label>Description</label>
        <textarea
          v-model="formData.description"
          rows="4"
          maxlength="1000"
        ></textarea>
        <div
          class="char-counter"
          :class="{ 'near-limit': formData.description.length > 900 }"
        >
          {{ formData.description.length }}/1000 characters
        </div>
        <span class="error-message" v-if="errors.description">{{
          errors.description
        }}</span>
      </div>

      <div class="form-actions">
        <button type="submit" class="save-btn">
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
        other_country: "",
        years_of_experience: null,
        description: "",
        selectedTags: [],
      },
      errors: {
        first_name: "",
        last_name: "",
        phone_number: "",
        street_address: "",
        city: "",
        state: "",
        country: "",
        years_of_experience: "",
        description: "",
      },
      commonCountries: [
        { code: "US", name: "United States" },
        { code: "CA", name: "Canada" },
        { code: "GB", name: "United Kingdom" },
        { code: "AU", name: "Australia" },
        { code: "DE", name: "Germany" },
        { code: "FR", name: "France" },
        { code: "JP", name: "Japan" },
        { code: "IN", name: "India" },
        { code: "BR", name: "Brazil" },
        { code: "ZA", name: "South Africa" },
      ],
    };
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
    validateFirstName() {
      if (this.formData.first_name.length > 35) {
        this.errors.first_name = "First name cannot exceed 35 characters";
        return false;
      }
      this.errors.first_name = "";
      return true;
    },

    validateLastName() {
      if (this.formData.last_name.length > 35) {
        this.errors.last_name = "Last name cannot exceed 35 characters";
        return false;
      }
      this.errors.last_name = "";
      return true;
    },

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
        this.errors.phone_number = "";
      } else if (digitsOnly.length < 10) {
        this.errors.phone_number = "Phone number must be at least 10 digits";
      } else if (digitsOnly.length > 15) {
        this.errors.phone_number = "Phone number must not exceed 15 digits";
      } else {
        this.errors.phone_number = "";
      }
    },
    validateYearsOfExperience() {
      const years = this.formData.years_of_experience;
      if (years === null || years === "") {
        this.errors.years_of_experience = "";
        return;
      }

      const numYears = Number(years);
      if (isNaN(numYears) || numYears < 0) {
        this.errors.years_of_experience = "Please enter a valid number";
      } else if (!Number.isInteger(numYears)) {
        this.errors.years_of_experience = "Please enter a whole number";
      } else if (numYears > 500) {
        this.errors.years_of_experience =
          "Years of experience cannot exceed 500";
      } else {
        this.errors.years_of_experience = "";
      }
    },
    handleCountryChange() {
      if (this.formData.country !== "Other") {
        this.formData.other_country = "";
      }
    },

    validateStreetAddress() {
      if (!this.formData.street_address) {
        this.errors.street_address = "";
        return true;
      }
      if (this.formData.street_address.length > 65) {
        this.errors.street_address = "Address cannot exceed 65 characters";
        return false;
      }
      this.errors.street_address = "";
      return true;
    },

    validateCity() {
      if (!this.formData.city) {
        this.errors.city = "";
        return true;
      }
      if (this.formData.city.length > 35) {
        this.errors.city = "City cannot exceed 35 characters";
        return false;
      }
      this.errors.city = "";
      return true;
    },

    validateState() {
      if (!this.formData.state) {
        this.errors.state = "";
        return true;
      }
      if (this.formData.state.length > 35) {
        this.errors.state = "State cannot exceed 35 characters";
        return false;
      }
      this.errors.state = "";
      return true;
    },

    validateDescription() {
      if (!this.formData.description) {
        this.errors.description = "";
        return true;
      }
      if (this.formData.description.length > 1000) {
        this.errors.description = "Description cannot exceed 1000 characters";
        return false;
      }
      this.errors.description = "";
      return true;
    },

    validateForm() {
      return (
        this.validateFirstName() &&
        this.validateLastName() &&
        this.validatePhoneNumber() &&
        this.validateStreetAddress() &&
        this.validateCity() &&
        this.validateState() &&
        this.validateYearsOfExperience() &&
        this.validateDescription()
      );
    },

    handleSubmit() {
      if (!this.validateForm()) {
        return;
      }

      const formDataToSubmit = {
        ...this.formData,
        tags: this.formData.selectedTags,
        user_type: this.formData.user_type.toLowerCase(),
        years_of_experience: this.formData.years_of_experience || 0,
      };
      this.$emit("submit", formDataToSubmit);
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

.tag-select {
  min-height: 100px;
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

.cancel-btn {
  background: #e74c3c;
  color: white;
}

.cancel-btn:hover {
  background: #c0392b;
}

.error-message {
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 0.3rem;
  display: block;
}

.form-group input.error,
.form-group textarea.error {
  border-color: #e74c3c;
}

.char-counter {
  font-size: 0.8rem;
  color: #757575;
  text-align: right;
  margin-top: 5px;
}

.char-counter.near-limit {
  color: #ff9800;
  font-weight: 500;
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