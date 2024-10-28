<template>
  <form @submit.prevent="submitForm">
    <div class="form-group row">
      <input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Church Name"
        v-model="church['Church Name']"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Church Address"
        v-model="church['Church Address']"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Pastor Name"
        v-model="church['Pastor Name']"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Church Number"
        v-model="church['Church Number']"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Email Address"
        v-model="church['Email Address']"
      /><button class="btn btn-success">Submit</button>
    </div>
  </form>

  <h1>List of Churches:</h1>
  <table class="table">
    <thead>
      <th>Church Name</th>
      <th>Address</th>
      <th>Pastor</th>
      <th>Phone #</th>
      <th>Email</th>
    </thead>
    <tbody>
      <tr
        v-for="church in churches"
        :key="church.id"
        @dblclick="$data.church = churches"
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
export default {
  name: "App",
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
    submitForm() {
      if (this.church.id === undefined) {
        this.createChurch();
      } else {
        this.editChurch();
      }
    },
    async getChurches() {
      var response = await fetch(
        "http://127.0.0.1:8000/baseapp/routers/church/"
      );
      this.churches = await response.json();
    },
    async createChurch() {
      await this.getChurches();
      await fetch("http://127.0.0.1:8000/baseapp/routers/church/", {
        method: "post",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(this.church),
      });
      await this.getChurches();
    },
    async editChurch() {
      await this.getChurches();
      await fetch(
        `http://127.0.0.1:8000/baseapp/routers/church/${this.church.id}/`,
        {
          method: "POST",
          headers: {
            "Content-type": "application/json",
          },
          body: JSON.stringify(this.church),
        }
      );
      await this.getChurches();
      this.church = {};
    },
    async deleteChurch(church) {
      await this.getChurches();
      await fetch(
        `http://127.0.0.1:8000/baseapp/routers/church/${church.id}/`,
        {
          method: "delete",
          headers: {
            "Content-type": "application/json",
          },
          body: JSON.stringify(this.church),
        }
      );
      await this.getChurches();
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
