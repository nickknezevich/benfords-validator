<script setup>
import { useValidationEntriesStore } from '../stores/validation_entries.store';
import { storeToRefs } from 'pinia';
import { ref, onMounted } from 'vue';
import { defineProps, reactive } from 'vue';
import Modal from './Modal.vue';
import ValidationEntryForm from './ValidationEntryForm.vue';
import ResultsChart from './ResultsChart.vue';

const store = useValidationEntriesStore();

onMounted(async () => {
    await store.getAll();
});

const { validationEntries, loading } = storeToRefs(store);

const closeableModal = ref(false);
const chartsModal = ref(false);
const selectedChartResults = ref({1: 10})

const modal = ref(false);

const openModal = () => {
  modal.value = true;
  setTimeout(() => {
    modal.value = false;
  }, 5000);
}

const openChartsModal = (result) => {
    chartsModal.value = true;

    selectedChartResults.value = result
    console.log(result)
}

</script>

<template>
    <button type="button" class="btn btn-success btn-sm" @click="closeableModal = true">Add New Entry</button>
    <br><br>
    <div class="table-wrap">
    <table class="table table-hover table-striped" v-if="!loading">
        <thead>
            <tr>
                <th scope="col">Date / Time</th>
                <th scope="col">User</th>
                <th scope="col">File</th>
                <th scope="col">Validation Result</th>
                <th scope="col">Action</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(validationEntry, index) in validationEntries" :key="index">
                <td>{{ validationEntry.created_at }}</td>
                <td>{{ validationEntry.user.first_name }} {{ validationEntry.user.last_name }}</td>
                <td>{{ validationEntry.title }}</td>
                <td>Validation result: {{ validationEntry.result.passed_validation }} <span v-if="validationEntry.result.passed_validation === true" class="text-success"><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-check" viewBox="0 0 16 16">
  <path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/>
</svg></span> <span v-else="validationEntry.result.passed_validation === false" class="text-danger"><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
  <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
</svg></span></td>
                <td>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btn-warning btn-sm" @click="openChartsModal(validationEntry.result)"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 16">
  <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
</svg> See Chart</button>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</div>
    
    <ValidationEntryForm v-model="closeableModal" closeable header="Add New Validation Entry"/>
    <Modal v-model="chartsModal" closeable header="Validation Results">
        <ResultsChart v-bind:results="selectedChartResults" />
    </Modal>

   
</template>

<style>
.table-wrap {
    height: 400px;
    overflow-y: scroll;
}

</style>

