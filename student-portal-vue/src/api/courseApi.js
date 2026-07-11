import apiClient from './apiClient'

export const courseApi = {
  /**
   * Fetch a list of courses (limited to 5 from placeholder posts)
   */
  getAllCourses() {
    return apiClient.get('/posts?_limit=5')
  },

  /**
   * Fetch specific course details by ID
   */
  getCourseById(id) {
    return apiClient.get(`/posts/${id}`)
  },

  /**
   * Mock enrollment endpoint
   */
  enrollStudent(studentId, courseId) {
    return apiClient.post('/posts', {
      studentId,
      courseId,
      enrolledAt: new Date().toISOString()
    })
  }
}
