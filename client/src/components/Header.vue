<template>
    <!--HEADER-->
    <header id="top-head" class="uk-position-fixed">
        <div class="uk-container uk-container-expand uk-background-primary">
            <nav class="uk-navbar uk-light" data-uk-navbar="mode:click; duration: 250">
                <div class="uk-navbar-left">
                    <div class="uk-navbar-item uk-hidden@s">
                        <a class="uk-logo" href="#"><img class="custom-logo" src="/img/logo.png" alt="" /></a>
                    </div>
                    <ul class="uk-navbar-nav uk-hidden@s" v-for="(route, index) in routes" :key="index">
                        <li>
                            <router-link :to="route.path"> {{ route.name }}</router-link>
                        </li>
                    </ul>
                </div>
                <div class="uk-navbar-right">
                    <ul class="uk-navbar-nav uk-visible@s" v-for="(route, index) in routes" :key="index">
                        <li>
                            <router-link :to="route.path"> {{ route.name }}</router-link>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    </header>
    <!--/HEADER-->
</template>

<script>
export default {
    name: "Header",
    components: {},
    computed: {
        routes() {
            return this.$router.options.routes;
        },
    },
};
</script>
