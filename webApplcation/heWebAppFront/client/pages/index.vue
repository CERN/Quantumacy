<template>
  <!--  v-if="!isLoading"-->
  <v-container fluid style="max-width: 700px">
    <QuestionComponent v-for="(datum, idx) in data" :key="idx" :data="datum" />
    <v-row>
      <v-col>
        <v-tooltip top>
          <template #activator="{ on, attrs }">
            <v-btn
              :loading="isLoading"
              rounded
              x-large
              block
              elevation="24"
              depressed
              v-bind="attrs"
              v-on="on"
              @click="calcFunc"
            >
              <div>
                <v-icon>mdi-calculator</v-icon>
                &nbsp;Run Homomorphic Encryption Operation
              </div>
            </v-btn>
          </template>
          <span>Start homomorphic encryption operation with the server. </span>
        </v-tooltip>
      </v-col>
    </v-row>
    <v-row align="center" justify="space-around">
      <v-col>
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-btn
              :loading="isLoading"
              block
              v-bind="attrs"
              prominent
              class="text-center rounded-pill"
              v-on="on"
            >
              <!--						<v-btn block text v-bind="attrs" v-on="on">-->
              <v-icon>mdi-message-reply-text-outline</v-icon>
              <span class="text--disabled">
								&nbsp;&nbsp;{{ resultMessage }} &nbsp;
							</span>
              <strong
                class="
									purple--text
									accent-3
									font-weight-black font-italic
									text-decoration-underline
								"
              >{{ resultValue }}</strong
              >
            </v-btn>
          </template>
          <span>Result of homomorphic encryption operation</span>
        </v-tooltip>
      </v-col>
    </v-row>
    <ResultComponent v-if="!isLoading" :result="result" />
    <v-container v-else fluid>
      <v-row>
        <v-col>
          <v-progress-linear
            indeterminate
            background-color="pink lighten-3"
            color="pink lighten-1"
            stream
          ></v-progress-linear>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
  <!--	<v-container v-else> loading {{ isLoading }}</v-container>-->
</template>

<script>
import QuestionComponent from "@/components/QuestionComponent";
import { mapGetters } from "vuex";
import { chaData } from "@@/data/chaData";
import SEAL from "node-seal";

export default {
  name: "ChaPage",
  components: {
    QuestionComponent
  },
  async asyncData() {
    const seal = await SEAL();
    const schemeType = seal.SchemeType.ckks;
    const securityLevel = seal.SecurityLevel.tc128;
    const polyModulusDegree = 4096;
    const bitSizes = [36, 36, 37];
    const bitSize = 20;
    const params = seal.EncryptionParameters(schemeType);
    params.setPolyModulusDegree(polyModulusDegree);

    params.setCoeffModulus(
      seal.CoeffModulus.Create(polyModulusDegree, Int32Array.from(bitSizes))
    );
    return {
      seal,
      isLoading: false,
      schemeType,
      securityLevel,
      polyModulusDegree,
      bitSizes,
      bitSize,
      params
    };
  },

  data() {
    return {
      data: chaData,
      seal: {},
      schemeType: {},
      securityLevel: "",
      polyModulusDegree: [],
      bitSizes: [],
      bitSize: 20,
      params: {},
      isLoading: true,
      result: 1,
      resultMessage: "The Calculated Homomorphic result result is ",
      homomorphicResult: 1
    };
  },

  computed: {
    ...mapGetters({
      getSelectedData: "chaStore/getSelectedData",
      getSelectedPoint: "chaStore/getSelectedPoint",
      getSeal: "sealStore/getSeal"
    }),
    resultValue() {
      return parseFloat(this.homomorphicResult).toFixed(4);
    }
  },

  mounted() {
  },
  methods: {
    async calcFunc() {
      this.isLoading = true;

      // make context
      const sealContext = await this.seal.Context(
        this.params,
        true,
        this.securityLevel
      );
      const keyGenerator = this.seal.KeyGenerator(sealContext);
      const publicKey = keyGenerator.createPublicKey();

      // operations
      const encoder = this.seal.CKKSEncoder(sealContext);
      const encryptor = this.seal.Encryptor(sealContext, publicKey);
      const selectedData = Object.values(this.getSelectedData).map((data) => {
        return [data];
      });
      const data = selectedData.map((dd) => {
        return Float64Array.from(dd);
      });

      // preprocess of data before send
      const sendingPlainTexts = data.map((d) => {
        return encoder.encode(d, Math.pow(2, 20));
      });
      const sendingCipherTexts = sendingPlainTexts.map((d) => {
        return encryptor.encrypt(d);
      });
      const sendingData = sendingCipherTexts.map((d) => {
        return d.save();
      });
      // console.log(sendingData[0]);
      // TODO change hard coding
      const operateResult = await this.$axios
        // .post("http://localhost:3030/homomorphic/chaData", {
        .post(process.env.HOMOMORPHIC_BACKEND, {
          chaData: {
            schemeType: "ckks",
            securityLevel: 128,
            polyModulusDegree: 4096,
            bitSizes: [36, 36, 37],
            bitSize: 20,
            selectedData: sendingData
          }
        })
        .then(({ data }) => {
          return data.result;
        })
        .catch((err) => {
          return err;
        });
      // restore
      const secretKey = keyGenerator.secretKey();
      const decryptor = this.seal.Decryptor(sealContext, secretKey);
      const receivedData = this.seal.CipherText();
      receivedData.load(sealContext, operateResult);
      const resultPlainText = decryptor.decrypt(receivedData);
      const result = encoder.decode(resultPlainText);
      const homomorphicResult = Math.round(result[0]);
      this.homomorphicResult = result[0];
      this.result = homomorphicResult;
      this.isLoading = false;
    }
  }
};
</script>

<style scoped></style>
