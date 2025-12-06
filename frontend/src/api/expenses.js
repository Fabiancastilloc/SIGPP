// frontend/src/api/expenses.js
import apiClient from './axios-config'

const expensesApi = {
  // Obtener gastos de un proyecto
  getExpenses: (projectId) => {
    return apiClient.get(`/projects/${projectId}/expenses`)
  },
  
  // Obtener gasto específico
  getExpenseById: (projectId, expenseId) => {
    return apiClient.get(`/projects/${projectId}/expenses/${expenseId}`)
  },
  
  // Crear gasto con archivo
  createExpense: (projectId, formData) => {
    return apiClient.post(`/projects/${projectId}/expenses`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // Eliminar gasto
  deleteExpense: (projectId, expenseId) => {
    return apiClient.delete(`/projects/${projectId}/expenses/${expenseId}`)
  },
  
  // Descargar soporte
  downloadSoporte: (filename) => {
    return apiClient.get(`/uploads/${filename}`, {
      responseType: 'blob'
    })
  }
}

export default expensesApi
