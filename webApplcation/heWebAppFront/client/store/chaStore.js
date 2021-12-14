import { chaData } from "@@/data/chaData";

export const state = () => ({
	chaData,
	selectedData: {
		age: 0,
		sex: 1,
		chf: 0,
		hyper: 0,
		stroke: 0,
		vascular: 0,
		diabetes: 0,
	},
});

export const mutations = {
	setSelectedChaData(state, { name, idx }) {
		state.chaData[name].columns.map((data, idx) => {
			data.selected = false;
			return data;
		});
		state.chaData[name].columns[idx].selected =
			!state.chaData[name].columns[idx].selected;
	},
	addData(state, { name, point }) {
		state.selectedData[name] = point;
	},
};

export const getters = {
	getChaData: (state) => {
		return state.chaData;
	},
	getSelectedData: (state) => {
		return state.selectedData;
	},
	getSelectedPoint: (state) => {
		return Object.values(state.selectedData);
	},
};
