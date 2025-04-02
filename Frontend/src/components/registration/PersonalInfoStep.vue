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
            @input="updateData"
          />
        </div>
      </div>

      <label for="phoneNumber">Phone Number:</label>
      <input
        type="text"
        id="phoneNumber"
        v-model="localData.phone_number"
        placeholder="Enter your phone number"
        @input="updateData"
      />

      <label for="yearsOfExperience"
        >Years of Experience:
        <span class="required-text"
          >If you have no years of experience please leave blank</span
        ></label
      >
      <input
        type="number"
        id="yearsOfExperience"
        v-model="localData.years_of_experience"
        min="0"
        max="100"
        placeholder="Enter your years of experience"
        @input="validateYearsOfExperience"
        @keypress="validateDigits"
      />
      <p v-if="yearsError" class="error-message">
        {{ yearsError }}
      </p>
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
        phone_number: this.personalData.phone_number || "",
        years_of_experience: this.personalData.years_of_experience || null,
      },
      yearsError: "",
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
        this.localData.years_of_experience = null;
        this.updateData();
        return;
      }

      const numYears = Number(years);
      if (isNaN(numYears) || numYears < 0) {
        this.yearsError = "Please enter a valid number";
        this.localData.years_of_experience = null;
      } else if (numYears > 100) {
        this.yearsError = "Experience cannot exceed 100 years";
        this.localData.years_of_experience = null;
      } else if (!Number.isInteger(numYears)) {
        this.yearsError = "Please enter a whole number";
        this.localData.years_of_experience = null;
      } else {
        this.yearsError = "";
      }
      this.updateData();
    },
    /* Updates parent with current personal information values */
    updateData() {
      this.$emit("update:personalData", {
        ...this.personalData,
        ...this.localData,
      });
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
        };
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.error-message {
  color: #d32f2f;
  font-size: 0.875rem;
  margin-top: 4px;
}
</style>
