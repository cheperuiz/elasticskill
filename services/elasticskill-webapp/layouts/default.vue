<template>
  <v-app dark>
    <v-app-bar :clipped-left="true" fixed app>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>ElasticSkill</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer :fixed="true" app>
      <span>&copy; 2020</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {};
  }
};
</script>
