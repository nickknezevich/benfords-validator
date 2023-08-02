import Axios from "axios";

export const connector = Axios.create({
  baseURL: "http://127.0.0.1:5001",
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  },
});

const authToken = localStorage.getItem('user');
// connector.interceptors.request.use((config) => {
//   config.params = config.params || {};
//   config.headers = {
//     Authorization: authToken ? authToken.token : ''
//   }
//   return config;
// });

export const getUsers = async query => {
  return connector.get('/api/users?q='+query);
};