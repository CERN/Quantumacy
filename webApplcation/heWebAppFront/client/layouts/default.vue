<template>
  <v-app dark>
    <v-app-bar fixed app>
      <v-icon color="darken-2"> mdi-domain</v-icon>
      <v-toolbar-title class="text-center" v-text="title" />
      <v-spacer />
      <a href="https://home.cern/science/computing/cern-openlab">
        <v-avatar>
          <!--        <img :src="require('@/static/snubh_logo.png')" alt="" />-->
          <img :src=cernImage alt="" />
        </v-avatar>
      </a>
    </v-app-bar>

    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>

    <v-footer :absolute="true" app padless>
      <v-col class="text-center">
				<span
        >&copy; {{ new Date().getFullYear() }} all copyrights reserved by
					Hanyul Ryu</span
        >
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      title: "Homomorphic Encryption with Medical Data",
      cernImage: require("../static/LogoOutline_small-White.png")
    };
  }
};
</script>
