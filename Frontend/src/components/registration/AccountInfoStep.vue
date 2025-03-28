<template>
  <div class="form-step">
    <h2 class="step-title">Account Information</h2>
    <form @submit.prevent="handleSubmit" class="form-group">
      <!-- Username Field -->
      <label for="username">
        <span class="required">*</span> Username:
        <span class="required-text">required</span>
      </label>
      <Field
        type="text"
        id="username"
        name="username"
        rules="required|min:3|max:25"
        v-model="localUserData.username"
        placeholder="Choose a unique username"
      />
      <!--<p v-if="usernameError" class="error-message">
        {{ usernameError }}
      </p>-->
      <ErrorMessage name="username" class="error-message" />

      <!-- Email Field -->
      <label for="email">
        <span class="required">*</span> Email:
        <span class="required-text">required</span>
      </label>
      <Field
        type="email"
        id="email"
        name="email"
        rules="required|email"
        v-model="localUserData.email"
        placeholder="Enter your email address"
      />
      <!--<p v-if="emailError" class="error-message">
        {{ emailError }}
      </p>-->
      <ErrorMessage name="email" class="error-message" />

      <!-- Password Field -->
      <label for="password">
        <span class="required">*</span> Password:
        <span class="required-text">required</span>
      </label>
      <Field
        type="password"
        id="password"
        name="password"
        rules="required|min:6|max:25"
        v-model="localUserData.password"
        placeholder="Create a secure password"
      />
      <ErrorMessage name="password" class="error-message" />

      <!-- Confirm Password Field -->
      <label for="confirmPassword">
        <span class="required">*</span> Confirm Password:
        <span class="required-text">required</span>
      </label>
      <Field
        type="password"
        id="confirmPassword"
        name="confirmPassword"
        v-model="confirmPassword"
        rules="required|same:password"
        placeholder="Confirm your password"
      />
      <!--<p v-if="passwordsDoNotMatch" class="error-message">
        Passwords do not match.
      </p>-->
      <ErrorMessage name="confirmPassword" class="error-message" />

      <!-- Add note about required fields -->
      <div class="info-message">
        <span class="info-icon">ℹ️</span>
        These account details are required. The following steps are optional but
        help complete your profile.
      </div>

      <!-- Submit Button -->
      <div class="form-navigation">
        <button type="submit" class="btn btn-primary">Next</button>
      </div>
    </form>
  </div>
</template>

<script>
import { defineRule, configure, Field, ErrorMessage } from "vee-validate";
import { required, min, max, email } from "@vee-validate/rules";

// Define validation rules
defineRule("required", required);
defineRule("min", min);
defineRule("max", max);
defineRule("email", email);

// Define a custom 'same' rule
defineRule("same", (value, [target], ctx) => {
  if (value === ctx.form[target]) {
    return true;
  }
  return `${ctx.field} must match ${target}`;
});

// Configure VeeValidate
configure({
  generateMessage: (ctx) => {
    const messages = {
      required: `${ctx.field} is required.`,
      min: `${ctx.field} must be at least ${ctx.rule.params[0]} characters.`,
      max: `${ctx.field} must not exceed ${ctx.rule.params[0]} characters.`,
      email: `Please enter a valid email address.`,
    };
    return messages[ctx.rule.name] || `The ${ctx.field} field is invalid.`;
  },
});

export default {
  name: "AccountInfoStep",
  components: {
    Field,
    ErrorMessage,
  },
  props: {
    userData: {
      type: Object,
      required: true,
    },
  },
  emits: ["update:userData", "next"],
  data() {
    return {
      localUserData: {
        username: this.userData.username || "",
        email: this.userData.email || "",
        password: this.userData.password || "",
      },
      confirmPassword: "",
      //passwordsDoNotMatch: false,
      //usernameError: "",
      //emailError: "",
    };
  },
  methods: {
    async handleSubmit() {
      try {
        // Update parent component with form data
        this.$emit("update:userData", { ...this.localUserData });

        // Emit next event to move to next step
        this.$emit("next");
      } catch (error) {
        console.error("Error submitting form:", error);
      }
    },
  },
  watch: {
    userData: {
      handler(newValue) {
        this.localUserData = { ...newValue };
      },
      deep: true,
    },
  },
  mounted() {
    console.log("AccountInfoStep mounted", this.userData);
  },
};
</script>

<style scoped>
.form-step {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.form-navigation {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.info-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #666;
}

.required {
  color: #dc3545;
  margin-right: 0.25rem;
}

.required-text {
  font-size: 0.8rem;
  color: #666;
  margin-left: 0.5rem;
}
</style>
