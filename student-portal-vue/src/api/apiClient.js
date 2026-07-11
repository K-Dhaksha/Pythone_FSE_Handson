import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request Interceptor: Attach mock auth token
apiClient.interceptors.request.use(
  (config) => {
    config.headers['Authorization'] = 'Bearer mock-token-xyz123'
    console.log(`[API Request Started] ${config.method.toUpperCase()} -> ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response Interceptor: Unwrap response data & standardize error messages
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API Response Success] -> Status: ${response.status}`)
    // Return response.data directly so callers don't need to parse the Axios wrapper
    return response.data
  },
  (error) => {
    console.error('[API Response Error]', error)
    
    // Standardize error message and status code
    const standardizedError = {
      message: error.response?.data?.message || error.message || 'An unexpected API error occurred.',
      statusCode: error.response?.status || 500,
      originalError: error
    }
    
    return Promise.reject(standardizedError)
  }
)

export default apiClient
