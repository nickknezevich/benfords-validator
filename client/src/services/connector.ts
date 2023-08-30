import Axios from "axios";

export const coreApiUrl = import.meta.env.VITE_CORE_API;

export const connector = Axios.create({
  baseURL: coreApiUrl,
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  },
});

const authToken = localStorage.getItem('user');

connector.interceptors.response.use(response => {
  return response;
}, error => {
  if (error.response.status === 401) {
      localStorage.removeItem('user');
  }
  return Promise.reject(error);
});