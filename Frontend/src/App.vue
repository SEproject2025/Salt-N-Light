<template>
  <div id="app">
    <AppNav />
    <HeaderComponent />
    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view :key="$route.fullPath" />
      </div>
    </div>
    <FooterComponent />
  </div>
</template>

<script>
import HeaderComponent from "@/components/common/HeaderComponent.vue";
import FooterComponent from "@/components/common/FooterComponent.vue";

export default {
  name: "App",
  components: {
    HeaderComponent,
    FooterComponent,
  },
};
</script>
