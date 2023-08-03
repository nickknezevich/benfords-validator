import Axios from "axios";

export const connector = Axios.create({
  baseURL: "http://127.0.0.1:5001",
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  },
});

const authToken = localStorage.getItem('user');
connector.interceptors.response.use(response => {
  return response;
}, error => {
  if (error.response.status === 401) {
      console.log('token expired',error.response)
      localStorage.removeItem('user');
  }
  return Promise.reject(error);
});

export const getUsers = async query => {
  return connector.get('/api/users?q='+query);
};