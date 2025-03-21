<template>
  <div class="registration-container">
    <div class="registration-card">
      <h1>Create Your Account</h1>

      <!-- Progress Bar Component -->
      <ProgressBar
        :steps="steps"
        :currentStep="currentStep"
        @go-to-step="goToStep"
      />

      <form>
        <!-- Step 1: Account Information -->
        <AccountInfoStep
          v-show="currentStep === 0"
          v-model:userData="form.user"
          @password-validation="handlePasswordValidation"
        />

        <!-- Step 2: Personal Information -->
        <PersonalInfoStep
          v-show="currentStep === 1"
          v-model:personalData="form"
        />

        <!-- Step 3: Location Information -->
        <LocationInfoStep
          v-show="currentStep === 2"
          v-model:locationData="form"
        />

        <!-- Step 4: Additional Information -->
        <AdditionalInfoStep
          v-show="currentStep === 3"
          v-model:additionalData="form"
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
          @prev-step="prevStep"
          @next-step="nextStep"
          @submit="registerUser"
        />
      </form>
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
        tags_ids: [],
        user_type: "",
        first_name: "",
        last_name: "",
        denomination: "",
        street_address: "",
        city: "",
        state: "",
        country: "",
        other_country: "",
        phone_number: "",
        years_of_experience: null,
        description: "",
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
    };
  },
  computed: {
    // Ensures that only required fields must be filled
    isFormValid() {
      const { username, email, password } = this.form.user;
      const isValid =
        username.trim() &&
        email.trim() &&
        password.trim() &&
        !this.passwordsDoNotMatch;
      console.log("isFormValid computed property:", {
        username: username.trim(),
        email: email.trim(),
        password: password.trim(),
        passwordsDoNotMatch: this.passwordsDoNotMatch,
        isValid,
      });
      return isValid;
    },
  },
  methods: {
    // Navigation methods
    async nextStep() {
      if (this.currentStep === 0) {
        // Check uniqueness before proceeding from step 1
        if (!this.isStepOneValid()) {
          return;
        }

        try {
          // Clear any existing messages
          this.message = "";
          this.isSuccess = false;

          // Fetch all profiles
          const response = await api.get("api/profiles/");
          const existingUsernames = response.data.map((profile) =>
            profile.user.username.toLowerCase()
          );

          // Check if username exists (case-insensitive comparison)
          if (
            existingUsernames.includes(this.form.user.username.toLowerCase())
          ) {
            this.message =
              "This username is already taken. Please choose another one.";
            this.isSuccess = false;
            return;
          }

          // Username is available, proceed to next step
          this.message = "";
          this.currentStep++;
        } catch (error) {
          console.error("Username check error:", error);
          this.message =
            "Error checking username availability. Please try again.";
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
    isStepOneValid() {
      const { username, email, password } = this.form.user;
      const isValid =
        username.trim() &&
        email.trim() &&
        password.trim() &&
        !this.passwordsDoNotMatch;

      if (!isValid) {
        this.message = "Please complete all required fields before proceeding.";
        this.isSuccess = false;
      }

      return isValid;
    },

    // Fetches predefined tags from the backend
    async fetchTags() {
      try {
        const response = await api.get("tag/");
        this.availableTags = response.data.filter(
          (tag) => tag.tag_is_predefined
        );
      } catch (error) {
        console.error("Failed to fetch tags:", error.response?.data);
      }
    },

    // Handle password validation from child component
    handlePasswordValidation(isValid) {
      this.passwordsDoNotMatch = !isValid;
    },

    // Calls the profiles endpoint to register the user
    async registerUser() {
      console.log("registerUser method called");
      console.log("Current form data:", this.form);

      try {
        // Create the data in the nested format expected by the backend
        const formData = {
          user: {
            username: this.form.user.username,
            email: this.form.user.email,
            password: this.form.user.password,
          },
          tags_ids: this.form.tags_ids,
          user_type: this.form.user_type
            ? this.form.user_type.toLowerCase()
            : null,
          first_name: this.form.first_name,
          last_name: this.form.last_name,
          denomination: this.form.denomination,
          street_address: this.form.street_address,
          city: this.form.city,
          state: this.form.state,
          country:
            this.form.country === "Other"
              ? this.form.other_country
              : this.form.country,
          phone_number: this.form.phone_number,
          years_of_experience: this.form.years_of_experience,
          description: this.form.description,
          profile_picture: null, // Always send null for profile picture
        };

        // Log the data being sent
        console.log("Registration data being sent:", formData);

        const response = await api.post("api/profiles/", formData);
        console.log("Registration response:", response.data);

        this.message = "Registration successful!";
        this.isSuccess = true;
        setTimeout(() => this.$router.push("/AppLogin"), 1000);
      } catch (error) {
        console.error("Registration failed:", error.response?.data);
        console.error("Error status:", error.response?.status);
        console.error("Error details:", error);
        this.message =
          error.response?.data?.detail ||
          error.response?.data?.user?.username?.[0] ||
          error.response?.data?.user?.email?.[0] ||
          "Registration failed. Please try again.";
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
        this.autocompleteService = new google.maps.places.AutocompleteService();
        this.placesService = new google.maps.places.PlacesService(
          document.createElement("div")
        );

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
        console.error(`Error fetching ${field} suggestions:`, error);
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
    console.log("RegistrationPage component mounted");
  },
  watch: {
    form: {
      handler(newVal) {
        console.log("Form data updated:", newVal);
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
@import "../components/registration/styles.css";

.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  background: #f4f7fc;
  padding: 20px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.registration-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  text-align: center;
}

h1 {
  margin-bottom: 30px;
  color: #333;
  font-weight: 600;
  font-size: 2rem;
}

@media (max-width: 768px) {
  .registration-card {
    padding: 25px;
  }
}

.message-container {
  margin: 15px 0;
  padding: 15px;
  border-radius: 8px;
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
</style>
