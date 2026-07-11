import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { courseApi } from '../api/courseApi'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])

  const totalCredits = computed(() => {
    return enrolledCourses.value.reduce((total, course) => total + Number(course.credits || 0), 0)
  })

  function enroll(course) {
    const exists = enrolledCourses.value.some((c) => c.id === course.id)
    if (!exists) {
      enrolledCourses.value.push(course)
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter((c) => c.id !== courseId)
  }

  /**
   * Advanced Pinia Pattern: Async Action
   * Fetches course details from API and performs enrollment setup in one transaction
   */
  async function fetchAndEnroll(courseId) {
    try {
      const post = await courseApi.getCourseById(courseId)
      const course = {
        id: post.id,
        name: post.title.charAt(0).toUpperCase() + post.title.slice(1, 30),
        code: `CS10${post.id}`,
        credits: post.id % 2 === 0 ? 4 : 3,
        grade: ['A', 'B', 'C', 'A', 'B'][post.id % 5]
      }
      
      // Perform mock API enrollment save request
      await courseApi.enrollStudent('STU-2026-9831', courseId)
      
      enroll(course)
      return course
    } catch (error) {
      console.error('[Pinia Store Action Error]', error)
      throw error
    }
  }

  /**
   * Setup Store $reset Pattern
   * Setup stores in Pinia do not have a default $reset method; we define and return it manually.
   */
  function $reset() {
    enrolledCourses.value = []
    console.log('[Pinia Store Reset] Enrollment state cleared.')
  }

  return {
    enrolledCourses,
    totalCredits,
    enroll,
    unenroll,
    fetchAndEnroll,
    $reset
  }
})
