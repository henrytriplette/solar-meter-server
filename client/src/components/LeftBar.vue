<template>
  <!-- LEFT BAR -->
  <aside id="left-col" class="uk-light uk-visible@s">
    <div class="left-logo uk-flex uk-flex-middle">
      <img class="custom-logo" src="/img/logo.png" alt="" />
    </div>

    <div class="left-content-box content-box-dark">
      <UserBar />
    </div>

    <div class="left-nav-wrap">
      <NavBar />
    </div>
  </aside>
  <!-- /LEFT BAR -->
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import UserBar from "@/components/UserBar.vue";

export default {
  components: {
    NavBar,
    UserBar,
  },
};
</script>
