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
      // Redirect to RegistrationPage
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
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
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
  position: relative;
}

.hero::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  background: rgba(0, 0, 0, 0.2);
}

.hero-content {
  max-width: 700px;
  width: 100%;
  position: relative;
  z-index: 1;
}

.hero h1 {
  font-size: 3.5rem;
  margin-bottom: 20px;
  line-height: 1.2;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 40px;
  line-height: 1.5;
  font-weight: 400;
  letter-spacing: 0.2px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.get-started-btn,
.learn-more-btn {
  padding: 12px 30px;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  cursor: pointer;
  white-space: nowrap;
  font-weight: 500;
  letter-spacing: 0.3px;
  transition: all 0.3s ease;
}

.get-started-btn {
  background-color: white;
  color: black;
  font-weight: 600;
}

.get-started-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.learn-more-btn {
  background-color: transparent;
  color: white;
  border: 2px solid white;
  font-weight: 600;
}

.learn-more-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

/* Mobile Responsive Styles */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
    padding: 0 10px;
  }

  .hero p {
    font-size: 1rem;
    padding: 0 20px;
  }

  .cta-buttons {
    padding: 0 20px;
  }

  .get-started-btn,
  .learn-more-btn {
    width: 100%;
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .hero h1 {
    font-size: 1.75rem;
  }

  .hero p {
    font-size: 0.9rem;
  }
}
</style>
