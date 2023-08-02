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
                <td>{{ validationEntry.user_id }}</td>
                <td>file place holder</td>
                <td></td>
                <td>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btn-warning btn-sm" @click="openChartsModal(validationEntry.result)">See Plot</button>
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

