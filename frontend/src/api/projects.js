import apiClient from './axios-config'

const projectsApi = {
  getProjects: (filters = {}) => {
    return apiClient.get('/projects', { params: filters })
  },
  
  getProjectById: (id) => {
    return apiClient.get(`/projects/${id}`)
  },
  
  createProject: (projectData) => {
    return apiClient.post('/projects', projectData)
  },
  
  submitProject: (projectId) => {
    return apiClient.post(`/projects/${projectId}/submit`)
  },
  
  validateProject: (projectId, validationData) => {
    return apiClient.post(`/projects/${projectId}/validate`, validationData)
  },
  
  activateProject: (projectId, activationData) => {
    return apiClient.post(`/projects/${projectId}/activate`, activationData)
  }
}

export default projectsApi
