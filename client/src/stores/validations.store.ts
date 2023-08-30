import { defineStore } from "pinia";
import { connector } from "@/services/connector";

const user = JSON.parse(localStorage.getItem("user") as string);

type State = {
  validations: Validation[];
  validation: Validation | null;
  isLoadingValidations: boolean;
  isSubmiting: boolean;
  isSubmited: boolean;
  errors: any | null;
};

type Validation = {
  id: number,
  user: {
    id: number
    email: string
    first_name: string
    last_name: string
    picture: string
  },
  result: {
    passed_validation: boolean,
    percentages_plot: object
  }
};

export type Filter = {
  date: string | null
}

export const useValidationsStore = defineStore({
  id: "validations",
  state: (): State => ({
    validations: [],
    validation: null,
    isLoadingValidations: false,
    isSubmiting: false,
    isSubmited: false,
    errors: null,
  }),
  actions: {
    getValidations(filter?: Filter) {
      this.isLoadingValidations = true;
      connector
        .get("/api/validation-entries", {
          params: filter,
          headers: {
            Authorization: `Bearer ${user.token}`,
          },
        })
        .then((validations) => (this.validations = validations.data.data))
        .catch((error: any) => {
          this.errors = error;
          this.isLoadingValidations = false;
        })
        .finally(() => {
          this.isLoadingValidations = false;
        });
    },
    add(
      title: string,
      file: string,
      referenceColumn: string,
      separator: string
    ) {
      this.isSubmiting = true;
      var bodyFormData = new FormData();
      bodyFormData.append("title", title);
      bodyFormData.append("file", file[0]);
      bodyFormData.append("reference_column", referenceColumn);
      if (separator) {
        bodyFormData.append("separator", separator);
      }

      connector.post(`/api/file-upload`, bodyFormData, {
        headers: {
          Authorization: `Bearer ${user.token}`,
          "Content-Type": `multipart/form-data; boundary=${bodyFormData._boundary}`,
        },
      })
      .then((response) => {
        this.validations.unshift(response.data.data);
        this.isSubmiting = false;
        this.isSubmited = true;
      })
      .catch((error: any) => {
        this.errors = error;
        this.isSubmiting = false;
        this.isSubmited = false;
      })
    },
  },
});
