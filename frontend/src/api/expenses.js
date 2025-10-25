import apiClient from './axios-config'

const expensesApi = {
  getExpenses: (projectId) => {
    return apiClient.get('/expenses', { params: { project_id: projectId } })
  },
  
  createExpense: (expenseData) => {
    return apiClient.post('/expenses', expenseData)
  },
  
  approveExpense: (expenseId, approval) => {
    return apiClient.post(`/expenses/${expenseId}/approve`, approval)
  }
}

export default expensesApi
