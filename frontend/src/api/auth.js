import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1'

const authApi = {
  login: (credentials) => {
    return axios.post(`${API_URL}/auth/login`, credentials)
  },
  
  register: (userData) => {
    return axios.post(`${API_URL}/auth/register`, userData)
  }
}

export default authApi
