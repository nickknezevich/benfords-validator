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
    <main class="d-flex w-100">
        <div class="container d-flex flex-column">
            <div class="row vh-100">
                <div class="col-sm-10 col-md-8 col-lg-6 col-xl-5 mx-auto d-table h-100">
                    <div class="d-table-cell align-middle">

                        <div class="text-center mt-4">
                            <h1 class="h2">Benford's Validator</h1>
                            <p class="lead">
                                Sign in to your account to continue
                            </p>
                        </div>
                        <div class="card">
                            <div class="card-body">
                                <div class="m-sm-3">
                                    <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
                                        <div class="mb-3">
                                            <label class="form-label">Email</label>
                                            <Field name="username" type="email" class="form-control form-control-lg"
                                                :class="{ 'is-invalid': errors.username }" placeholder="username" />
                                            <div class="invalid-feedback">{{ errors.username }}</div>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Password</label>
                                            <Field name="password" type="password" class="form-control form-control-lg"
                                                :class="{ 'is-invalid': errors.password }" placeholder="password" />
                                            <div class="invalid-feedback">{{ errors.password }}</div>
                                        </div>
                                        <div class="form-group">
                                            <button class="w-100 btn btn-lg btn-primary" :disabled="isSubmitting">
                                                <span v-show="isSubmitting"
                                                    class="spinner-border spinner-border-sm mr-1"></span>
                                                Login
                                            </button>
                                        </div>
                                        <div v-if="errors.apiError" class="alert alert-danger mt-3 mb-0">Provided credentials are invalid!</div>
                                    </Form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
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