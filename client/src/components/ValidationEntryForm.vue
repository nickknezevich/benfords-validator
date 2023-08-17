<script setup>

import { Form, Field } from 'vee-validate';
import * as Yup from 'yup';
import { mixed } from 'yup';
import { useValidationEntriesStore } from '../stores/validation_entries.store';
import { defineProps, defineEmits, ref, toRefs, watch } from 'vue';
import Modal from './Modal.vue';
import { useToast } from "vue-toastification";

const schema = Yup.object().shape({
    title: Yup.string().required('File title is required'),
    reference_column: Yup.string().required('Reference column is required'),
    file: Yup.mixed().required('File is required'),
    separator: Yup.string()
});

const toast = useToast();

const emit = defineEmits();

const closeableModal = ref(false);

const modal = ref(false);

const showModal = ref(true);

function onSubmit(values, { setErrors, isSubmitting }) {
    const validationEntriesStore = useValidationEntriesStore();
    const { title, reference_column, file, separator } = values;

    validationEntriesStore.add(title, file, reference_column, separator)
        .then(() => {
            toast.success("New Validation Succesfully Added!", {
                timeout: 2000
            });
            emit("update:modelValue", false) // Close the modal after successful submission
        })
        .catch(error => {
            setErrors(error.response.data.errors)
            toast.error(`There was an error while adding a new Validation Entry`, {
                timeout: 2000
            });
        });

}

</script>
<template>
    <Modal v-model="closeableModal" closeable header="Add new Validation Entry">
        <Form @submit="onSubmit" :validation-schema="schema" v-slot="{ errors, isSubmitting }">
            <div class="form-group pb-3">
                <label for="title" class="form-label">File title</label>
                <Field name="title" type="text" class="form-control" :class="{ 'is-invalid': errors.title }"
                    placeholder="File title" />
                <div class="invalid-feedback">{{ errors.title }}</div>
            </div>
            <div class="form-group pb-3">
                <label for="reference_column" class="form-label">Reference Column</label>
                <Field name="reference_column" type="text" class="form-control"
                    :class="{ 'is-invalid': errors.reference_column }" placeholder="Reference Column" />
                <div class="invalid-feedback">{{ errors.reference_column }}</div>
            </div>
            <div class="form-group pb-3">
                <label for="reference_column" class="form-label">File</label>
                <Field name="file" type="file" ref="file" class="form-control" :class="{ 'is-invalid': errors.file }"
                    placeholder="File" />
                <div class="invalid-feedback">{{ errors.file }}</div>
            </div>
            <div class="form-group pb-3">
                <label for="separator" class="form-label">Separator</label>
                <Field name="separator" type="text" class="form-control" :class="{ 'is-invalid': errors.separator }"
                    placeholder="Separator" />
                <div class="invalid-feedback">{{ errors.separator }}</div>
                <small class="text-muted">Eg. \td</small>
            </div>
            <div class="form-group pb-3">
                <button class="btn btn-lg btn-primary" :disabled="isSubmitting">
                    <span v-show="isSubmitting" class="spinner-border spinner-border-sm mr-1"></span>
                    Save
                </button>
            </div>
        </Form>
    </Modal>
</template>

