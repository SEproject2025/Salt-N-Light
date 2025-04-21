<template>
  <div class="progress-container">
    <div class="step-indicators">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="step-indicator"
        :class="{
          active: currentStep >= index,
          completed: currentStep > index,
        }"
      >
        <div class="step-number">{{ index + 1 }}</div>
        <div class="step-label">{{ step.label }}</div>
      </div>
    </div>
    <div class="progress-bar-container">
      <div
        class="progress-bar"
        :style="{ width: progressPercentage + '%' }"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProgressBar",
  props: {
    steps: {
      type: Array,
      required: true,
    },
    currentStep: {
      type: Number,
      required: true,
    },
  },
  computed: {
    /* Calculates progress percentage (0-100) based on current step */
    progressPercentage() {
      return (this.currentStep / (this.steps.length - 1)) * 100;
    },
  },
};
</script>

<style scoped>
.progress-container {
  width: 100%;
  position: relative;
  margin-bottom: 30px;
}

.progress-bar-container {
  position: absolute;
  top: 15px;
  left: 0;
  right: 0;
  height: 4px;
  background-color: white;
  z-index: 0;
}

.progress-bar {
  height: 4px;
  background-color: #4caf50;
  position: absolute;
  top: 0;
  left: 0;
  transition: width 0.3s ease;
}

.step-indicators {
  display: flex;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: default;
  background-color: white;
  padding: 0 5px;
}

.step-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 5px;
  font-weight: 500;
  border: 2px solid white;
}

.step-indicator.active .step-number {
  background-color: #4caf50;
  color: white;
}

.step-indicator.completed .step-number {
  background-color: #4caf50;
  color: white;
}

.step-label {
  font-size: 0.8rem;
  color: #666;
  text-align: center;
}
</style>
