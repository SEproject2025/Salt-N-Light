<template>
  <div id="app">
    <AppNav />
    <HeaderComponent />
    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view :key="$route.fullPath" />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "@/components/common/HeaderComponent.vue";

export default {
  name: "App",
  components: {
    HeaderComponent,
  },
};
</script>
