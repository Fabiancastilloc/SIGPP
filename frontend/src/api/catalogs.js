import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1'

const catalogsApi = {
  getSedes: () => {
    return axios.get(`${API_URL}/catalogs/sedes`)
  },
  
  getFacultades: (sedeId = null) => {
    return axios.get(`${API_URL}/catalogs/facultades`, {
      params: sedeId ? { sede_id: sedeId } : {}
    })
  },
  
  getCarreras: (facultadId = null) => {
    return axios.get(`${API_URL}/catalogs/carreras`, {
      params: facultadId ? { facultad_id: facultadId } : {}
    })
  },
  
  getProfesores: () => {
    return axios.get(`${API_URL}/catalogs/profesores`)
  }
}

export default catalogsApi
