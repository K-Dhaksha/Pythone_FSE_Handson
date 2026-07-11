<template>
  <div class="detail-container">
    <div class="back-link-wrapper">
      <router-link to="/courses" class="back-link">← Back to Courses</router-link>
    </div>

    <div v-if="loading" class="state-container">
      <p class="state-text">Loading course details...</p>
      <div class="spinner"></div>
    </div>

    <div v-else-if="error" class="state-container error-state">
      <h2>Error Loading Details</h2>
      <p class="state-text error-text">{{ error }}</p>
      <router-link to="/courses" class="btn btn-primary">Browse Courses</router-link>
    </div>

    <div v-else-if="!course" class="not-found">
      <h2>Course Not Found</h2>
      <p>The course with ID {{ $route.params.id }} could not be found.</p>
      <router-link to="/courses" class="btn btn-primary">Browse Courses</router-link>
    </div>

    <div v-else class="detail-card">
      <div class="detail-header">
        <span class="course-code">{{ course.code }}</span>
        <h1 class="course-title">{{ course.name }}</h1>
      </div>

      <div class="detail-body">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Credits</span>
            <span class="info-value">{{ course.credits }} Credits</span>
          </div>
          <div class="info-item">
            <span class="info-label">Target Grade</span>
            <span class="info-value grade-value">{{ course.grade }}</span>
          </div>
        </div>

        <div class="course-description">
          <h3>Course Description</h3>
          <p>
            This course covers advanced concepts and fundamentals. It includes theoretical foundations,
            practical implementation tasks, hands-on lab sessions, and direct mentorship designed to prepare you for
            industry requirements.
          </p>
        </div>
      </div>

      <div class="detail-footer">
        <button 
          v-if="!isEnrolled" 
          @click="handleEnroll" 
          class="enroll-btn"
        >
          Enroll in Course
        </button>
        <div v-else class="already-enrolled">
          <span class="check-icon">✓</span> Enrolled in this course
          <router-link to="/profile" class="view-profile-link">View in Profile</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useEnrollmentStore } from '../stores/enrollment'
import { courseApi } from '../api/courseApi'

const route = useRoute()
const router = useRouter()
const enrollmentStore = useEnrollmentStore()

// Use storeToRefs to safely destructure reactive state
const { enrolledCourses } = storeToRefs(enrollmentStore)

const courseId = Number(route.params.id)
const course = ref(null)
const loading = ref(true)
const error = ref(null)

async function fetchCourseDetails() {
  loading.value = true
  error.value = null
  try {
    const post = await courseApi.getCourseById(courseId)
    course.value = {
      id: post.id,
      name: post.title.charAt(0).toUpperCase() + post.title.slice(1, 30),
      code: `CS10${post.id}`,
      credits: post.id % 2 === 0 ? 4 : 3,
      grade: ['A', 'B', 'C', 'A', 'B'][post.id % 5]
    }
  } catch (err) {
    error.value = err.message || 'Failed to retrieve course details.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCourseDetails()
})

const isEnrolled = computed(() => {
  return course.value ? enrolledCourses.value.some(c => c.id === course.value.id) : false
})

function handleEnroll() {
  if (course.value) {
    enrollmentStore.enroll(course.value)
    router.push('/profile')
  }
}
</script>

<style scoped>
.detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 24px;
}

.back-link-wrapper {
  margin-bottom: 24px;
}

.back-link {
  color: #a855f7;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.back-link:hover {
  color: #6366f1;
}

.not-found,
.state-container {
  text-align: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 48px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.state-text {
  font-size: 1.2rem;
  color: #9ca3af;
}

.error-text {
  color: #ef4444;
  margin-bottom: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(168, 85, 247, 0.2);
  border-top-color: #a855f7;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.detail-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.detail-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding-bottom: 24px;
}

.course-code {
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #a855f7;
  background: rgba(168, 85, 247, 0.15);
  padding: 6px 12px;
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 16px;
}

.course-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
}

.detail-body {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.info-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 0.85rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
}

.grade-value {
  color: #34d399;
}

.course-description h3 {
  color: #ffffff;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 12px;
}

.course-description p {
  color: #9ca3af;
  line-height: 1.6;
  margin: 0;
}

.detail-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.enroll-btn {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  color: #ffffff;
  border: none;
  padding: 14px 36px;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4);
}

.enroll-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
}

.already-enrolled {
  color: #34d399;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.1rem;
}

.check-icon {
  background: rgba(52, 211, 153, 0.15);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.view-profile-link {
  color: #a855f7;
  text-decoration: underline;
  margin-left: 8px;
  font-weight: 500;
}

.view-profile-link:hover {
  color: #6366f1;
}

@media (max-width: 640px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
