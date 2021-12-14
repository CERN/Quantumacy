<template>
	<v-sheet shaped class="mx-auto" style="margin-top: 20px">
		<v-container fluid>
			<v-row>
				<v-col>
					<v-card class="mx-auto">
						<v-card-title>
							<span>
								<strong style="font-size: 1.75rem"> {{ result }} </strong>
								points
							</span>
						</v-card-title>
						<v-card-text>
							<v-container>
								<v-row>
									<v-col cols="12">
										Stroke risk was
										<span style="color: red">
											{{ resultTable[result]["result00"] }}%
										</span>
										per year in >90,000 patients (the Swedish Atrial
										Fibrillation Cohort Study) and
										<span style="color: red">
											{{ resultTable[result]["result01"] }}%
										</span>
										risk of stroke/TIA/systemic embolism.
									</v-col>
								</v-row>
								<v-row>
									<v-col v-if="result === 8" cols="12">
										We realize that 8 points showed a lower risk than 7 points,
										these were the findings in the study, obviously one should
										assume all scores ≥7 have a risk >10%.
									</v-col>
								</v-row>
								<v-row>
									<v-col cols="12">
										One recommendation suggests a 0 score is “low” risk and may
										not require anticoagulation; a 1 score is “low-moderate”
										risk and should consider antiplatelet or anticoagulation,
										and score 2 or greater is “moderate-high” risk and should
										otherwise be an anticoagulation candidate.
									</v-col>
								</v-row>
							</v-container>
						</v-card-text>
					</v-card>
				</v-col>
			</v-row>
		</v-container>
	</v-sheet>
</template>

<script>
import { resultTable } from "@@/data/resultTable";

export default {
	name: "ResultComponent",
	props: {
		result: {
			type: Number,
			default: () => {
				return 1;
			},
		},
	},
	data() {
		return {
			resultTable,
		};
	},
};
</script>

<style scoped></style>
