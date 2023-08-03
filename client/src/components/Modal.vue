<template>
    <teleport to="body">
        <transition name="fade">
            <div v-if="modelValue" class="pt-5 position-fixed top-0 start-0 h-100 w-100 vue-modal"
                style="background-color: rgba(0, 0, 0, 0.25)">
                <div id="backdrop" @click="backdropClick" class="modal1-dialog h-100 overflow-auto">
                    <div class="card px-0" :class="(container == null) ? 'container' : `container-${container}`"
                        :style="(maxwidth != null) ? `max-width: ${maxwidth}` : null">
                        <div class="card-header h2">
                            {{ header }}
                            <button v-if="closeable" @click='$emit("update:modelValue", false)'
                                class="btn btn-text float-end"><strong><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
  <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
</svg></strong></button>
                        </div>
                        <div class="card-body">
                            <slot></slot>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </teleport>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';

const backdropClick = (event) => {
    if (event.target.id == 'backdrop' && props.closeable == true) {
        emit("update:modelValue", false);
    }
}

const props = defineProps({
    modelValue: {
        type: Boolean,
        required: true,
        default: false
    },
    closeable: {
        type: Boolean,
        required: false,
        default: false
    },
    header: {
        type: String,
        required: false,
        default: null
    },
    container: {
        type: String,
        required: false,
        default: null
    },
    maxwidth: {
        type: String,
        required: false,
        default: null
    }
})

const emit = defineEmits();

const isVisible = ref(false);

</script>

<style scoped>
.vue-modal {
    z-index: 1000;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0
}

</style>