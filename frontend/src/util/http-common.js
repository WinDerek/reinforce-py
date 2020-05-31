import axios from 'axios'

export const AXIOS = axios.create({
  baseURL: `http://10.19.125.108:45679/api`
})
