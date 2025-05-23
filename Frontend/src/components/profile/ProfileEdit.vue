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
          <label for="streetAddress">Street Address:</label>
          <input
            id="streetAddress"
            name="streetAddress"
            v-model="formData.street_address"
            type="text"
            placeholder="Enter your street address"
          />
        </div>

        <div class="form-group">
          <label for="city">City:</label>
          <input
            id="city"
            name="city"
            v-model="formData.city"
            type="text"
            placeholder="Enter your city"
          />
        </div>

        <div class="form-group">
          <label for="state">State:</label>
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
          <select
            id="country"
            v-model="formData.country"
            class="country-select"
            required
            @change="handleCountryChange"
          >
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
              required
            />
          </div>
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
        <div class="tags-container">
          <div class="tags-grid">
            <div
              v-for="tag in availableTags"
              :key="tag.id"
              class="tag-option"
              :class="{ selected: formData.selectedTags.includes(tag.id) }"
              @click="toggleTag(tag.id)"
            >
              {{ tag.name }}
            </div>
          </div>
        </div>
      </div>

      <div class="form-group full-width description-section">
        <label for="description">Description:</label>
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
        other_country: "",
        years_of_experience: "",
        description: "",
        selectedTags: [],
      },
      yearsError: "",
      phoneNumberError: "",
      commonCountries: [
        { code: "US", name: "United States" },
        { code: "CA", name: "Canada" },
        { code: "GB", name: "United Kingdom" },
        { code: "AU", name: "Australia" },
        { code: "NZ", name: "New Zealand" },
        { code: "IN", name: "India" },
        { code: "PH", name: "Philippines" },
        { code: "SG", name: "Singapore" },
        { code: "MY", name: "Malaysia" },
        { code: "ID", name: "Indonesia" },
      ],
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

    // Handle country initialization
    if (this.profile.country) {
      // Check if the country is in our common countries list
      const isCommonCountry = this.commonCountries.some(
        (country) => country.name === this.profile.country
      );

      if (!isCommonCountry) {
        // If it's not a common country, set it as "Other" and put the value in other_country
        this.formData.country = "Other";
        this.formData.other_country = this.profile.country;
      } else {
        // If it is a common country, set it directly
        this.formData.country = this.profile.country;
      }
    }
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
    handleCountryChange() {
      if (this.formData.country !== "Other") {
        this.formData.other_country = "";
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

      // Handle country value - if "Other" is selected, use other_country value
      const countryValue =
        this.formData.country === "Other"
          ? this.formData.other_country
          : this.formData.country;

      const formDataToSubmit = {
        first_name: this.formData.first_name,
        last_name: this.formData.last_name,
        user_type: this.formData.user_type.toLowerCase(),
        phone_number: this.formData.phone_number || null,
        street_address: this.formData.street_address || null,
        city: this.formData.city || null,
        state: this.formData.state || null,
        country: countryValue || null,
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
  font-weight: 600;
  margin-bottom: 1rem;
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

.tags-container {
  margin-top: 5px;
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 5px;
  margin-top: 5px;
}

.tag-option {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s ease;
}

.tag-option:hover {
  background-color: #f0f0f0;
}

.tag-option.selected {
  background-color: #e3f2fd;
  border-color: #2196f3;
  color: #1976d2;
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
  background: #3498db;
  color: white;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-btn:hover {
  background: #3498db;
}

.save-btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
  opacity: 0.7;
}

.cancel-btn {
  background: #e74c3c;
  color: white;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
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

.country-select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
  background-color: white;
  cursor: pointer;
}

.country-select:focus {
  border-color: #3498db;
  outline: none;
}

.other-country-input {
  margin-top: 0.5rem;
}

.other-country-input input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.other-country-input input:focus {
  border-color: #3498db;
  outline: none;
}

.description-section {
  margin-top: 2rem;
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
