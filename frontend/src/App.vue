<script setup>
import ChurchRegister from "./components/ChurchRegister.vue";
import MissionaryRegister from "./components/MissionaryRegister.vue";
</script>

<template>
  <ChurchRegister />
  <MissionaryRegister />
</template>

<script>
export default {
  name: "App",
  components: {
    ChurchRegister,
    MissionaryRegister,
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
