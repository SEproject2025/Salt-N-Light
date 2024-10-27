<template>
  <table class="table">
    <thead>
      <th>Church Name</th>
      <th>Address</th>
      <th>Pastor</th>
      <th>Phone #</th>
      <th>Email</th>
    </thead>
    <tbody>
      <tr v-for="church in churches" :key="church.id">
        <td>{{ church.church_name }}</td>
        <td>{{ church.church_address }}</td>
        <td>{{ church.pastor_name }}</td>
        <td>{{ church.church_number }}</td>
        <td>{{ church.email_address }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      churches: [],
    };
  },
  async created() {
    var response = await fetch("http://127.0.0.1:8000/baseapp/routers/church/");
    this.churches = await response.json();
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
