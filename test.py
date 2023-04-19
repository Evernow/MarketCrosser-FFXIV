ingredientlst ={"Iron Ingot": {
            "Job": ["Armorer"],
            "Category": "Metal",
            "Level": " 13",
            "Difficulty": 27,
            "Amount from craft": 1,
            "Ingredients": {
                  "": "",
                  "Iron Ore": "3",
                  "Ice Shard": "1"
            }
}}
name="Iron Ingot"
job=["Blacksmith"]

if name in ingredientlst:
    ingredientlst[name]["Job"]=ingredientlst[name]["Job"] +job
    print(ingredientlst)
    
    