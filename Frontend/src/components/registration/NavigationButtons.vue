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
