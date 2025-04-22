<template>
  <footer class="bg-gray-900 text-gray-300 px-6 py-8 text-lg">
    <div
      class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center space-y-6 md:space-y-0"
    >
      <!-- Site Logo / Title -->
      <div class="site-logo">
        <a href="/LandingPage">
          <img
            src="@/assets/pictures/Evangelium-Logo-02.png"
            alt="Evangelium Logo"
            class="logo"
          />
        </a>
      </div>

      <!--Router Links-->
      <div class="flex space-x-6">
        <router-link to="/LandingPage" class="hover:text-white"
          >About</router-link
        >
        <router-link to="/AppLogin" class="hover:text-white"
          >Log in</router-link
        >
        <router-link to="/RegistrationPage" class="hover:text-white"
          >Register</router-link
        >
      </div>

      <!-- Social Media Links -->
      <div class="flex space-x-4">
        <a
          href="@/pages/UserProfile.vue
          blank"
          class="hover:text-white"
          >🔔</a
        >
        <a
          href="@/pages/SearchPage.vue"
          target="_blank"
          class="hover:text-white"
          >🔍</a
        >
        <a
          href="@/pages/UserProfile.vue"
          target="_blank"
          class="hover:text-white"
          >👤</a
        >
      </div>
    </div>

    <div class="mt-6 text-center text-sm text-gray-500">
      &copy; 2025 Evangelium. All rights reserved.
    </div>
  </footer>
</template>

<style scoped>
/* Site Logo */
.site-logo .logo {
  margin-left: 50px;
  height: auto;
  width: 165px;
  border-radius: 0;
  object-fit: contain;
}
</style>
