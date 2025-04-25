<template>
  <div id="app" class="min-h-screen flex flex-col">
    <HeaderComponent />
    <main class="flex-grow">
      <router-view :key="$route.fullPath" />
    </main>
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
