<template>
  <form @submit.prevent="submitForm">
    <div class="form-group row">
      <input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Missionary Name"
        v-model="missionary.missionary_name"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Email Address"
        v-model="missionary.email_address"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Phone Number"
        v-model="missionary.phone_number"
      /><input
        type="text"
        class="form-control col-3 mx-2"
        placeholder="Field of Service"
        v-model="missionary.field_of_service"
      /><button class="btn btn-success">Submit</button>
    </div>
  </form>

  <h1>List of Missionaries:</h1>
  <table class="table">
    <thead>
      <tr>
        <th>Missionary Name</th>
        <th>Email Address</th>
        <th>Phone Number</th>
        <th>Field of Service</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="missionary in missionaries"
        :key="missionary.id"
        @dblclick="$data.missionary = missionary"
      >
        <td>{{ missionary.missionary_name }}</td>
        <td>{{ missionary.email_address }}</td>
        <td>{{ missionary.phone_number }}</td>
        <td>{{ missionary.field_of_service }}</td>
        <td>
          <button
            class="btn btn-outline-danger btn-sm mx-1"
            @click="deleteMissionary(missionary)"
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
  name: "MissionaryRegister",
  data() {
    return {
      missionary: {},
      missionaries: [],
    };
  },
  async created() {
    await this.getMissionaries();
  },

  methods: {
    async submitForm() {
      if (this.missionary.id === undefined) {
        await this.createMissionary();
      } else {
        await this.editMissionary();
      }
    },
    async getMissionaries() {
      var response = await fetch("http://127.0.0.1:8000/missionary/");
      this.missionaries = await response.json();
    },
    async createMissionary() {
      await this.getMissionaries();
      await fetch("http://127.0.0.1:8000/missionary/", {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(this.missionary),
      });
      await this.getMissionaries();
    },
    async editMissionary() {
      await this.getMissionaries();
      await fetch(`http://127.0.0.1:8000/missionary/${this.missionary.id}/`, {
        method: "PUT",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(this.missionary),
      });
      await this.getMissionaries();
      this.missionary = {};
    },
    async deleteMissionary(missionary) {
      await this.getMissionaries();
      await fetch(`http://127.0.0.1:8000/missionary/${missionary.id}/`, {
        method: "delete",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify(this.missionary),
      });
      await this.getMissionaries();
    },
  },
};
</script>
