export const state = () => ({
  chaData: {},
});

export const mutations = {
  mutationA(state, { data1, data2 }) {},
};

export const actions = {
  actionsA({ rootState, state, dispatch, commit }, payload) {},
};

export const getters = {};

// 각각 컴포넌트 (dispatch)--> actions (commit)--> mutations (state)--> state -->모든 컴포넌트에서 활용
