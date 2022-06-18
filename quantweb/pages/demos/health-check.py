#
# Cardiovascular risk assessment in adults (ACC/AHA 2013)
#

# Define program
import sys
import getopt
import pickle
from math import log, sqrt, exp
from eva import *

# Load values
try:
  opts, args = getopt.getopt(sys.argv[1:], "he:x:a:t:l:s:m:k:d:", ["help", "eth=", "sex=", "age=", "tc=", "hdl=", "syst=", "meds=", "smoke=", "diab="])
except:
  print("Invalid input parameters")
  sys.exit(2)

for opt, arg in opts:
  if opt in ("-h", "--help"):
    print("{0} -e <ethnicity> -x <sex> -a <age> -t <total cholesterol> -h <HDL cholesterol> -s <systolic pressure> -m <pressure meds?> -k <smoker?> -d <diabetes?>".format(sys.argv[0]))
    sys.exit(2)
  elif opt in ("-e", "--eth"):
    arg_ethnicity = arg
  elif opt in ("-x", "--sex"):
    arg_sex = arg
  elif opt in ("-a", "--age"):
    arg_age = int(arg)
  elif opt in ("-t", "--tc"):
    arg_tot_chol = int(arg)
  elif opt in ("-l", "--hdl"):
    arg_hdl = int(arg)
  elif opt in ("-s", "--syst"):
    arg_systolic = int(arg)
  elif opt in ("-m", "--meds"):
    arg_meds = int(arg)
  elif opt in ("-k", "--smoke"):
    arg_smoke = int(arg)
  elif opt in ("-d", "--diab"):
    arg_diabetes = int(arg)

# Coefficients
# Black or African American female patients
if (arg_ethnicity == "African-American") and (arg_sex == "Female"):
  CAge = 17.114
  CSqAge = 0
  CTotalChol = 0.94
  CAgeTotalChol = 0
  CHDLChol = -18.92
  CAgeHDLChol = 4.475
  COnHypertensionMeds = 29.291
  CAgeOnHypertensionMeds = -6.432
  COffHypertensionMeds = 27.82
  CAgeOffHypertensionMeds = -6.087
  CSmoker = 0.691
  CAgeSmoker = 0
  CDiabetes = 0.874
  S10 = 0.9533
  MeanTerms = 86.61
elif (arg_ethnicity == "African-American") and (arg_sex == "Male"):
  CAge = 2.469
  CSqAge = 0
  CTotalChol = 0.302
  CAgeTotalChol = 0
  CHDLChol = -0.307
  CAgeHDLChol = 0
  COnHypertensionMeds = 1.916
  CAgeOnHypertensionMeds = 0
  COffHypertensionMeds = 1.809
  CAgeOffHypertensionMeds = 0
  CSmoker = 0.549
  CAgeSmoker = 0
  CDiabetes = 0.645
  S10 = 0.8954
  MeanTerms = 19.54
elif (arg_ethnicity == "White" or arg_ethnicity == "Other") and (arg_sex == "Female"):
  CAge = -29.799
  CSqAge = 4.884
  CTotalChol = 13.54
  CAgeTotalChol = -3.114
  CHDLChol = -13.578
  CAgeHDLChol = 3.149
  COnHypertensionMeds = 2.019
  CAgeOnHypertensionMeds = 0
  COffHypertensionMeds = 1.957
  CAgeOffHypertensionMeds = 0
  CSmoker = 7.574
  CAgeSmoker = -1.665
  CDiabetes = 0.661
  S10 = 0.9665
  MeanTerms = -29.18
elif (arg_ethnicity == "White" or arg_ethnicity == "Other") and (arg_sex == "Male"):
  CAge = 12.344
  CSqAge = 0
  CTotalChol = 11.853
  CAgeTotalChol = -2.664
  CHDLChol = -7.99
  CAgeHDLChol = 1.769
  COnHypertensionMeds = 1.797
  CAgeOnHypertensionMeds = 0
  COffHypertensionMeds = 1.764
  CAgeOffHypertensionMeds = 0
  CSmoker = 7.837
  CAgeSmoker = -1.795
  CDiabetes = 0.658
  S10 = 0.9144
  MeanTerms = 61.18

# Define formula

# Terms =  (C_Age * ln(Age)) + (C_Sq_Age * sq(ln(Age))) + (C_Total_Chol * ln(Total_cholesterol)) + (C_Age_Total_Chol * ln(Age) * ln(Total_cholesterol))
#  + (C_HDL_Chol * ln(HDL_cholesterol)) + (C_Age_HDL_Chol * ln(Age) * ln(HDL_cholesterol)) +
# (Do you take blood pressure medication? * C_Do you take blood pressure medication?s * ln(Systolic blood pressure)) + 
# (Do you take blood pressure medication? * C_Age_Do you take blood pressure medication?s * ln(Age) * ln(Systolic blood pressure)) + 
# (not Do you take blood pressure medication? * C_Off_Hypertension_Meds * ln(Systolic blood pressure)) + 
# (not Do you take blood pressure medication? * C_Age_Off_Hypertension_Meds * ln(Age) * ln(Systolic blood pressure)) + 
# (C_Do you smoke cigarettes? * Do you smoke cigarettes?) + 
# (C_Age_Do you smoke cigarettes? * ln(Age) * Do you smoke cigarettes?) + (C_Do you have diabetes? * Do you have diabetes?)

ClearTerms =  (CAge * log(55)) + (CSqAge * (log(55))**2) + (CTotalChol * log(180)) + (CAgeTotalChol * log(55) * log(180)) + \
  (CHDLChol * log(50)) + (CAgeHDLChol * log(55) * log(50)) + (0 * COnHypertensionMeds * log(130)) + \
  (0 * CAgeOnHypertensionMeds * log(55) * log(130)) + (1 * COffHypertensionMeds * log(130)) + \
  (1 * CAgeOffHypertensionMeds * log(55) * log(130)) + (0 * CSmoker) + (CAgeSmoker * log(55) * 0) + (CDiabetes * 0)
print(ClearTerms)

poly = EvaProgram("Polynomial", vec_size=4096)
with poly:
  lnAge = Input("lnage")
  sqlnAge = Input("sqlnage")
  lnTotalCholesterol = Input("lntotalcholesterol")
  lnHDLCholesterol = Input("lnhdlcholesterol")
  onHypertensionMeds = Input("onhypertensionmeds")
  lnSystolicBloodPressure = Input("lnsystolicbloodpressure")
  smoker = Input("smoker")
  diabetes = Input("diabetes")

  Output("terms", (CAge * lnAge) + (CSqAge * sqlnAge) + (CTotalChol * lnTotalCholesterol) + (CAgeTotalChol * lnAge * lnTotalCholesterol) + (CHDLChol * lnHDLCholesterol) + (CAgeHDLChol * lnAge * lnHDLCholesterol) + (onHypertensionMeds * COnHypertensionMeds * lnSystolicBloodPressure) + (onHypertensionMeds * CAgeOnHypertensionMeds * lnAge * lnSystolicBloodPressure) + ((1 - onHypertensionMeds) * COffHypertensionMeds * lnSystolicBloodPressure) + ((1 - onHypertensionMeds) * CAgeOffHypertensionMeds * lnAge * lnSystolicBloodPressure) + (CSmoker * smoker) + (CAgeSmoker * lnAge * smoker) + (CDiabetes * diabetes))

poly.set_output_ranges(30)
poly.set_input_scales(30)

# Compile program with CKKS scheme
from eva.ckks import *
compiler = CKKSCompiler()
compiled_poly, params, signature = compiler.compile(poly)

#
# Generate key context
#   public context contains : public key, relin key, galois key
#   secret context contains : secret key
#
from eva.seal import *
public_ctx, secret_ctx = generate_keys(params)

#
# Create encryption for x (= 0.0, 1.1, 2.2, 3.3)
#
inputs = { "lnage": [0.0 for i in range(compiled_poly.vec_size)], "sqlnage": [0.0 for i in range(compiled_poly.vec_size)], "lntotalcholesterol": [0.0 for i in range(compiled_poly.vec_size)], "lnhdlcholesterol": [0.0 for i in range(compiled_poly.vec_size)], "onhypertensionmeds": [0.0 for i in range(compiled_poly.vec_size)], "lnsystolicbloodpressure": [0.0 for i in range(compiled_poly.vec_size)], "smoker": [0.0 for i in range(compiled_poly.vec_size)], "diabetes": [0.0 for i in range(compiled_poly.vec_size)]}

inputs["lnage"][0] = log(arg_age)
inputs["sqlnage"][0] = (log(arg_age))**2
inputs["lntotalcholesterol"][0] = log(arg_tot_chol)
inputs["lnhdlcholesterol"][0] = log(arg_hdl)
inputs["lnsystolicbloodpressure"][0] = log(arg_systolic)
inputs["onhypertensionmeds"][0] = arg_meds
inputs["smoker"][0] = arg_smoke
inputs["diabetes"][0] = arg_diabetes

encInputs = public_ctx.encrypt(inputs, signature)
#save(encInputs, "pages/demos/encinputs.evaseal")
print(encInputs)

#
# Execute computation
#
encOutputs = public_ctx.execute(compiled_poly, encInputs)
save(encOutputs, "pages/demos/encoutput.evaseal")

#
# Decrypt results
#
outputs = secret_ctx.decrypt(encOutputs, signature)
print("********** Result is **********")
for i in range(1):
  #print(outputs["terms"][i])
  #print(MeanTerms)
  print("Cardiovascular risk: %4.2f%%" %(100 * (1 - S10**(exp(outputs["terms"][i]-MeanTerms)))))

