<template>
  <div class="profile-container">
    <header class="profile-header">
      <h1 class="page-title">My <span class="gradient-text">Profile</span></h1>
      <p class="page-subtitle">Manage your enrolled courses and view academic summary.</p>
    </header>

    <div class="profile-layout">
      <!-- Enrollment Summary Dashboard -->
      <section class="summary-section">
        <div class="summary-card">
          <h3>Academic Summary</h3>
          <div class="stat-group">
            <div class="stat-item">
              <span class="stat-label">Enrolled Courses</span>
              <span class="stat-value">{{ enrollmentStore.enrolledCourses.length }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Total Credits</span>
              <span class="stat-value credits-value">{{ enrollmentStore.totalCredits }}</span>
            </div>
          </div>
          <div class="profile-info">
            <div class="info-row">
              <span class="info-lbl">Student Name:</span>
              <span class="info-val">K-Dhaksha</span>
            </div>
            <div class="info-row">
              <span class="info-lbl">Student ID:</span>
              <span class="info-val">STU-2026-9831</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Enrolled Courses List -->
      <section class="enrolled-section">
        <h2>My Enrolled Courses</h2>
        
        <div v-if="enrollmentStore.enrolledCourses.length === 0" class="empty-state">
          <div class="empty-icon">📂</div>
          <p>You are not currently enrolled in any courses.</p>
          <router-link to="/courses" class="btn-browse">Browse Catalog</router-link>
        </div>

        <div v-else class="enrolled-list">
          <div 
            v-for="course in enrollmentStore.enrolledCourses" 
            :key="course.id" 
            class="enrolled-item"
          >
            <div class="enrolled-info">
              <span class="enrolled-code">{{ course.code }}</span>
              <h3 class="enrolled-name">{{ course.name }}</h3>
              <span class="enrolled-credits">{{ course.credits }} Credits</span>
            </div>
            <div class="enrolled-actions">
              <span class="enrolled-grade">Target: {{ course.grade }}</span>
              <button 
                @click="enrollmentStore.unenroll(course.id)" 
                class="unenroll-btn"
                title="Drop Course"
              >
                Drop Course
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment'

const enrollmentStore = useEnrollmentStore()
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.profile-header {
  text-align: left;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 8px 0;
}

.gradient-text {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-subtitle {
  color: #9ca3af;
  font-size: 1.1rem;
  margin: 0;
}

.profile-layout {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 32px;
  align-items: start;
}

.summary-section {
  position: sticky;
  top: 100px;
}

.summary-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.summary-card h3 {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 16px;
}

.stat-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-label {
  font-size: 0.9rem;
  color: #9ca3af;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
}

.credits-value {
  color: #a855f7;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 16px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.info-lbl {
  color: #9ca3af;
}

.info-val {
  color: #ffffff;
  font-weight: 600;
}

.enrolled-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.enrolled-section h2 {
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.empty-state {
  background: rgba(255, 255, 255, 0.03);
  border: 1px dotted rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  padding: 60px 40px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  font-size: 3rem;
}

.empty-state p {
  color: #9ca3af;
  margin: 0;
  font-size: 1.05rem;
}

.btn-browse {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  padding: 10px 24px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.btn-browse:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
}

.enrolled-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.enrolled-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  transition: border-color 0.2s ease;
}

.enrolled-item:hover {
  border-color: rgba(168, 85, 247, 0.3);
}

.enrolled-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.enrolled-code {
  font-size: 0.8rem;
  font-weight: 700;
  color: #a855f7;
  background: rgba(168, 85, 247, 0.1);
  padding: 4px 8px;
  border-radius: 6px;
}

.enrolled-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

.enrolled-credits {
  font-size: 0.85rem;
  color: #9ca3af;
}

.enrolled-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.enrolled-grade {
  font-size: 0.9rem;
  color: #34d399;
  font-weight: 500;
}

.unenroll-btn {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.unenroll-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .profile-layout {
    grid-template-columns: 1fr;
  }
  .summary-section {
    position: static;
  }
  .enrolled-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  .enrolled-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  .enrolled-actions {
    width: 100%;
    justify-content: space-between;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 12px;
  }
}
</style>
