<template>
  <div class="split-container">
    <!-- Left side with image -->
    <div class="split-left">
      <img
        src="@/assets/pictures/signup.jpg"
        alt="Sign up"
        class="signup-image"
      />
    </div>

    <!-- Right side with registration form -->
    <div class="split-right">
      <div class="registration-card">
        <h1 class="text-[38px] font-bold mt-4 mb-4 text-center">
          Create Your Account
        </h1>

        <!-- Progress Bar Component -->
        <ProgressBar :steps="steps" :currentStep="currentStep" />

        <form>
          <!-- Step 1: Account Information -->
          <AccountInfoStep
            v-show="currentStep === 0"
            v-model:userData="form.user"
            @update:userData="updateUserData"
            @password-validation="handlePasswordValidation"
            @validation-status="handleValidationStatus"
          />

          <!-- Step 2: Personal Information -->
          <PersonalInfoStep
            v-show="currentStep === 1"
            v-model:personalData="form"
            @validation-status="handlePersonalInfoValidation"
          />

          <!-- Step 3: Location Information -->
          <LocationInfoStep
            v-show="currentStep === 2"
            v-model:locationData="form"
            :isAnonymous="form.is_anonymous"
            @validation-status="handleLocationInfoValidation"
          />

          <!-- Step 4: Additional Information -->
          <AdditionalInfoStep
            v-show="currentStep === 3"
            v-model:additionalData="form"
            @validation-status="handleAdditionalInfoValidation"
          />

          <!-- Error Message -->
          <div
            v-if="message"
            :class="[
              'message-container',
              { 'error-message': !isSuccess, 'success-message': isSuccess },
            ]"
          >
            <span class="message-icon">{{ !isSuccess ? "⚠️" : "✅" }}</span>
            {{ message }}
          </div>

          <!-- Navigation Buttons -->
          <NavigationButtons
            :currentStep="currentStep"
            :steps="steps"
            :isStepOneValid="isStepOneValid()"
            :isFormValid="isFormValid"
            :isCurrentStepValid="isCurrentStepValid"
            @prev-step="prevStep"
            @next-step="nextStep"
            @submit="registerUser"
          />
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios.js";
import ProgressBar from "@/components/registration/ProgressBar.vue";
import AccountInfoStep from "@/components/registration/AccountInfoStep.vue";
import PersonalInfoStep from "@/components/registration/PersonalInfoStep.vue";
import LocationInfoStep from "@/components/registration/LocationInfoStep.vue";
import AdditionalInfoStep from "@/components/registration/AdditionalInfoStep.vue";
import NavigationButtons from "@/components/registration/NavigationButtons.vue";

/* global google */

export default {
  components: {
    ProgressBar,
    AccountInfoStep,
    PersonalInfoStep,
    LocationInfoStep,
    AdditionalInfoStep,
    NavigationButtons,
  },
  data() {
    return {
      form: {
        user: {
          username: "",
          email: "",
          password: "",
        },
        tags: [],
        user_type: "",
        first_name: "",
        last_name: "",
        street_address: "",
        city: "",
        state: "",
        country: "",
        other_country: "",
        phone_number: "",
        years_of_experience: null,
        description: "",
        is_anonymous: false,
      },
      passwordsDoNotMatch: false,
      message: "",
      isSuccess: false,
      availableTags: [],
      suggestions: {
        address: [],
        city: [],
        state: [],
      },
      autocompleteService: null,
      placesService: null,
      currentStep: 0,
      steps: [
        { label: "Account" },
        { label: "Personal" },
        { label: "Location" },
        { label: "Additional" },
      ],
      validationStatus: {
        isValid: false,
        errors: {},
      },
      existingUsernames: new Set(),
      existingEmails: new Set(),
      stepValidation: {
        0: false, // Account step
        1: false, // Personal step
        2: false, // Location step
        3: false, // Additional step
      },
    };
  },
  computed: {
    // Ensures that only required fields must be filled
    isFormValid() {
      const username = this.form?.user?.username || "";
      const email = this.form?.user?.email || "";
      const password = this.form?.user?.password || "";

      const isValid =
        username.trim() &&
        email.trim() &&
        password.trim() &&
        !this.passwordsDoNotMatch;
      return isValid;
    },
    isCurrentStepValid() {
      return this.stepValidation[this.currentStep];
    },
  },
  methods: {
    updateUserData(updatedUserData) {
      this.form.user = { ...this.form.user, ...updatedUserData };
    },
    handlePasswordValidation(isValid) {
      this.passwordsDoNotMatch = !isValid;
    },
    handleValidationStatus(status) {
      this.validationStatus = status;
      this.stepValidation[0] = status.isValid;
    },
    handlePersonalInfoValidation(isValid) {
      this.stepValidation[1] = isValid;
    },
    handleLocationInfoValidation(isValid) {
      this.stepValidation[2] = isValid;
    },
    handleAdditionalInfoValidation(isValid) {
      this.stepValidation[3] = isValid;
    },
    async fetchExistingUsers() {
      try {
        const response = await api.get("api/profiles/");
        this.existingUsernames = new Set(
          response.data.map((profile) => profile.user.username.toLowerCase())
        );
        this.existingEmails = new Set(
          response.data.map((profile) => profile.user.email.toLowerCase())
        );
      } catch (error) {
        // Don't show error to user, just log it
      }
    },
    isStepOneValid() {
      const username = this.form?.user?.username || "";
      const email = this.form?.user?.email || "";
      const password = this.form?.user?.password || "";

      const isValid =
        username.trim() &&
        email.trim() &&
        password.trim() &&
        !this.passwordsDoNotMatch &&
        this.validationStatus.isValid;

      if (!isValid) {
        this.isSuccess = false;
      }

      return isValid;
    },
    // Navigation methods
    async nextStep() {
      if (this.currentStep === 0) {
        if (!this.isStepOneValid()) {
          return;
        }

        try {
          // Clear any existing messages
          this.message = "";
          this.isSuccess = false;

          // If we don't have the existing users data yet, try to fetch it
          if (
            this.existingUsernames.size === 0 ||
            this.existingEmails.size === 0
          ) {
            try {
              await this.fetchExistingUsers();
            } catch (error) {
              // Continue anyway, we'll handle missing data gracefully
            }
          }

          // Check if username exists (case-insensitive comparison)
          if (
            this.existingUsernames.has(this.form.user.username.toLowerCase())
          ) {
            this.message =
              "This username is already taken. Please choose another one.";
            this.isSuccess = false;
            return;
          }

          // Check if email exists (case-insensitive comparison)
          if (this.existingEmails.has(this.form.user.email.toLowerCase())) {
            this.message =
              "This email is already registered. Please use a different email address.";
            this.isSuccess = false;
            return;
          }

          // Username and email are available, proceed to next step
          this.message = "";
          this.currentStep++;
        } catch (error) {
          if (error.code === "ECONNABORTED") {
            this.message =
              "Connection timed out. Please check your connection and try again.";
          } else {
            this.message =
              "Error checking username and email availability. Please try again.";
          }

          this.isSuccess = false;
          return;
        }
      } else if (this.currentStep < this.steps.length - 1) {
        this.message = ""; // Clear message when moving to next step
        this.currentStep++;
      }
    },
    prevStep() {
      if (this.currentStep > 0) {
        this.message = ""; // Clear message when moving to previous step
        this.currentStep--;
      }
    },
    goToStep(step) {
      // Only allow going to completed steps or the next available step
      if (step <= this.currentStep + 1) {
        this.currentStep = step;
      }
    },

    // Fetches predefined tags from the backend
    async fetchTags() {
      try {
        const response = await api.get("tag/");
        this.availableTags = response.data.filter(
          (tag) => tag.tag_is_predefined
        );
      } catch (error) {
        // Don't show error to user, just log it
      }
    },

    // Calls the profiles endpoint to register the user
    async registerUser() {
      try {
        // Create the data in the nested format expected by the backend
        const formData = {
          user: {
            username: this.form.user.username,
            email: this.form.user.email,
            password: this.form.user.password,
          },
          tags: this.form.tags,
          user_type: this.form.user_type
            ? this.form.user_type.toLowerCase()
            : null,
          first_name: this.form.first_name || null,
          last_name: this.form.last_name || null,
          street_address: this.form.street_address || null,
          city: this.form.city || null,
          state: this.form.state || null,
          country:
            this.form.country === "Other"
              ? this.form.other_country
              : this.form.country || null,
          phone_number: this.form.phone_number || null,
          years_of_experience: this.form.years_of_experience || null,
          description: this.form.description || null,
          profile_picture: null,
        };

        await api.post("api/profiles/", formData);

        this.message = "Registration successful!";
        this.isSuccess = true;
        setTimeout(() => this.$router.push("/AppLogin"), 1000);
      } catch (error) {
        if (error.code === "ECONNABORTED") {
          this.message =
            "Registration timed out. Please check your connection and try again.";
        } else if (error.response) {
          this.message =
            error.response?.data?.detail ||
            error.response?.data?.user?.username?.[0] ||
            error.response?.data?.user?.email?.[0] ||
            "Registration failed. Please try again.";
        } else {
          this.message =
            "Registration failed. Please check your connection and try again.";
        }

        this.isSuccess = false;
      }
    },

    // Google Places API for Address Autocomplete
    initGooglePlaces() {
      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyCzHCbngGLUj41VG6hmwFsAoUak7QwnX3k&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => {
        if (google && google.maps && google.maps.places) {
          this.autocompleteService =
            new google.maps.places.AutocompleteService();
          this.placesService = new google.maps.places.PlacesService(
            document.createElement("div")
          );
        } else {
          null;
        }

        // Add input event listeners
        ["streetAddress", "city", "state"].forEach((field) => {
          this.$refs[`${field}Input`]?.addEventListener("input", (e) =>
            this.handleInput(e, field)
          );
        });
      };
      document.head.appendChild(script);
    },

    async handleInput(event, field) {
      const input = event.target.value;
      if (input.length < 2) {
        this.suggestions[field] = [];
        return;
      }

      try {
        const types = {
          streetAddress: ["address"],
          city: ["(cities)"],
          state: ["administrative_area_level_1"],
        };

        const response = await this.autocompleteService.getPlacePredictions({
          input,
          types: types[field],
        });
        this.suggestions[field] = response.predictions;
      } catch (error) {
        this.suggestions[field] = [];
      }
    },

    selectAddress(place) {
      this.suggestions.address = [];
      this.form.street_address = place.description;

      this.placesService.getDetails(
        {
          placeId: place.place_id,
          fields: ["address_components"],
        },
        (result, status) => {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
            result.address_components.forEach((component) => {
              const type = component.types[0];
              if (type === "locality") this.form.city = component.long_name;
              if (type === "administrative_area_level_1")
                this.form.state = component.long_name;
            });
          }
        }
      );
    },

    selectCity(suggestion) {
      this.suggestions.city = [];
      this.form.city = suggestion.description;
    },

    selectState(suggestion) {
      this.suggestions.state = [];
      this.form.state = suggestion.description;
    },
  },
  // Fetches all the predefined tags on page load
  mounted() {
    this.fetchTags();
    this.initGooglePlaces();
    this.fetchExistingUsers();
  },
  watch: {
    form: {
      handler() {
        null;
      },
      deep: true,
    },
  },
  beforeUnmount() {
    // Clean up event listeners
    ["streetAddress", "city", "state"].forEach((field) => {
      this.$refs[`${field}Input`]?.removeEventListener("input", (e) =>
        this.handleInput(e, field)
      );
    });
  },
};
</script>

<style scoped>
.split-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.split-left {
  flex: 1;
  overflow: hidden;
}

.signup-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.split-right {
  flex: 1;
  background: #ffffff;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 2rem;
  padding-top: 1.5rem;
  overflow-y: auto;
}

.registration-card {
  width: 100%;
  max-width: 800px;
  background: white;
  padding: 2rem;
  padding-top: 1rem;
}

.registration-card h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 2rem;
  text-align: left;
  font-weight: 600;
}

.message-container {
  margin: 15px 0;
  padding: 15px;
  font-weight: 500;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 10px;
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

.message-icon {
  font-size: 1.2rem;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  border-left: 4px solid #f44336;
}

.success-message {
  background-color: #e8f5e9;
  color: #2e7d32;
  border-left: 4px solid #4caf50;
}

@media (max-width: 1024px) {
  .split-container {
    flex-direction: column;
  }

  .split-left {
    height: 200px;
  }

  .split-right {
    padding: 1rem;
  }

  .registration-card {
    padding: 1rem;
  }

  .registration-card h1 {
    font-size: 2rem;
  }
}
</style>
