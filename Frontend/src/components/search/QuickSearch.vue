<template>
  <div class="quick-search">
    <div class="search-input-wrapper">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Quick search..."
        @keyup.enter="handleSearch"
      />
      <div class="search-icon">
        <i class="fas fa-search"></i>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuickSearch",
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({
          path: "/searchpage",
          query: { q: this.searchQuery },
        });
        this.searchQuery = "";
      }
    },
  },
};
</script>

<style scoped>
.quick-search {
  position: relative;
  width: 300px;
}

.search-input-wrapper {
  position: relative;
}

.search-input-wrapper input {
  width: 100%;
  padding: 8px 32px 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
}

.search-input-wrapper input:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.1);
}

.search-icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  pointer-events: none;
}
</style>
