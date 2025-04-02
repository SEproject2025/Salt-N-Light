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
            @input="validateFirstName"
            :class="{ error: firstNameError }"
          />
          <p v-if="firstNameError" class="error-message">
            {{ firstNameError }}
          </p>
        </div>
        <div class="form-col">
          <label for="lastName">Last Name:</label>
          <input
            type="text"
            id="lastName"
            v-model="localData.last_name"
            placeholder="Enter your last name"
            @input="validateLastName"
            :class="{ error: lastNameError }"
          />
          <p v-if="lastNameError" class="error-message">{{ lastNameError }}</p>
        </div>
      </div>

      <label for="denomination">Denomination:</label>
      <input
        type="text"
        id="denomination"
        v-model="localData.denomination"
        placeholder="Enter your religious denomination"
        @input="updateData"
      />

      <label for="phoneNumber">Phone Number:</label>
      <input
        type="tel"
        id="phoneNumber"
        v-model="localData.phone_number"
        placeholder="Enter your phone number"
        @input="validatePhoneNumber"
        pattern="[0-9+\s()-]*"
        :class="{ error: phoneNumberError }"
      />
      <p v-if="phoneNumberError" class="error-message">
        {{ phoneNumberError }}
      </p>

      <label for="yearsOfExperience">Years of Experience:</label>
      <input
        type="number"
        id="yearsOfExperience"
        v-model="localData.years_of_experience"
        placeholder="Enter your years of experience"
        @input="updateData"
      />
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
  emits: ["update:personalData"],
  data() {
    return {
      localData: {
        user_type: this.personalData.user_type || "",
        first_name: this.personalData.first_name || "",
        last_name: this.personalData.last_name || "",
        denomination: this.personalData.denomination || "",
        phone_number: this.personalData.phone_number || "",
        years_of_experience: this.personalData.years_of_experience || null,
      },
      firstNameError: "",
      lastNameError: "",
      phoneNumberError: "",
    };
  },
  methods: {
    /* Updates parent with current personal information values */
    updateData() {
      this.$emit("update:personalData", {
        ...this.personalData,
        ...this.localData,
      });
    },
    validateFirstName() {
      const value = this.localData.first_name;
      if (!value) {
        this.firstNameError = "First Name is required";
      } else if (value.length < 2) {
        this.firstNameError = "First Name must be at least 2 characters";
      } else if (value.length > 35) {
        this.firstNameError = "First Name must not exceed 35 characters";
      } else if (!/^[a-zA-Z\s-']+$/.test(value)) {
        this.firstNameError =
          "First Name can only contain letters, spaces, hyphens, and apostrophes";
      } else {
        this.firstNameError = "";
      }
      this.updateData();
    },
    validateLastName() {
      const value = this.localData.last_name;
      if (!value) {
        this.lastNameError = "Last Name is required";
      } else if (value.length < 2) {
        this.lastNameError = "Last Name must be at least 2 characters";
      } else if (value.length > 35) {
        this.lastNameError = "Last Name must not exceed 35 characters";
      } else if (!/^[a-zA-Z\s-']+$/.test(value)) {
        this.lastNameError =
          "Last Name can only contain letters, spaces, hyphens, and apostrophes";
      } else {
        this.lastNameError = "";
      }
      this.updateData();
    },
    validatePhoneNumber() {
      const value = this.localData.phone_number;
      // Remove any non-digit characters for validation
      const digitsOnly = value.replace(/\D/g, "");

      // Remove any non-allowed characters
      this.localData.phone_number = value.replace(/[^0-9+\s()-]/g, "");

      if (!value) {
        this.phoneNumberError = "Phone number is required";
      } else if (digitsOnly.length < 10) {
        this.phoneNumberError = "Phone number must be at least 10 digits";
      } else if (digitsOnly.length > 15) {
        this.phoneNumberError = "Phone number must not exceed 15 digits";
      } else {
        this.phoneNumberError = "";
      }
      this.updateData();
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
          denomination: newValue.denomination || "",
          phone_number: newValue.phone_number || "",
          years_of_experience: newValue.years_of_experience || null,
        };
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.error {
  border-color: #f44336;
}

.error-message {
  color: #f44336;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>
