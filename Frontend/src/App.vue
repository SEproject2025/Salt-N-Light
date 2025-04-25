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
import { ref, provide } from "vue";

export default {
  name: "App",
  components: {
    HeaderComponent,
    FooterComponent,
  },
  setup() {
    const isLoggedIn = ref(!!localStorage.getItem("access_token"));

    const updateLoginState = (state) => {
      isLoggedIn.value = state;
    };

    provide("isLoggedIn", isLoggedIn);
    provide("updateLoginState", updateLoginState);

    return {
      isLoggedIn,
      updateLoginState,
    };
  },
};
</script>
