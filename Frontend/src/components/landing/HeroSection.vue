<<<<<<< HEAD
<template>
  <div id="app">
    <header>
      <div class="logo">SaltnLight Logo</div>
      <nav>
        <a href="#">About Us</a>
        <a href="#">The Team</a>
        <a href="#">FAQ</a>
        <button class="login-btn" @click="goToLogin">Log In</button>
      </nav>
    </header>

    <main>
      <section class="hero">
        <div class="hero-content">
          <h1>Connecting Churches and Missionaries Worldwide.</h1>
          <p>
            Empowering partnerships for a greater impact. Discover, connect, and
            support like-minded missionaries and churches.
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
  methods: {
    getStarted() {
      // Handle Get Started logic
      this.$router.push("/AppLogin");
      console.log("Get Started clicked");
    },
    learnMore() {
      // Handle Learn More logic
      console.log("Learn More clicked");
    },
    goToLogin() {
      // Programmatically navigate to the login page
      this.$router.push("/AppLogin");
      console.log("Get Started clicked");
    },
  },
  name: "HeroSection",
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: transparent;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
  display: flex;
  justify-content: space-between;
  padding: 20px 50px;
  background-color: transparent;
  position: absolute;
  width: 100%;
  z-index: 10;
}

.logo {
  font-size: 18px;
  color: white;
}

nav {
  display: flex;
  align-items: center;
}

nav a {
  color: white;
  margin: 0 15px;
  text-decoration: none;
}

.login-btn {
  background-color: white;
  border: none;
  color: black;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
}

main {
  display: flex;
  flex-direction: row;
  height: 100%;
}

.hero {
  flex: 1;
  background-image: url("/src/assets//pictures/missionary_background.jpg");
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  text-align: center;
  padding: 0 20px;
}

.hero-content {
  max-width: 700px;
}

.hero-content textarea:focus {
  caret-color: transparent;
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
=======
<template>
  <div id="app">
    <header>
      <div class="logo">SaltnLight Logo</div>
      <nav>
        <a href="#">About Us</a>
        <a href="#">The Team</a>
        <a href="#">FAQ</a>
        <button class="login-btn">Log In</button>
      </nav>
    </header>

    <main>
      <section class="hero">
        <div class="hero-content">
          <h1>Connecting Churches and Missionaries Worldwide.</h1>
          <p>
            Empowering partnerships for a greater impact. Discover, connect, and
            support like-minded missionaries and churches.
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
  methods: {
    getStarted() {
      // Handle Get Started logic
      console.log("Get Started clicked");
    },
    learnMore() {
      // Handle Learn More logic
      console.log("Learn More clicked");
    },
  },
  name: "HeroSection",
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background-color: transparent;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

header {
  display: flex;
  justify-content: space-between;
  padding: 20px 50px;
  background-color: transparent;
  position: absolute;
  width: 100%;
  z-index: 10;
}

.logo {
  font-size: 18px;
  color: white;
}

nav {
  display: flex;
  align-items: center;
}

nav a {
  color: white;
  margin: 0 15px;
  text-decoration: none;
}

.login-btn {
  background-color: white;
  border: none;
  color: black;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
}

main {
  display: flex;
  flex-direction: row;
  height: 100%;
}

.hero {
  flex: 1;
  background-image: url("/src/assets//pictures/missionary_background.jpg");
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  text-align: center;
  padding: 0 20px;
}

.hero-content {
  max-width: 700px;
}

.hero-content textarea:focus {
  caret-color: transparent;
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
>>>>>>> QA
