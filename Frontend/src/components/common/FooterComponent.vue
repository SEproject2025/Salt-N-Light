<template>
  <footer class="bg-gray-900 text-gray-300 px-6 py-8">
    <div
      class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center space-y-6 md:space-y-0"
    >
      <!-- Site Logo / Title -->
      <div class="text-xl font-semibold">MyAwesomeSite</div>

      <!-- Router Links -->
      <div class="flex space-x-6">
        <router-link to="/AboutUsSection" class="hover:text-white"
          >About</router-link
        >
        <router-link to="/AppLogin" class="hover:text-white"
          >Log in</router-link
        >
        <router-link to="/RegistrationPage" class="hover:text-white"
          >Register</router-link
        >
      </div>

      <!-- Social Icons 
       <div class="flex space-x-4">
         <a href="https://twitter.com" target="_blank" class="hover:text-white">🐦</a>
         <a href="https://facebook.com" target="_blank" class="hover:text-white">📘</a>
         <a href="https://instagram.com" target="_blank" class="hover:text-white">📸</a>
       </div>-->
    </div>

    <div class="mt-6 text-center text-sm text-gray-500">
      &copy; 2025 MyAwesomeSite. All rights reserved.
    </div>
  </footer>
</template>
