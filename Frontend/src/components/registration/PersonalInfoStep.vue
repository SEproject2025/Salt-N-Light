<template>
  <div class="form-step">
    <h2 class="step-title">Personal Information</h2>
    <div class="form-group">
      <label for="userType">User Type:</label>
      <select id="userType" v-model="localData.user_type" @change="updateData">
        <option value="">Select User Type (optional)</option>
        <option value="Missionary">Missionary</option>
        <option value="Supporter">Supporter</option>
      </select>

      <div class="form-row">
        <div class="form-col">
          <label for="firstName">First Name:</label>
          <input
            type="text"
            id="firstName"
            v-model="localData.first_name"
            placeholder="Enter your first name"
            maxlength="35"
            @input="updateData"
          />
        </div>
        <div class="form-col">
          <label for="lastName">Last Name:</label>
          <input
            type="text"
            id="lastName"
            v-model="localData.last_name"
            placeholder="Enter your last name"
            maxlength="35"
            @input="updateData"
          />
        </div>
      </div>

      <label for="phoneNumber">Phone Number:</label>
      <input
        type="tel"
        id="phoneNumber"
        v-model="localData.phone_number"
        placeholder="Enter your phone number"
        @input="validatePhoneNumber"
        @keypress="validatePhoneDigits"
      />
      <p v-if="phoneNumberError" class="error-message">
        {{ phoneNumberError }}
      </p>

      <label for="yearsOfExperience"
        >Years in Ministry:
        <span class="required-text"
          >If it's less than one year, please leave this field blank</span
        ></label
      >
      <input
        type="number"
        id="yearsOfExperience"
        v-model="localData.years_of_experience"
        min="0"
        max="500"
        placeholder="Enter the # of years in the ministry"
        @input="validateYearsOfExperience"
        @keypress="validateDigits"
      />
      <div v-if="yearsError" :class="['message-container', 'error-message']">
        {{ yearsError }}
      </div>

      <div class="anonymous-option">
        <label class="checkbox-label">
          <input
            type="checkbox"
            v-model="localData.is_anonymous"
            @change="updateData"
          />
          <span>Make my profile anonymous</span>
        </label>
        <p class="helper-text">
          Anonymous profiles will not appear in search results or matchmaking.
          Your profile will only be visible to you.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PersonalInfoStep",
  props: {
    personalData: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:personalData", "validation-status"],
  data() {
    return {
      localData: {
        user_type: this.personalData.user_type || "",
        first_name: this.personalData.first_name || "",
        last_name: this.personalData.last_name || "",
        phone_number: this.personalData.phone_number || "",
        years_of_experience: this.personalData.years_of_experience || null,
        is_anonymous: this.personalData.is_anonymous || false,
      },
      yearsError: "",
      firstNameError: "",
      lastNameError: "",
      phoneNumberError: "",
    };
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
      const years = this.localData.years_of_experience;
      if (years === null || years === "") {
        this.yearsError = "";
        this.updateData();
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
      this.updateData();
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
      const value = this.localData.phone_number;
      // Remove any non-digit characters
      const digitsOnly = value.replace(/\D/g, "");

      // Update the input value to only contain digits
      this.localData.phone_number = digitsOnly;

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
      this.updateData();
    },
    /* Updates parent with current personal information values */
    updateData() {
      this.$emit("update:personalData", {
        ...this.personalData,
        ...this.localData,
      });
      this.validateForm();
    },
    validateForm() {
      const isValid = !this.phoneNumberError && !this.yearsError;
      this.$emit("validation-status", isValid);
    },
  },
  watch: {
    /* Syncs local data when parent data changes */
    personalData: {
      handler(newValue) {
        this.localData = {
          user_type: newValue.user_type || "",
          first_name: newValue.first_name || "",
          last_name: newValue.last_name || "",
          phone_number: newValue.phone_number || "",
          years_of_experience: newValue.years_of_experience || null,
          is_anonymous: newValue.is_anonymous || false,
        };
        this.validateForm();
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.message-container {
  margin: 2px 0;
  padding: 2px;
  border-radius: 8px;
  font-weight: 500;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: 0.95rem;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.anonymous-option {
  margin: 20px 0;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.helper-text {
  margin-top: 5px;
  font-size: 0.9rem;
  color: #666;
}

.error {
  border-color: #f44336;
}

.error-message {
  color: #f44336;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>
