#### ######################### ### 
###  Part 1: Vacation Packages ###
#### ######################### ### 

# Super Class: VacationPackage #
def abstract_class():
    raise NotImplementedError("This is an abstract class. Please define the method in the subclass.")

def vacation_describe_package():
    abstract_class()

def vacation_calculate_cost():
    abstract_class()

#  VacationPackage: Data dictionary for Parent Class
def vacation_package_new(destination, cost_per_day, duration_in_days):
    new_object = {
        "destination": destination, #str
        "cost_per_day": cost_per_day, #int
        "duration_in_days": duration_in_days, #int
        "_class": VacationPackage
    }
    return new_object

# VacationPackage: Class / Methods Dictionary 
VacationPackage = {
    #attributes
    "_classname": "VacationPackage",
    "_parent": None,
    "_new": vacation_package_new,
    #abstract methods
    "describe_package": vacation_describe_package,
    "calculate_cost": vacation_calculate_cost
}
#### ###################### ### 

### #################################################### ### 
# 3 Subclasses: BeachResort, AdventureTrip, LuxuryCruise ###
### #################################################### ### 


# BeachResort Class #
def beach_calculate_cost(thing):
    if thing["includes_surfing"]:
        return thing["cost_per_day"] * thing["duration_in_days"] + 100
    return thing["cost_per_day"] * thing["duration_in_days"]


def beach_describe_package(thing):
    if thing["includes_surfing"]:
        return f"The {thing['duration_in_days']} day long {thing['_class']['vacation_type']} in {thing['destination']} includes surfing." 
    return f"The {thing['duration_in_days']} day long {thing['_class']['vacation_type']} in {thing['destination']} does not include surfing." 


# Data dictionary BeachResort
def beach_new(destination, cost_per_day, duration_in_days, surfing):
    return make(VacationPackage, destination, cost_per_day, duration_in_days) | {
        "includes_surfing": surfing,
        "_class": BeachResort
    }

# BeachResort: Class / Methods Dictionary 
BeachResort = {
    "_classname": "BeachResort",
    "_parent": VacationPackage,
    "_new": beach_new,
    "includes_surfing": "beach_surfing", #bool
    "calculate_cost":  beach_calculate_cost,
    "describe_package": beach_describe_package,
    "vacation_type": "Beach Resort vacation"
}
# ############# #


# AdventureTrip #
def adventure_calculate_cost(thing):
    if thing["difficulty_level"] == "hard":
        return thing["cost_per_day"] * thing["duration_in_days"] * 2
    return thing["cost_per_day"] * thing["duration_in_days"]


def adventure_describe_destination(thing): #Returns a string. Describes the destination, number of days, and the difficulty level
    if thing["difficulty_level"] == "hard":
        return f"The {thing['duration_in_days']} day long {thing['_class']['vacation_type']} in {thing['destination']} is considered hard." 
    return f"The {thing['duration_in_days']} day long {thing['_class']['vacation_type']} in {thing['destination']} is considered easy." 


# Data dictionary AdventureTrip
def adventure_new(destination, cost_per_day, duration_in_days, level):
    return make(VacationPackage, destination, cost_per_day, duration_in_days) | {
        "difficulty_level": level,
        "_class": AdventureTrip,
    }

#AdventureTrip: Class / Methods Dictionary 
AdventureTrip = {
    "_classname": "AdventureTrip",
    "_parent": VacationPackage,
    "_new": adventure_new,
    "calculate_cost":  adventure_calculate_cost,
    "describe_package": adventure_describe_destination,
    "vacation_type": "Adventure trip"
}
# ############# #

# LuxuryCruise #
def cruise_calculate_cost(thing):
    if thing["has_private_suite"]:
        return thing["cost_per_day"] * thing["duration_in_days"]*1.5
    return thing["cost_per_day"] * thing["duration_in_days"]


def cruise_describe_destination(thing):
    if thing["has_private_suite"]:
        return f"The {thing['duration_in_days']} day long {thing['_class']['vacation_type']} in {thing['destination']} includes a private suite." 
    return f"The {thing['duration_in_days']} day long {thing['_class']['vacation_type']} in {thing['destination']} does not include a private suite." 


# LuxuryCruise: Data dictionary 
def cruise_new(destination, cost_per_day, duration_in_days, has_private_suite):
    return make(VacationPackage, destination, cost_per_day, duration_in_days) | {
        "_class": LuxuryCruise,
        "has_private_suite": has_private_suite
    }

# LuxuryCruise: Class / Methods Dictionary 
LuxuryCruise = {
    "_classname": "LuxuryCruise",
    "_parent": VacationPackage,
    "_new": cruise_new,
    "calculate_cost": cruise_calculate_cost,
    "describe_package": cruise_describe_destination,
    "vacation_type": "Luxury Cruise"
}
# ############# #

#### ###################### ### 
# Make, Call & Find Functions #
#### ###################### ### 

### method to make new objects
def make(cls, *args, **kwargs):
    return cls["_new"](*args, **kwargs)

### method to call functions ###
def call(thing, key_name, *args, **kwargs):
    
    
    method = find(thing["_class"], key_name) #find methods function
    return method(thing, *args, **kwargs)

### recursive function to find specific method within class & parent classes
def find(cls:dict, key_name): 
    if key_name in cls.keys():
        return cls[key_name]

    elif "_parent" in cls.keys():
        if cls["_parent"] != None:
            if key_name in cls["_parent"].keys():
                return cls["_parent"][key_name]
        pass
    
    raise NotImplementedError("Missing method " + key_name)

#### ###################### ### 

#### ######################### ### 
###  Part 2: Vacation Summary  ###
#### ######################### ### 

def calculate_total_cost(thing):
    total = 0
    # print("DEBUG: calculating...")
    for value in thing["currentdict"].values():
        # print("DEBUG: for value in currentdict values")
        # the the current copy of globals, we check for values that fulfill 1. are a dictionary
        # 2. have VacationPackage as a Parent 3. include the search term
        if isinstance(value, dict):
            # print("DEBUG: value is dict")
            if "_class" in value:
                # print("DEBUG: class is a key in the dict")
                # print(f"DEBUG: class is {value['_class']['_classname']}")
                # print(f"DEBUG: parent class is {value['_class']['_parent']['_classname']}")
                if value["_class"] != VacationBookingSummary and "_parent" in value["_class"].keys():
                    if value["_class"]["_parent"]["_classname"] == "VacationPackage" and search(thing["search_term"], value):
                        total += call(value, "calculate_cost")

    return total


# the basic construction of the next function is just the same:
def extract_total_vacation_summary(thing):
    # print("DEBUG: summarizing...")
    totalstring = ""
    for value in thing["currentdict"].values():
        if isinstance(value, dict):
            if "_class" in value:
                if value["_class"] != VacationBookingSummary and "_parent" in value["_class"].keys():
                    if value["_class"]["_parent"]["_classname"] == "VacationPackage" and search( thing["search_term"], value):
                        totalstring += call(value, "describe_package")
                        totalstring += "\n"

    return totalstring


# set "" by default as a search term
def vacation_summary_new(search_term="", current_dict=None):
    return VacationBookingSummary | {
        "currentdict": globals().copy() if current_dict==None else current_dict,
        "search_term": search_term,
        "_class": VacationBookingSummary,
    }


VacationBookingSummary = {
    "_new": vacation_summary_new,
    "calculate_total_cost": calculate_total_cost,
    "extract_total_vacation_summary": extract_total_vacation_summary,
    "_parent": None,
}


# for a more structured code, a recursive implementation to find out
# whether the search term is in your dictionary:
def search(search_term, data):
    found = False
    # print("DEBUG: searching...")
    if isinstance(data, dict):
        for key, value in data.items():
            found = search(search_term, value) or found or search(search_term, key)

    if isinstance(data, str):
        if search_term.lower() in data.lower():
            found = True
            # print("DEBUG: Found!")

    return found


#### ################## ### 
# Examples for Step 1 & 2 #
#### ################## ### 

if __name__ == "__main__":

    # Examples for VacationPackage objects
    bea_1 = make(BeachResort, "Silent Beach", 100, 1, False)
    adv_1 = make(AdventureTrip, "Silent Hills", 100, 1, "easy")
    cru_1 = make(LuxuryCruise, "Silent Cruise 1", 100, 1, False)
    cru_2 = make(LuxuryCruise, "Silent Cruise 2", 100, 1, False)

    #cost of vacation package
    print(f'Output should  be 100 and is: {call(bea_1, "calculate_cost")}')
    
    ### ########################### ###

    #Examples for Summary Objects ###
    V_bea= make(VacationBookingSummary, search_term="beach") #only beach vacations
    V_tot=make(VacationBookingSummary) # all types of vacation packages

    #summary of all descriptions:
    print(call(V_tot, "extract_total_vacation_summary"))

    #total cost
    print(f'Output should  be 100 and is: {call(V_bea, "calculate_total_cost")}')
    print( f'Output should  be 400 and is: {call(V_tot, "calculate_total_cost")}') 
    ## ########################### ###

    
