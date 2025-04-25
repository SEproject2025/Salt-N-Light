<template>
  <footer class="bg-gray-900 text-gray-300 px-6 py-8 text-lg">
    <div class="max-w-6xl mx-auto flex items-center justify-between relative">
      <!-- Left: Site Logo -->
      <div class="site-logo">
        <a href="/LandingPage">
          <img
            src="@/assets/pictures/Evangelium-Logo-02.png"
            alt="Evangelium Logo"
            class="logo"
          />
        </a>
      </div>

      <!-- Center: Navigation Links (Absolutely centered) -->
      <div class="absolute left-1/2 transform -translate-x-1/2 flex space-x-6">
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

      <!-- Right: Social Icons -->
      <div class="flex space-x-4">
        <a
          href="https://www.instagram.com/evangelium.app?igsh=MWo0aWQ2a3R3Ym96bg=="
          target="_blank"
          class="hover:text-pink-600"
        >
          <span class="hover:text-white material-symbols-outlined"
            >photo_camera</span
          >
        </a>
      </div>
    </div>

    <!-- Footer Bottom -->
    <div class="mt-6 text-center text-sm text-gray-500">
      &copy; 2025 Evangelium. All rights reserved.<br />All photos were obtained
      from
      <a
        href="https://unsplash.com/"
        target="_blank"
        class="text-gray-400 hover:text-white"
        >Unsplash</a
      >.
    </div>
  </footer>
</template>

<style scoped>
.site-logo .logo {
  height: auto;
  width: 165px;
  object-fit: contain;
}
</style>
