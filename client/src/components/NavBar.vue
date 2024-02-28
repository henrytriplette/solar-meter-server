<template>
  <ul
    class="uk-nav uk-nav-default uk-nav-parent-icon"
    data-uk-nav
    v-for="(route, index) in routes"
    :key="index"
  >
    <li v-if="route.children" class="uk-parent">
      <a href="#"
        ><span
          data-uk-icon="icon: thumbnails"
          class="uk-margin-small-right"
        ></span
        >{{ route.name }}</a
      >
      <ul class="uk-nav-sub">
        <li v-for="child in route.children">
          <router-link :to="{ name: child.name }">
            <span
              data-uk-icon="icon: album"
              class="uk-margin-small-right"
            ></span>
            {{ child.name }}
          </router-link>
        </li>
      </ul>
    </li>
    <li v-else>
      <router-link :to="route.path"> {{ route.name }}</router-link>
    </li>
  </ul>
</template>

<script>
export default {
  name: "Menu",
  components: {},
  computed: {
    routes() {
      return this.$router.options.routes;
    },
  },
};
</script>
