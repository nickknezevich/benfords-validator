import { defineStore } from 'pinia';

import { connector } from '@/services/connector';

const authToken = JSON.parse(localStorage.getItem('user'));

export const useValidationEntriesStore = defineStore({
    id: 'validation_entries',
    state: () => ({
        validationEntries: []
    }),
    actions: {
        async getAll() {
            this.validationEntries = { loading: true };
            connector.get('/api/validation-entries', {
                headers: {
                    Authorization: `Bearer ${authToken.token}` 
                  }
            })
                .then(response => this.validationEntries = response.data.data)
                .catch(error => this.validationEntries = { error })
        },
        async add(title, file, reference_column) {
            var bodyFormData = new FormData();
            bodyFormData.append('title', title);
            bodyFormData.append('file', file);
            bodyFormData.append('reference_column', reference_column);
            const response = await connector.post(`/api/file-upload`, bodyFormData, {
                headers: {
                    Authorization: `Bearer ${authToken.token}`,
                    'Content-Type': `multipart/form-data; boundary=${bodyFormData._boundary}`
                  }
            });
            console.log(response.data.data)
            // update pinia state
            this.validationEntries.push(response.data.data);
        },
    },
    getters: {
        all(state) {
            return state.validationEntries;
        }
    }
});