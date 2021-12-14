import SEAL from "node-seal";

export const state = () => ({
	seal: {},
	schemeType: "scheme Type",
	securityLevel: "",
	polyModulusDegree: 4096,
	bitSizes: [36, 36, 37],
	scale: 20, // bitSize
	params: {},
	encoder: "",
	keyGenerator: "",
	publicKey: "",
	secretKey: "",
	encryptor: "",
	decryptor: "",
	evaluator: "",
});

export const actions = {
	async createSeal({ commit }) {
		try {
			const seal = await SEAL();
			await commit("setSeal", seal);
			return seal;
		} catch (e) {
			// console.log(e);
		}
	},
	async createScheme({ commit }, seal) {
		try {
			// const scheme = seal.SchemeType.ckks
			const scheme = await commit("setSchemeType", seal);
			// console.log("create schemebb", scheme, "UU");
			return scheme;
		} catch (e) {
			// console.log(e);
		}
	},
};
export const mutations = {
	setSeal(state, seal) {
		state.seal = seal;
		return state.seal;
	},
	setSchemeType(state, schemeType) {
		state.schemeType = schemeType;
		return state.schemeType;
	},
	setSecurityLevel(state) {
		state.securityLevel = state.seal.SecurityLevel.tc128;
		return state.securityLevel;
	},
	setPolyModulusDegree(state, degree) {
		state.polyModulusDegree = degree;
		return state.polyModulusDegree;
	},
	setBitSizes(state, bitSizes) {
		state.bitSizes = bitSizes;
		return state.bitSizes;
	},
	setParams(state, params) {
		state.params = params;
		return state.params;
	},
	setContext(state, { context }) {
		state.context = context;
		return context;
	},

	setEncoder(state, payload) {
		state.encoder = payload.encoder;
	},
	setKeyGenerator(state, { keyGenerator }) {
		state.keyGenerator = keyGenerator;
	},
	setKeys(state) {
		state.publicKey = state.keyGenerator.createPublicKey();
		state.secretKey = state.keyGenerator.secretKey();
	},
	setOperators(state, { seal, context, publicKey }) {
		// console.log("op", seal);
		// console.log(context, publicKey);
	},
};

export const getters = {
	getSeal: (state) => {
		return state.seal;
	},
	getSchemeType: (state) => {
		return state.schemeType;
	},
	getPolyModulusDegree(state) {
		return state.polyModulusDegree;
	},
	getBitSizes(state) {
		return state.bitSizes;
	},
	getBitScale(state) {
		return state.scale;
	},

	getSecurityLevel: (state) => {
		return state.securityLevel;
	},
	getParams(state) {
		return state.params;
	},
	getContext: (state) => {
		return state.context;
	},
	getEncoder(state) {
		return state.encoder;
	},
	getKeyGenerator(state) {
		return state.keyGenerator;
	},
	getPublicKey(state) {
		return state.publicKey;
	},
	getSecretKey(state) {
		return state.secretKey;
	},
};
