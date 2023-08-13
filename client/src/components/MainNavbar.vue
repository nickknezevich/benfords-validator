<script setup>
import { useAuthStore } from '../stores/auth.store';
const authStore = useAuthStore();

const { isAuthenticated } = authStore;
console.log("IS_AUTHENTICATED", isAuthenticated)
if (authStore.isAuthenticated === true) {
  const { user } = authStore.user;
}

const { user } = authStore.user;

const logout = () => {
  authStore.logout();
}
</script>

<template>
    
    <nav class="navbar navbar-expand navbar-light navbar-bg">
        <a class="sidebar-toggle js-sidebar-toggle">
            <i class="hamburger align-self-center"></i>
        </a>

        <div class="navbar-collapse collapse">
            <ul class="navbar-nav navbar-align">
                <li class="nav-item dropdown">
                    <a class="nav-icon dropdown-toggle d-inline-block d-sm-none" href="#" data-bs-toggle="dropdown">
                        <i class="align-middle" data-feather="settings"></i>
                    </a>

                    <a class="nav-link dropdown-toggle d-none d-sm-inline-block" href="#" data-bs-toggle="dropdown">
                        <img :src="user.picture" class="avatar img-fluid rounded me-1 rounded-circle" :alt="user.first_name" /> <span
                            class="text-dark">{{ user.first_name }} {{ user.last_name }}</span>
                    </a>
                    <div class="dropdown-menu dropdown-menu-end">
                        <a class="dropdown-item" href="pages-profile.html"><i class="align-middle me-1"
                                data-feather="user"></i> Profile</a>
                        
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" @click="logout()">Log out</a>
                    </div>
                </li>
            </ul>
        </div>
    </nav>
</template>

<style>

.sidebar-toggle {
    cursor: pointer;
    display: flex;
    height: 26px;   
    width: 26px;
    margin-left: 10px;
}

.dropdown-toggle::after {
    display: inline-block;
    margin-left: 0.255em;
    vertical-align: 0.255em;
    content: "";
    border-top: 0px transparent;
    border-right: solid !important;
    border-bottom: solid;
    border-left: 0.3em transparent;
}

.dropdown-menu.dropdown-menu-lg.dropdown-menu-end.py-0.show {
    width: 350px;
}

.dropdown, .dropdown-center, .dropend, .dropstart, .dropup, .dropup-center {
    position: relative;
    margin-right: 10px;
}

</style>