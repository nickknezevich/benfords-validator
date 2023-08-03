<script setup>
import { Form, Field } from 'vee-validate';
import * as Yup from 'yup';

import { useAuthStore } from '../stores/auth.store';

const schema = Yup.object().shape({
    username: Yup.string().required('Username is required'),
    password: Yup.string().required('Password is required')
});

function onSubmit(values, { setErrors }) {
    const authStore = useAuthStore();
    const { username, password } = values;

    return authStore.login(username, password)
        .catch(error => setErrors({ apiError: error }));
}
</script>

<template>
    <!-- <div class="alert alert-info">
        Username: test<br />
        Password: test
    </div> -->
    <img class="mb-4 mt-3" src="@/assets/logo.svg" alt="" width="72" height="57">
    <h1 class="h3 mb-3 fw-normal">Sign in</h1>
    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">

        <div class="form-group pb-2">
            <Field name="username" type="text" class="form-control" :class="{ 'is-invalid': errors.username }"
                placeholder="username" />
            <div class="invalid-feedback">{{ errors.username }}</div>
        </div>
        <div class="form-group pb-2">

            <Field name="password" type="password" class="form-control" :class="{ 'is-invalid': errors.password }"
                placeholder="password" />
            <div class="invalid-feedback">{{ errors.password }}</div>
        </div>
        <div class="form-group">
            <button class="w-100 btn btn-lg btn-primary" :disabled="isSubmitting">
                <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
                Login
            </button>
        </div>
        <div v-if="errors.apiError" class="alert alert-danger mt-3 mb-0">{{ errors.apiError }}</div>
    </Form>
</template>

<style>
.form-signin {
    max-width: 330px;
    padding: 15px;
}

.w-100 {
    width: 100% !important;
}
</style>