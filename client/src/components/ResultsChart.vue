<script setup>
import { Bar } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement} from 'chart.js'
import { defineProps } from 'vue';
import { Colors } from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Colors, PointElement, LineElement)

const props = defineProps(['results'])
const chartData = {
    labels: Object.keys(props.results.percentages_plot_data),
    datasets: [{data: [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6], label: "Benford's Percentages", type: 'line'}, { data: Object.values(props.results.percentages_plot_data), label: 'Results' }]
}

const chartOptions = {
    responsive: true,
    plugins: {
        title: {
            display: true,
            text: `Passed Benford's Validation: ${props.results.passed_validation}`
        }
    }
}
</script>

<template>
    <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
</template>