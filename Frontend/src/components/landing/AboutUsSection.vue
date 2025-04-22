<template>
  <section id="about-us" class="about-us-section">
    <div class="content-container">
      <div class="text-content">
        <h2>About Us</h2>
        <h1>Uniting Churches and Missionaries for a Greater Purpose</h1>
        <p>
          At Evangelium, we believe in the power of meaningful connections to
          drive change and spread hope around the world.
        </p>
        <p>
          Our platform bridges the gap between churches and missionaries,
          enabling partnerships rooted in shared values and a unified mission.
        </p>
        <!-- <button class="cta-btn" @click="scrollToBenefits">See Benefits</button> -->
      </div>
      <div class="image-container">
        <img src="@/assets/pictures/hug.jpg" alt="Missionary group image" />
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "AboutUsSection",
  methods: {
    scrollToBenefits() {
      const benefitsSection = document.getElementById("benefits");
      if (benefitsSection) {
        benefitsSection.scrollIntoView({ behavior: "smooth" });
      }
    },
  },
};
</script>

<style scoped>
.about-us-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px;
  background-color: #f7f7f7;
  min-height: 600px;
}

.content-container {
  display: flex;
  max-width: 1200px;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.text-content {
  max-width: 500px;
  margin-right: 20px;
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
