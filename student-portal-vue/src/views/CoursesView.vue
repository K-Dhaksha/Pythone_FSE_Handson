<template>
  <div class="courses-container">
    <header class="courses-header">
      <h1 class="page-title">Explore <span class="gradient-text">Courses</span></h1>
      <p class="page-subtitle">Select a course to view details and enroll.</p>
      
      <div class="search-wrapper">
        <input 
          v-model="searchTerm" 
          type="text" 
          placeholder="Search by course name..." 
          class="search-input"
        />
        <span class="search-icon">🔍</span>
      </div>
    </header>

    <div v-if="loading" class="state-container">
      <p class="state-text">Loading course catalog...</p>
      <div class="spinner"></div>
    </div>

    <div v-else-if="error" class="state-container error-state">
      <p class="state-text error-text">{{ error }}</p>
      <button @click="fetchCourses" class="retry-btn">Retry</button>
    </div>

    <div v-else>
      <div v-if="filteredCourses.length === 0" class="no-results">
        <p>No courses found matching "{{ searchTerm }}".</p>
      </div>

      <div v-else class="courses-grid">
        <CourseCard 
          v-for="course in filteredCourses" 
          :key="course.id"
          :name="course.name"
          :code="course.code"
          :credits="course.credits"
          :grade="course.grade"
        >
          <template #actions>
            <router-link :to="`/courses/${course.id}`" class="view-details-btn">
              View Details
            </router-link>
          </template>
        </CourseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import CourseCard from '../components/CourseCard.vue'
import { courseApi } from '../api/courseApi'

const searchTerm = ref('')
const courses = ref([])
const loading = ref(true)
const error = ref(null)

async function fetchCourses() {
  loading.value = true
  error.value = null
  try {
    const posts = await courseApi.getAllCourses()
    courses.value = posts.map((post, index) => ({
      id: post.id,
      name: post.title.charAt(0).toUpperCase() + post.title.slice(1, 30),
      code: `CS10${index + 1}`,
      credits: index % 2 === 0 ? 4 : 3,
      grade: ['A', 'B', 'C', 'A', 'B'][index % 5]
    }))
  } catch (err) {
    error.value = err.message || 'Failed to load courses. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCourses()
})

const filteredCourses = computed(() => {
  return courses.value.filter(course =>
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})
</script>

<style scoped>
.courses-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.courses-header {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
}

.gradient-text {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-subtitle {
  color: #9ca3af;
  font-size: 1.1rem;
  margin: 0 0 16px 0;
}

.search-wrapper {
  position: relative;
  width: 100%;
  max-width: 500px;
}

.search-input {
  width: 100%;
  padding: 14px 20px 14px 50px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  font-size: 1rem;
  color: #ffffff;
  outline: none;
  transition: all 0.3s ease;
}

.search-input:focus {
  background: rgba(255, 255, 255, 0.08);
  border-color: #a855f7;
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.1rem;
  pointer-events: none;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.no-results {
  text-align: center;
  padding: 60px 0;
  color: #9ca3af;
  font-size: 1.1rem;
}

.view-details-btn {
  width: 100%;
  text-align: center;
  padding: 10px;
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.view-details-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
}

.state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  gap: 16px;
}

.state-text {
  font-size: 1.2rem;
  color: #9ca3af;
}

.error-text {
  color: #ef4444;
}

.retry-btn {
  padding: 10px 24px;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
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
</style>
