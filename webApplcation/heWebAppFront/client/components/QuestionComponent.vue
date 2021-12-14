<template>
	<v-row align="center" no-gutters>
		<v-col cols="12" sm="6">
			<v-container>
				<v-row no-gutters>
					<v-col>
						{{ data.text }}
					</v-col>
				</v-row>
			</v-container>
			<v-divider />
		</v-col>
		<v-divider vertical />
		<v-col cols="12" sm="6">
			<v-container>
				<v-row no-gutters>
					<v-col
						v-for="(datum, idx) in data.columns"
						:key="datum.name"
						class="text-center"
						cols="12"
						:sm="12 / data.columns.length"
					>
						<v-hover v-slot="{ hover }">
							<v-card
								class="mx-auto"
								:elevation="hover ? 16 : 2"
								:class="[{ selected: datum.selected }, { onHover: hover }]"
								@click="updateData({ datum, name: data.name, idx })"
							>
								{{ datum.text }}
							</v-card>
						</v-hover>
					</v-col>
				</v-row>
			</v-container>
			<v-divider />
		</v-col>
	</v-row>
</template>

<script>
import { mapGetters } from "vuex";

export default {
	name: "QuestionComponent",
	props: {
		data: {
			type: Object,
			default: () => {
				return {};
			},
		},
		idx: {
			type: Number,
			default: () => {
				return 0;
			},
		},
	},
	data() {
		return {
			selected: true,
			selectedColumn: {},
		};
	},
	computed: {
		selectedData() {
			return this.$store.state.chaStore.selectedData;
		},
		...mapGetters({
			getSelectedPoint: "chaStore/getSelectedPoint",
		}),
	},
	beforeMount() {},
	mounted() {},

	methods: {
		updateData({ datum, name, idx }) {
			this.$store.commit("chaStore/setSelectedChaData", { name, idx });
			this.$store.commit("chaStore/addData", {
				name,
				point: datum.point,
			});
		},
	},
};
</script>

<style scoped>
.offHover {
	background-color: yellowgreen;
}

.selected {
	background-color: darkred;
}

.onHover {
	background-color: red;
}
</style>
