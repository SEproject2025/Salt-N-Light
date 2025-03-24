<template>
  <div>
    <div
      v-for="(tag, index) in tags"
      :key="index"
      class="chip"
      :style="{ backgroundColor: '#f55d25', color: 'black' }"
      :title="tag.description || 'No description available'"
    >
      <div class="chip-label">{{ tag.tag_name }}</div>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios.js";

export default {
  data() {
    return {
      tags: [],
    };
  },
  created() {
    this.fetchTags();
  },
  methods: {
    async fetchTags() {
      try {
        const response = await api.get("tag/");
        this.tags = response.data;
      } catch (error) {
        console.error("There was an error fetching the tags:", error);
      }
    },
  },
};
</script>

<style scoped>
.chip {
  font-family: -apple-system, SF UI Text, Helvetica Neue, Helvetica, Arial,
    sans-serif;
  -webkit-text-size-adjust: 100%;
  list-style: none;
  white-space: normal !important;
  -webkit-tap-highlight-color: transparent;
  font-size: 14px;
  font-weight: 400;
  background: rgba(0, 0, 0, 0.37);
  height: 23px;
  line-height: 23px;
  border-radius: 5px;
  padding: 0 6px;
  box-sizing: border-box;
  vertical-align: middle;
  display: inline-flex;
  -webkit-box-align: center;
  align-items: center;
  margin: 2px 0;
  background-color: #ac648d;
  color: white;
}

.chip:hover {
  background-color: #f55d25;
}

.chip-label {
  margin-right: 8px;
}
</style>
