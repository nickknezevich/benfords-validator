import { defineStore } from 'pinia';

import { connector } from '@/services/connector';
import router from '../router';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        user: JSON.parse(localStorage.getItem('user')),
        isAuthenticated: false,
        returnUrl: null
    }),
    actions: {
        async login(username, password) {
            const authData = await connector.post(`/api/auth/login`, { username, password });
            // update pinia state
            this.user = authData.data.data;
            this.isAuthenticated = true;

            console.log("IS_AUTH", this.isAuthenticated)
            // store user details and jwt in local storage to keep user logged in between page refreshes
            localStorage.setItem('user', JSON.stringify(this.user));

            // redirect to previous url or default to home page
            window.location.href = this.returnUrl || '/'
        },
        logout() {
            this.user = null;
            this.isAuthenticated = false;
            localStorage.removeItem('user');
            router.go('login')
        }
    }
});