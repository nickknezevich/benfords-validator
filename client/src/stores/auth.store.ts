import { defineStore } from "pinia";

import { connector } from "@/services/connector";
import router from "../router";

type User = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  image_url: string;
};

type State = {
  user: User | null;
  isAuthenticated: boolean;
  returnUrl: string | null;
  isLoading: boolean;
};

export const useAuthStore = defineStore({
  id: "auth",
  state: (): State => ({
    // initialize state from local storage to enable user to stay logged in
    user: JSON.parse(localStorage.getItem("user") as string),
    isAuthenticated: false,
    returnUrl: null,
    isLoading: false,
  }),
  actions: {
    async login(username: string, password: string): Promise<void> {
      this.isLoading = false;
      const authData: any = await connector.post(`/api/auth/login`, {
        username,
        password,
      });
      this.isLoading = false;
      this.user = authData.data.data;
      this.isAuthenticated = true;
      localStorage.setItem("user", JSON.stringify(this.user));
      window.location.href = this.returnUrl || "/";
    },
    async logout(): Promise<void> {
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem("user");
      router.go("login" as any);
    },
  },
});
