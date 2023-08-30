<script setup lang="ts">
import { ref, onMounted } from "vue";
import { storeToRefs } from "pinia";
import { useValidationsStore } from "@/stores/validations.store";
const validationsStore = useValidationsStore();
const { validations, isLoadingValidations, isSubmiting, errors } =
  storeToRefs(validationsStore);
const date = ref(null);
const dialog = ref(false);
const resultsDialog = ref(false);
const selectedChartResults = ref<any>(null);
const emit = defineEmits<{
  (e: "close-dialog", value: boolean): void;
}>();
import ResultsChart from "@/components/ResultsChart.vue";

import moment from "moment";
import ValidationEntryForm from "@/components/ValidationEntryForm.vue";

type DataTableHeader = {
  key: string;
  title: string;
  colspan?: number;
  rowspan?: number;
  fixed?: boolean;
  align?: "start" | "end";
  width?: number;
  minWidth?: string;
  maxWidth?: string;
  sortable?: boolean;
};

const headers: DataTableHeader[] = [
  {
    title: "ID",
    align: "start",
    sortable: false,
    key: "id",
  },
  {
    title: "Date",
    align: "start",
    sortable: false,
    key: "created_at",
  },
  {
    title: "User",
    align: "start",
    sortable: false,
    key: "user",
  },
  {
    title: "Validation Result",
    align: "start",
    sortable: false,
    key: "result",
  },
];

const dataTableSettings = {
  itemsPerPage: 10,
};

const page = ref(1);
const selectedItem = ref<string | null>("0");

const search = () => {
  validationsStore.getValidations({
    date: date.value,
  });
};

const handleRowClick = (id: string, result: any) => {
  selectedItem.value = id;
  openChartsDialog(result);
};

const openChartsDialog = (result: any) => {
  resultsDialog.value = true;
  selectedChartResults.value = result;
};

const closeDialog = () => {
  dialog.value = false;
};

const closeResultsDialog = () => {
  resultsDialog.value = false;
};

onMounted(() => {
  validationsStore.getValidations();
});
</script>
<template>
  <v-container fluid>
    <header class="text-h5">Validation Entries</header>
  </v-container>
  <form @submit.prevent="search">
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="2">
          <label class="mb-2">Validation Date</label>
          <VueDatePicker
            v-model="date"
            class="mt-1"
            dark
            :enableTimePicker="false"
          />
        </v-col>
        <v-col cols="12" md="2" class="mt-7"
          ><v-btn
            variant="flat"
            color="light-green-darken-1"
            :disabled="isLoadingValidations"
            :loading="isLoadingValidations"
            @click="search"
            >Search</v-btn
          ></v-col
        >
        <v-col class="mt-7">
          <v-btn
            variant="flat"
            color="light-green-darken-1"
            :disabled="isLoadingValidations"
            class="float-right"
            :loading="isLoadingValidations"
            @click="dialog = true"
            >Add New Entry</v-btn
          >
        </v-col>
      </v-row>
    </v-container>
  </form>
  <v-container fluid>
    <v-data-table
      v-if="validations !== null"
      v-model:page="page"
      v-model:page-count="validations.length"
      :items-per-page="dataTableSettings.itemsPerPage"
      :headers="headers"
      :items="validations"
      :loading="isLoadingValidations"
      item-selectable
      single-select
      class="elevation-1"
      fixed-header
      height="500px"
    >
      <template v-slot:item="{ item }" v-slot:item-clickable="true">
        <tr
          class="v-data-table__tr v-data-table__tr--clickable"
          :class="{ selected: item.columns.id == selectedItem }"
          @click="handleRowClick(item.columns.id, item.columns.result)"
        >
          <td @click:exact="handleRowClick">{{ item.columns.id }}</td>
          <td>
            {{ moment(item.columns.created_at).format("MM/DD/YYYY HH:mm") }}
          </td>
          <td>
            <strong
              >{{ item.columns.user.first_name }}
              {{ item.columns.user.last_name }}</strong
            >
          </td>
          <td>
            Passed Validation:
            <v-icon
              v-if="item.columns.result.passed_validation === false"
              icon="mdi-close"
              color="red-darken-2"
            ></v-icon>
            <v-icon
              v-if="item.columns.result.passed_validation === true"
              icon="mdi-check-bold"
              color="green-darken-2"
            ></v-icon>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>

  <v-dialog v-model="dialog" width="600">
    <v-card>
      <v-card-title>
        <div class="text-h5 mt-2">
          Add New Validation Entry<v-btn
            class="float-right"
            @click="closeDialog"
            variant="text"
            icon="mdi-close"
          ></v-btn>
        </div>
      </v-card-title>
      <v-card-text class="mb-2">
        <ValidationEntryForm v-on:close-dialog="closeDialog" />
      </v-card-text>
    </v-card>
  </v-dialog>
  <v-dialog v-model="resultsDialog" width="600">
    <v-card>
      <v-card-title>
        <div class="text-h5 mt-2">
          Validation Results<v-btn
            class="float-right"
            @click="closeResultsDialog"
            variant="text"
            icon="mdi-close"
          ></v-btn>
        </div>
      </v-card-title>
      <v-card-text class="mb-2">
        <ResultsChart
          v-bind:results="selectedChartResults"
          v-on:close-dialog="closeResultsDialog"
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<style>
tr.v-data-table__td.selected {
  border-left: 3px solid orange;
  background-color: orange !important;
  color: orange;
}

tr.v-data-table__tr.selected {
  border-left: 3px solid orange;
  background-color: orange !important;
  color: orange;
}
</style>
