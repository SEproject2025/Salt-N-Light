<template>
  <div class="form-navigation">
    <button
      v-if="currentStep > 0"
      type="button"
      class="btn-secondary"
      @click="$emit('prev-step')"
    >
      Previous
    </button>

    <button
      v-if="currentStep < steps.length - 1"
      type="button"
      class="btn-primary"
      :disabled="!isCurrentStepValid"
      @click="$emit('next-step')"
    >
      Next
    </button>
    <button
      v-if="currentStep === steps.length - 1"
      type="button"
      class="btn-submit"
      :disabled="!isFormValid"
      @click="handleSubmit"
    >
      Create Account
    </button>
  </div>
</template>

<script>
export default {
  name: "NavigationButtons",
  props: {
    currentStep: {
      type: Number,
      required: true,
    },
    steps: {
      type: Array,
      required: true,
    },
    isStepOneValid: {
      type: Boolean,
      required: true,
    },
    isFormValid: {
      type: Boolean,
      required: true,
    },
    isCurrentStepValid: {
      type: Boolean,
      required: true,
    },
  },
  emits: ["prev-step", "next-step", "skip-to-final", "submit"],
  methods: {
    handleSubmit() {
      if (this.isFormValid) {
        this.$emit("submit");
      }
    },
  },
};
</script>
<style scoped>
.btn-primary {
  background-color: #007bff;
  color: white;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  opacity: 1; /* 🔐 Always visible */
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #007bff;
}

.btn-primary:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.btn-secondary {
  width: 80px;
  height: 40px;
  padding: 0;
  background-color: #e0e0e0;
  color: #333;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  text-align: center;
}

.btn-secondary:hover {
  background-color: #d5d5d5;
}

.btn-submit {
  background-color: #007bff;
  color: white;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  opacity: 1;
  transition: background-color 0.3s;
}

.btn-submit:hover {
  background-color: #007bff;
}

.btn-submit:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
