<template>
  <div id="app">
    <AppNav />
    <HeaderComponent />
    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view />
      </div>
    </div>
    <!--<FooterComponent />-->
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
