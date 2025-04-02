<template>
  <div class="form-step">
    <h2 class="step-title">Account Information</h2>
    <div class="form-group">
      <!-- Username Field -->
      <label for="username">
        <span class="required">*</span> Username:
        <span class="required-text">required</span>
      </label>
      <input
        type="text"
        id="username"
        v-model="localUserData.username"
        placeholder="Choose a unique username"
        :class="{ error: usernameError }"
      />
      <p v-if="usernameError" class="error-message">{{ usernameError }}</p>

      <!-- Email Field -->
      <label for="email">
        <span class="required">*</span> Email:
        <span class="required-text">required</span>
      </label>
      <input
        type="email"
        id="email"
        v-model="localUserData.email"
        placeholder="Enter your email address"
        :class="{ error: emailError }"
      />
      <p v-if="emailError" class="error-message">{{ emailError }}</p>

      <!-- Password Field -->
      <label for="password">
        <span class="required">*</span> Password:
        <span class="required-text">required</span>
      </label>
      <input
        type="password"
        id="password"
        v-model="localUserData.password"
        placeholder="Create a secure password"
        :class="{ error: passwordError }"
      />
      <p v-if="passwordError" class="error-message">{{ passwordError }}</p>

      <!-- Confirm Password Field -->
      <label for="confirmPassword">
        <span class="required">*</span> Confirm Password:
        <span class="required-text">required</span>
      </label>
      <input
        type="password"
        id="confirmPassword"
        v-model="confirmPassword"
        placeholder="Confirm your password"
        :class="{ error: confirmPasswordError }"
      />
      <p v-if="confirmPasswordError" class="error-message">
        {{ confirmPasswordError }}
      </p>

      <!-- Add note about required fields -->
      <div class="info-message">
        <span class="info-icon">ℹ️</span>
        These account details are required. The following steps are optional but
        help complete your profile.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AccountInfoStep",
  props: {
    userData: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:userData", "password-validation"],
  data() {
    return {
      localUserData: {
        username: this.userData.username || "",
        email: this.userData.email || "",
        password: this.userData.password || "",
      },
      confirmPassword: "",
      usernameError: "",
      emailError: "",
      passwordError: "",
      confirmPasswordError: "",
    };
  },
  watch: {
    "localUserData.username": {
      handler(newVal) {
        this.validateUsername(newVal);
        this.$emit("update:userData", { ...this.userData, username: newVal });
        this.validateForm();
      },
    },
    "localUserData.email": {
      handler(newVal) {
        this.validateEmail(newVal);
        this.$emit("update:userData", { ...this.userData, email: newVal });
        this.validateForm();
      },
    },
    "localUserData.password": {
      handler(newVal) {
        this.validatePassword(newVal);
        this.$emit("update:userData", { ...this.userData, password: newVal });
        this.validateForm();
      },
    },
    confirmPassword: {
      handler(newVal) {
        this.validateConfirmPassword(newVal);
        this.validateForm();
      },
    },
    userData: {
      handler(newVal) {
        this.localUserData = {
          username: newVal.username || "",
          email: newVal.email || "",
          password: newVal.password || "",
        };
      },
      deep: true,
    },
  },
  methods: {
    validateUsername(value) {
      if (!value) {
        this.usernameError = "Username is required";
      } else if (value.length < 3) {
        this.usernameError = "Username must be at least 3 characters";
      } else if (value.length > 25) {
        this.usernameError = "Username must not exceed 25 characters";
      } else {
        this.usernameError = "";
      }
    },
    validateEmail(value) {
      if (!value) {
        this.emailError = "Email is required";
      } else {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const ipEmailRegex = /^[^\s@]+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;

        if (!emailRegex.test(value) && !ipEmailRegex.test(value)) {
          this.emailError = "Please enter a valid email address";
        } else if (ipEmailRegex.test(value)) {
          const ipPart = value.split("@")[1];
          const ipNumbers = ipPart.split(".").map(Number);
          if (ipNumbers.some((num) => num > 255)) {
            this.emailError = "Invalid IP address format";
          } else {
            this.emailError = "";
          }
        } else {
          this.emailError = "";
        }
      }
    },
    validatePassword(value) {
      if (!value) {
        this.passwordError =
          "Password must contain at least a number, a letter and a special character and be at least 6 characters long";
      } else if (value.length < 6) {
        this.passwordError = "Password must be at least 6 characters";
      } else if (value.length > 25) {
        this.passwordError = "Password must not exceed 25 characters";
      } else {
        // Check for at least one number
        const hasNumber = /\d/.test(value);
        // Check for at least one letter
        const hasLetter = /[a-zA-Z]/.test(value);
        // Check for at least one special character
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(value);

        if (!hasNumber) {
          this.passwordError = "Password must contain at least one number";
        } else if (!hasLetter) {
          this.passwordError = "Password must contain at least one letter";
        } else if (!hasSpecial) {
          this.passwordError =
            'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)';
        } else {
          this.passwordError = "";
        }
      }
    },
    validateConfirmPassword(value) {
      if (!value) {
        this.confirmPasswordError = "Please confirm your password";
      } else if (value !== this.localUserData.password) {
        this.confirmPasswordError = "Passwords do not match";
      } else {
        this.confirmPasswordError = "";
      }
    },
    validateForm() {
      const isValid =
        !this.usernameError &&
        !this.emailError &&
        !this.passwordError &&
        !this.confirmPasswordError;

      this.$emit("password-validation", isValid);
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
