<<<<<<< HEAD
<template>
  <div id="app">
    <AppNav />

    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "App",
  components: {
  },
};
</script>
=======
<template>
  <div id="app">
    <AppNav />
    <HeaderComponent />
    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view />
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
>>>>>>> QA
