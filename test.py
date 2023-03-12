from fuzzywuzzy import fuzz

s1 = "neotropical comorant"
s2 = "neotropic cormorant"
threshold = 90  # set the threshold for a match

score = fuzz.token_set_ratio(s1, s2)
if score >= threshold:
    print(f"Strings match with score {score}")
else:
    print("Strings do not match")



