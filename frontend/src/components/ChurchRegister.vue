<template>
  <form @submit.prevent="submitForm">
    <div class="form-group row">
      <input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Church Name"
        v-model="church.church_name"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Pastor Name"
        v-model="church.pastor_name"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Church Address"
        v-model="church.church_address"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Church Number"
        v-model="church.church_number"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Email Address"
        v-model="church.email_address"
      /><button class="btn btn-success">Submit</button>
    </div>
  </form>

  <h1>List of Churches:</h1>
  <table class="table">
    <thead>
      <tr>
        <th>Church Name</th>
        <th>Address</th>
        <th>Pastor</th>
        <th>Phone Number</th>
        <th>Email</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="church in churches"
        :key="church.id"
        @dblclick="$data.church = church"
      >
        <td>{{ church.church_name }}</td>
        <td>{{ church.church_address }}</td>
        <td>{{ church.pastor_name }}</td>
        <td>{{ church.church_number }}</td>
        <td>{{ church.email_address }}</td>
        <td>
          <button
            class="btn btn-outline-danger btn-sm mx-1"
            @click="deleteChurch(church)"
          >
            x
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import axios from "axios";
export default {
  name: "ChurchRegister",
  data() {
    return {
      church: {},
      churches: [],
    };
  },
  async created() {
    await this.getChurches();
  },

  methods: {
    async submitForm() {
      if (this.church.id === undefined) {
        await this.createChurch();
      } else {
        await this.editChurch();
      }
    },
    async getChurches() {
      var response = await fetch("http://127.0.0.1:8000/church/");
      this.churches = await response.json();
    },
    async createChurch() {
      await this.getChurches();
      await axios.post("http://127.0.0.1:8000/churchpost/", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(this.church),
      });
      await this.getChurches();
    },
    async editChurch() {
      await this.getChurches();
      await fetch(`http://127.0.0.1:8000/church/${this.church.id}/`, {
        method: "PUT",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(this.church),
      });
      await this.getChurches();
      this.church = {};
    },
    async deleteChurch(church) {
      await this.getChurches();
      await fetch(`http://127.0.0.1:8000/church/${church.id}/`, {
        method: "delete",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(this.church),
      });
      await this.getChurches();
    },
  },
};
</script>
