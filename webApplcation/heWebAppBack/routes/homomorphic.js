const express = require("express");
const router = express.Router();
// import SEAL from "node-seal";
const SEAL = require("node-seal");
let { PythonShell } = require("python-shell");
/* GET users listing. */
router.get("/", (req, res) => {
	try {
		console.log("??");
		return res.status(200).json({ homomorphic });
	} catch (e) {
		return res.status(500).json({ error: e });
	}
});

router.post("/chaData", async (req, res, next) => {
	try {
		const seal = await SEAL();

		const { chaData } = req.body;
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
		const sealContext = await seal.Context(params, true, securityLevel);

		const evaluator = seal.Evaluator(sealContext);
		const receivedData = chaData.selectedData.map((data) => {
			const t = seal.CipherText();
			t.load(sealContext, data);
			return t;
		});
		const resultCipher = receivedData[0];
		for (let i = 1; i < receivedData.length; i++) {
			evaluator.add(receivedData[i], resultCipher, resultCipher);
		}
		const result = resultCipher.save();

		return res.status(200).json({ result });
	} catch (e) {
		return res.status(500).json({
			error: e,
			message: "[ERROR]\t:\tcha Data error",
		});
	}
});

module.exports = router;
