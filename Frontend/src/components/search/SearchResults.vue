<template>
  <div class="search-results">
    <p v-if="!results.length">No results found.</p>
    <div v-else class="results-grid">
      <UserCard
        v-for="result in results"
        :key="result.id"
        :id="result.id"
        :first_name="result.first_name"
        :last_name="result.last_name"
        :city="result.city"
        :state="result.state"
        :country="result.country"
        :description="result.description"
        :tags="result.tags"
        :user_type="result.user_type"
      />
    </div>
  </div>
</template>

<script>
import UserCard from "./UserCard.vue";

export default {
  name: "SearchResults",
  components: {
    UserCard,
  },
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
  padding: 20px;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>
