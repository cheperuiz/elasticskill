<template>
  <v-card flat class="ma-8 pa-8">
    <v-toolbar prominent flat color="rgba(0,0,0,0)" class="mb-8">
      <v-icon class="display-4 ma-4">mdi-tag-multiple</v-icon>
      <v-toolbar-title class="display-4">Tags:</v-toolbar-title>
    </v-toolbar>
    <v-row>
      <v-combobox
        v-model="chips"
        :items="items"
        chips
        clearable
        label="Search for any topic..."
        multiple
        prepend-icon="mdi-filter-variant"
        solo
        class="mx-8"
      >
        <template v-slot:selection="{ attrs, item, select, selected }">
          <v-chip
            v-bind="attrs"
            :input-value="selected"
            close
            @click="select"
            @click:close="remove(item)"
            class="ma-2"
          >
            <strong>{{ item }}</strong>&nbsp;
          </v-chip>
        </template>
      </v-combobox>
      <v-checkbox @change="chips=[...chips]" v-model="and" label="Include all (AND)"></v-checkbox>
    </v-row>
    <v-toolbar color="rgba(0,0,0,0)" flat>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-row justify="space-around">
      <v-card outlined class="ma-2" max-width="45%">
        <v-list-item>
          <v-card-title class="display-1">Projects & Tasks:</v-card-title>
          <v-spacer></v-spacer>
          <v-avatar>
            <v-icon class="display-1">mdi-account-clock</v-icon>
          </v-avatar>
        </v-list-item>
        <v-container>
          <v-chip
            @click="add(tag.term)"
            :color="colorFor(tag,tasksColors)"
            v-for="tag in tasksTags"
            :key="tag.term"
          >
            <strong>{{tag.term}}</strong>
          </v-chip>
        </v-container>
      </v-card>
      <v-card outlined class="ma-2" max-width="45%">
        <v-list-item>
          <v-card-title class="display-1">Discussions:</v-card-title>
          <v-spacer></v-spacer>
          <v-avatar>
            <v-icon class="display-1">mdi-forum</v-icon>
          </v-avatar>
        </v-list-item>
        <v-container>
          <v-chip
            @click="add(tag.term)"
            :color="colorFor(tag,threadsColors)"
            v-for="tag in threadsTags"
            :key="tag.term"
          >
            <strong>{{tag.term}}</strong>
          </v-chip>
        </v-container>
      </v-card>
    </v-row>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      and: false,
      chips: [],
      items: [],
      pagesize: 50,
      offset: 0,
      tasksTags: null,
      tasksColors: [20, 10],
      threadsColors: [100, 50]
    };
  },
  watch: {
    chips: async function() {
      const params = {
        keywords: this.chips,
        limit: this.pagesize,
        skip: this.offset,
        operator: this.operator
      };
      const tasksTags = await this.fetchTags("tasks", params);
      const threadsTags = await this.fetchTags("threads", params);
      this.tasksTags = tasksTags;
      this.threadsTags = threadsTags;
    }
  },
  computed: {
    operator() {
      return !!this.and ? "and" : "or";
    }
  },
  async asyncData({ app, params }) {
    const offset = 0;
    const pagesize = 50;

    const { data: tasksResp } = await app.$axios.get(`/tags/tasks`, {
      params: { skip: offset, limit: pagesize }
    });
    const { data: threadsResp } = await app.$axios.get(`/tags/threads`, {
      params: { skip: offset, limit: pagesize }
    });
    const tasksTags = tasksResp.data.values;
    const threadsTags = threadsResp.data.values;
    return {
      tasksTags,
      threadsTags
    };
  },
  methods: {
    remove(item) {
      this.chips.splice(this.chips.indexOf(item), 1);
      this.chips = [...this.chips];
    },
    add(item) {
      if (this.chips.indexOf(item) >= 0) return;
      this.chips.push(item);
      this.chips = [...this.chips];
    },
    async fetchTags(index, params) {
      const url = `/tags/${index}`;
      const { data: resp } = await this.$axios.get(url, {
        params: {
          keywords: params.keywords.join(","),
          limit: params.limit,
          skip: params.skip,
          operator: params.operator
        }
      });
      console.log(params.operator);
      return resp.data.values;
    },
    colorFor(item, colors) {
      if (item.term_freq >= colors[0]) return "light-green";
      if (item.term_freq >= colors[1]) return "orange";
      return "secondary";
    }
  }
};
</script>

<style>
</style>