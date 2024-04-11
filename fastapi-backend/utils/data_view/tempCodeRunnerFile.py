# For 'experience' with numeric values, handle separately
# df["experience"] = df["experience"].apply(
#     lambda x: x if x in replacements["experience"] else (x + "年" if x.isdigit() else x)
# )
# df["experience"] = df["experience"].apply(
#     lambda x: x
#     if pd.isnull(x) or x in replacements["experience"]
#     else (x + "年" if isinstance(x, str) and x.isdigit() else x)
# )