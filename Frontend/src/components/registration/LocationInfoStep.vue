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
        <div v-if="localData.country === 'Other'" class="other-country-input">
          <input
            type="text"
            v-model="localData.other_country"
            placeholder="Enter your country"
            required
            @input="updateData"
          />
        </div>
        <div v-if="countryError" class="error-message">{{ countryError }}</div>
      </div>

      <div v-if="!isAnonymous" class="location-warning">
        <p>
          <strong>Note:</strong> Your location information will be visible to
          other users to help facilitate connections and support. If you prefer
          to keep your location private, you can make your profile anonymous in
          the previous step.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LocationInfoStep",
  props: {
    locationData: {
      type: Object,
      required: true,
    },
    isAnonymous: {
      type: Boolean,
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
        country: [],
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

    handleCountryChange() {
      if (this.localData.country !== "Other") {
        this.localData.other_country = "";
      }
      this.updateData();
    },

    /* Handles address selection from suggestions */
    selectAddress(place) {
      this.suggestions.address = [];
      this.localData.street_address = place.description;
      this.updateData();
    },

    /* Handles city selection from suggestions */
    selectCity(suggestion) {
      this.suggestions.city = [];
      this.localData.city = suggestion.description;
      this.updateData();
    },

    /* Handles state selection from suggestions */
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
    isAnonymous: {
      handler(newValue) {
        // Clear location warning when anonymous status changes
        if (newValue) {
          this.suggestions = {
            address: [],
            city: [],
            state: [],
            country: [],
          };
        }
      },
      immediate: true,
    },
  },
};
</script>

<style scoped>
.location-warning {
  margin-top: 2px;
  padding: 2px;
  background-color: #fff3e0;
  border-radius: 4px;
  display: flex;
  align-items: center;
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
  background-color: white;
  cursor: pointer;
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

.suggestions-list {
  position: absolute;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  z-index: 1000;
  margin-top: 4px;
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.suggestion-item:hover {
  background-color: #f5f5f5;
}

.suggestion-item:last-child {
  border-bottom: none;
}
</style>
