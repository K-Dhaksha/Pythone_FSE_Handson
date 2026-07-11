<template>
  <div class="home-container">
    <section class="hero-section">
      <h1 class="hero-title">Welcome to the <span class="gradient-text">Student Portal</span></h1>
      <p class="hero-subtitle">
        Manage your academic journey, discover exciting courses, and track your progress in real-time.
      </p>
      <div class="cta-buttons">
        <router-link to="/courses" class="btn btn-primary">Browse Courses</router-link>
        <router-link to="/profile" class="btn btn-secondary">View Profile</router-link>
      </div>
    </section>

    <section class="features-section">
      <div class="feature-card">
        <div class="feature-icon">📚</div>
        <h3>Course Catalog</h3>
        <p>Explore high-quality courses with rich curriculums tailored to build your career.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Instant Enrollment</h3>
        <p>Enroll in courses with a single click and manage your curriculum on the fly.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Academic Progress</h3>
        <p>Track your credit count and performance metrics instantly from your profile.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
// Setup is empty for static landing view
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  gap: 60px;
  padding: 40px 24px;
}

.hero-section {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 0;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.2;
  margin-bottom: 20px;
  color: #ffffff;
}

.gradient-text {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #9ca3af;
  line-height: 1.6;
  margin-bottom: 36px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.btn {
  padding: 12px 28px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.feature-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-4px);
  border-color: rgba(99, 102, 241, 0.3);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 12px;
}

.feature-card p {
  color: #9ca3af;
  line-height: 1.5;
  font-size: 0.95rem;
  margin: 0;
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 2.25rem;
  }
  .cta-buttons {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
