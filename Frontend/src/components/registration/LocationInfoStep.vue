<template>
  <div class="form-step">
    <h2 class="step-title">Location Information</h2>
    <div class="form-group">
      <div class="address-section">
        <label for="streetAddress">Street Address:</label>
        <input
          type="text"
          id="streetAddress"
          v-model="localData.street_address"
          ref="streetAddressInput"
          placeholder="Enter your street address"
          @input="updateData"
        />
        <div v-if="suggestions.address.length > 0" class="suggestions-list">
          <div
            v-for="(suggestion, index) in suggestions.address"
            :key="index"
            class="suggestion-item"
            @click="selectAddress(suggestion)"
          >
            {{ suggestion.description }}
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-col">
          <label for="city">City:</label>
          <input
            type="text"
            id="city"
            v-model="localData.city"
            ref="cityInput"
            placeholder="Enter your city"
            @input="updateData"
          />
          <div v-if="suggestions.city.length > 0" class="suggestions-list">
            <div
              v-for="(suggestion, index) in suggestions.city"
              :key="index"
              class="suggestion-item"
              @click="selectCity(suggestion)"
            >
              {{ suggestion.description }}
            </div>
          </div>
        </div>

        <div class="form-col">
          <label for="state">State:</label>
          <input
            type="text"
            id="state"
            v-model="localData.state"
            ref="stateInput"
            placeholder="Enter your state"
            @input="updateData"
          />
          <div v-if="suggestions.state.length > 0" class="suggestions-list">
            <div
              v-for="(suggestion, index) in suggestions.state"
              :key="index"
              class="suggestion-item"
              @click="selectState(suggestion)"
            >
              {{ suggestion.description }}
            </div>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label for="country">
          <span class="required">*</span> Country:
          <span class="required-text">required</span>
        </label>
        <select
          id="country"
          v-model="localData.country"
          class="country-select"
          required
          @change="updateData"
        >
          <option value="">Select your country</option>
          <option value="United States">United States</option>
          <option value="Canada">Canada</option>
          <option value="United Kingdom">United Kingdom</option>
          <option value="Australia">Australia</option>
          <option value="Philippines">Philippines</option>
          <option value="India">India</option>
          <option value="Nigeria">Nigeria</option>
          <option value="Kenya">Kenya</option>
          <option value="South Africa">South Africa</option>
          <option value="Other">Other (specify below)</option>
        </select>
        <div v-if="localData.country === 'Other'" class="other-country-input">
          <input
            type="text"
            v-model="localData.other_country"
            placeholder="Enter your country"
            class="mt-2"
            required
            @input="updateData"
          />
        </div>
        <p v-if="countryError" class="error-message">
          {{ countryError }}
        </p>
      </div>

      <!-- Location Visibility Warning -->
      <div class="location-warning">
        <span class="warning-icon">⚠️</span>
        <p>
          Your location information will be visible to other users. This helps
          with matchmaking and community features.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
/* global google */

export default {
  name: "LocationInfoStep",
  props: {
    locationData: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:locationData", "validation"],
  data() {
    return {
      localData: {
        street_address: this.locationData.street_address || "",
        city: this.locationData.city || "",
        state: this.locationData.state || "",
        country: this.locationData.country || "",
        other_country: this.locationData.other_country || "",
      },
      suggestions: {
        address: [],
        city: [],
        state: [],
      },
      autocompleteService: null,
      placesService: null,
      countryError: "",
    };
  },
  computed: {
    isCountryValid() {
      if (this.localData.country === "Other") {
        return this.localData.other_country.trim() !== "";
      }
      return this.localData.country.trim() !== "";
    },
  },
  mounted() {
    this.initGooglePlaces();
  },
  beforeUnmount() {
    // Clean up event listeners
    ["streetAddress", "city", "state"].forEach((field) => {
      this.$refs[`${field}Input`]?.removeEventListener("input", (e) =>
        this.handleInput(e, field)
      );
    });
  },
  methods: {
    /* Updates parent with current location data values */
    updateData() {
      this.validateCountry();
      this.$emit("update:locationData", {
        ...this.locationData,
        ...this.localData,
      });
      this.$emit("validation", {
        isValid: this.isCountryValid,
        error: this.countryError,
      });
    },

    validateCountry() {
      if (!this.localData.country) {
        this.countryError = "Please select your country";
      } else if (
        this.localData.country === "Other" &&
        !this.localData.other_country.trim()
      ) {
        this.countryError = "Please specify your country";
      } else {
        this.countryError = "";
      }
    },

    /* Initializes Google Places API for address autocomplete */
    initGooglePlaces() {
      if (window.google && window.google.maps && window.google.maps.places) {
        this.setupGooglePlacesServices();
      } else {
        const script = document.createElement("script");
        script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyCzHCbngGLUj41VG6hmwFsAoUak7QwnX3k&libraries=places`;
        script.async = true;
        script.defer = true;
        script.onload = () => {
          this.setupGooglePlacesServices();
        };
        document.head.appendChild(script);
      }
    },

    /* Sets up Google Places services and input event listeners */
    setupGooglePlacesServices() {
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
    },

    /* Fetches and displays autocomplete suggestions based on user input */
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

    /* Updates address field and extracts city and state from selection */
    selectAddress(place) {
      this.suggestions.address = [];
      this.localData.street_address = place.description;
      this.updateData();

      this.placesService.getDetails(
        {
          placeId: place.place_id,
          fields: ["address_components"],
        },
        (result, status) => {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
            result.address_components.forEach((component) => {
              const type = component.types[0];
              if (type === "locality") {
                this.localData.city = component.long_name;
              }
              if (type === "administrative_area_level_1") {
                this.localData.state = component.long_name;
              }
            });
            this.updateData();
          }
        }
      );
    },

    /* Updates city field with selected suggestion */
    selectCity(suggestion) {
      this.suggestions.city = [];
      this.localData.city = suggestion.description;
      this.updateData();
    },

    /* Updates state field with selected suggestion */
    selectState(suggestion) {
      this.suggestions.state = [];
      this.localData.state = suggestion.description;
      this.updateData();
    },
  },
  watch: {
    locationData: {
      handler(newValue) {
        this.localData = {
          street_address: newValue.street_address || "",
          city: newValue.city || "",
          state: newValue.state || "",
          country: newValue.country || "",
          other_country: newValue.other_country || "",
        };
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.location-warning {
  margin-top: 20px;
  padding: 15px;
  background-color: #fff3e0;
  border-left: 4px solid #ff9800;
  border-radius: 4px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.warning-icon {
  font-size: 1.2rem;
}

.location-warning p {
  margin: 0;
  color: #e65100;
  font-size: 0.9rem;
  line-height: 1.4;
}

.error-message {
  color: #d32f2f;
  font-size: 0.875rem;
  margin-top: 4px;
}

.required {
  color: #d32f2f;
  margin-right: 4px;
}

.required-text {
  color: #666;
  font-size: 0.875rem;
  margin-left: 4px;
}

.country-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 4px;
}

.other-country-input {
  margin-top: 8px;
}

.other-country-input input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
