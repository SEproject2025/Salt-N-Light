<template>
  <div class="hero-section">
    <header>
      <div></div>
      <nav></nav>
    </header>

    <main>
      <section class="hero">
        <div class="hero-content">
          <h1>Connecting Churches and Missionaries Worldwide.</h1>
          <p>
            Empowering partnerships for a greater impact. Discover, connect, and
            support like-minded churches and missionaries.
          </p>
          <div class="cta-buttons">
            <button class="get-started-btn" @click="getStarted">
              Get Started
            </button>
            <button class="learn-more-btn" @click="learnMore">
              Learn More
            </button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: "HeroSection",
  methods: {
    getStarted() {
      // Redirect to RegistrationPagePage
      this.$router.push("/RegistrationPage");
    },
    learnMore() {
      // Scroll to the About Us section
      const aboutSection = document.getElementById("about-us");
      if (aboutSection) {
        aboutSection.scrollIntoView({ behavior: "smooth" });
      }
    },
  },
};
</script>

<style scoped>
/* Global resets */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Header styling */
header {
  display: flex;
  justify-content: space-between;
  padding: 20px 50px;
  position: absolute;
  width: 100%;
  z-index: 10;
}

.logo-link {
  font-size: 18px;
  color: white;
  text-decoration: none;
}

nav {
  display: flex;
  align-items: center;
}

.nav-link {
  color: white;
  margin: 0 15px;
  text-decoration: none;
}

/* Hero section styling */
.hero {
  height: 100vh;
  background-image: url("/src/assets/pictures/missionary_background.jpg");
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  color: white;
  padding: 0 20px;
}

.hero-content {
  max-width: 700px;
}

.hero h1 {
  font-size: 3.5rem;
  margin-bottom: 20px;
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 40px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
}

.get-started-btn,
.learn-more-btn {
  padding: 12px 30px;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  cursor: pointer;
  margin: 0 10px;
}

.get-started-btn {
  background-color: white;
  color: black;
  font-weight: bold;
}

.learn-more-btn {
  background-color: transparent;
  color: white;
  border: 2px solid white;
  font-weight: bold;
}
</style>
