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
        <img src="@/assets/pictures/praying.jpg" alt="Missionary group image" />
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
  padding: 60px 20px;
  background-color: #f7f7f7;
  min-height: 600px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.content-container {
  display: flex;
  max-width: 1200px;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 40px;
}

.text-content {
  max-width: 500px;
  flex: 1;
  min-width: 280px;
}

.text-content h2 {
  font-size: 1rem;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #333;
  margin-bottom: 10px;
  font-weight: 600;
}

.text-content h1 {
  font-size: 2.5rem;
  font-weight: 600;
  color: #000;
  margin-bottom: 20px;
  line-height: 1.2;
  letter-spacing: -0.5px;
}

.text-content p {
  font-size: 1rem;
  color: #555;
  margin-bottom: 20px;
  line-height: 1.6;
  font-weight: 400;
  letter-spacing: 0.2px;
}

.cta-btn {
  background-color: #000;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0.3px;
  transition: all 0.3s ease;
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.image-container {
  flex: 1;
  min-width: 280px;
  max-width: 500px;
}

.image-container img {
  width: 100%;
  height: auto;
  border-radius: 10px;
  object-fit: cover;
}

/* Mobile Responsive Styles */
@media (max-width: 768px) {
  .about-us-section {
    padding: 40px 20px;
  }

  .content-container {
    flex-direction: column;
    text-align: center;
  }

  .text-content {
    max-width: 100%;
  }

  .text-content h1 {
    font-size: 2rem;
  }

  .text-content p {
    font-size: 0.95rem;
  }

  .image-container {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .about-us-section {
    padding: 30px 15px;
  }

  .text-content h1 {
    font-size: 1.75rem;
  }

  .text-content p {
    font-size: 0.9rem;
  }
}
</style>
