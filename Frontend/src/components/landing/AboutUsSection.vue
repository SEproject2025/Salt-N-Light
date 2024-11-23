<<<<<<< HEAD
<template>
  <section class="about-us-section">
    <div class="content-container">
      <div class="text-content">
        <h2>About Us</h2>
        <h1>Uniting Churches and Missionaries for a Greater Purpose</h1>
        <p>
          At SaltnLight, we believe in the power of meaningful connections to
          drive change and spread hope around the world.
        </p>
        <p>
          Our platform is designed to bridge the gap between churches and
          missionaries, enabling partnerships that are rooted in shared values
          and a unified mission.
        </p>
        <button class="cta-btn">See Benefits</button>
      </div>
      <div class="image-container">
        <img
          src="@/assets/pictures/Africa-missionaries.jpg"
          alt="Missionary group image"
        />
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "AboutUsSection",
};
</script>

<style scoped>
.about-us-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px;
  background-color: #f7f7f7;
  min-height: 600px; /* added this to prevent box from shrinking too small to size of text/picture */
}

.content-container {
  display: flex;
  max-width: 1200px;
  justify-content: space-between;
  align-items: center;
}

/* This prevents the text caret from showing up in any text area not sure if it worked */
.text-content input:focus,
.text-content textarea:focus {
  caret-color: transparent;
}

.text-content {
  max-width: 500px;
  margin-right: 200px;
}

.text-content h2 {
  font-size: 1rem;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #333;
  margin-bottom: 10px;
}

.text-content h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #000;
  margin-bottom: 20px;
}

.text-content p {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
}

.cta-btn {
  background-color: #000;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.image-container img {
  max-width: 500px;
  border-radius: 10px;
  object-fit: cover;
}
</style>
=======
<template>
  <section class="about-us-section">
    <div class="content-container">
      <div class="text-content">
        <h2>About Us</h2>
        <h1>Uniting Churches and Missionaries for a Greater Purpose</h1>
        <p>
          At SaltnLight, we believe in the power of meaningful connections to
          drive change and spread hope around the world.
        </p>
        <p>
          Our platform is designed to bridge the gap between churches and
          missionaries, enabling partnerships that are rooted in shared values
          and a unified mission.
        </p>
        <button class="cta-btn">See Benefits</button>
      </div>
      <div class="image-container">
        <img
          src="@/assets/pictures/Africa-missionaries.jpg"
          alt="Missionary group image"
        />
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "AboutUsSection",
};
</script>

<style scoped>
.about-us-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px;
  background-color: #f7f7f7;
  min-height: 600px; /* added this to prevent box from shrinking too small to size of text/picture */
}

.content-container {
  display: flex;
  max-width: 1200px;
  justify-content: space-between;
  align-items: center;
}

/* This prevents the text caret from showing up in any text area not sure if it worked */
.text-content input:focus,
.text-content textarea:focus {
  caret-color: transparent;
}

.text-content {
  max-width: 500px;
  margin-right: 200px;
}

.text-content h2 {
  font-size: 1rem;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #333;
  margin-bottom: 10px;
}

.text-content h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #000;
  margin-bottom: 20px;
}

.text-content p {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
}

.cta-btn {
  background-color: #000;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.image-container img {
  max-width: 500px;
  border-radius: 10px;
  object-fit: cover;
}
</style>
>>>>>>> QA
