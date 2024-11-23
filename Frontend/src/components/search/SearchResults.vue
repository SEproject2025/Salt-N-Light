<template>
  <div class="search-results">
    <p v-if="!results.length">No results found.</p>
    <ul v-else>
      <li v-for="result in results" :key="result.id">
        <h4>{{ result.email }}</h4>
        <p>{{ result.user_type }} - {{ result.phone_number }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SearchResults",
  props: {
    results: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.search-results {
  padding: 10px;
}
</style>
