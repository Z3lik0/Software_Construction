from vacation_booking import *
from testing_framework import find_tests, run_tests
import test_vacation_booking  # Import the current test module
import time
import sys

# Tests for Parent Class
def test_vac_abstract_describe(): #is this an abstract class?
    vac_1 = make(VacationPackage, "The World", 100, 1)
    try: 
        actual = call(vac_1, "vacation_describe_package")
        assert False  # This should never be reached
    except NotImplementedError:
        assert True


def test_vac_abstract_calculate_cost():
    vac_1 = make(VacationPackage, "The World", 100, 1)
    try: 
        actual = call(vac_1, "vacation_calculate_cost")
    except NotImplementedError:
        assert True    

### ################# ###
### ################# ###

# Tests for BeachResort

def test_bea_surfing_included(): # tests string output of description
    beach = make(BeachResort, "Maldives", 100, 7, True)
    expected = "The 7 day long Beach Resort vacation in Maldives includes surfing."
    actual = call(beach, "describe_package")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_bea_surfing_not_included(): # tests string output of description
    beach = make(BeachResort, "Maldives", 100, 7, False)
    expected = "The 7 day long Beach Resort vacation in Maldives does not include surfing."
    actual = call(beach, "describe_package")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_bea_surfing_higher_price(): #tests results of calculation method
    beach = make(BeachResort, "Maldives", 100, 7, True)
    expected = 7 * 100 + 100
    actual = call(beach, "calculate_cost")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_bea_inheritance(): #tests whether the parent is VacationPackage
    beach = make(BeachResort, "Maldives", 100, 7, True)
    expected = "VacationPackage"
    actual = beach["_class"]["_parent"]["_classname"] 
    assert actual is expected, f"Expected Parent: {expected} ≠ Actual Parent: {actual}"

### ################# ###
### ################# ###

# Tests for AdventureTrip


def test_adv_easy_descr(): # tests string output of description
    adventure = make(AdventureTrip, "Peru", 150, 4, "easy")
    expected = "The 4 day long Adventure trip in Peru is considered easy."
    actual = call(adventure, "describe_package")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_adv_not_hard_descr(): # tests string output of description
    adventure = make(AdventureTrip, "Peru", 150, 4, "hard")
    expected = "The 4 day long Adventure trip in Peru is considered hard."
    actual = call(adventure, "describe_package")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_adv_higher_price(): #tests results of calculation method, "hard"
    adventure = make(AdventureTrip, "Peru", 150, 4, "hard")
    expected = 4 * 150 *2
    actual = call(adventure, "calculate_cost")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_adv_inheritance(): #tests whether 
    adventure = make(AdventureTrip, "Peru", 150, 4, "easy")
    expected = "VacationPackage"
    actual = adventure["_class"]["_parent"]["_classname"] 
    assert actual is expected, f"Expected Parent: {expected} ≠ Actual Parent: {actual}"

# Tests for LuxuryCruise

def test_cru_describe_with_private_suite():
    cruise = make(LuxuryCruise, "Dest", 100, 7, True)
    expected = "The 7 day long Luxury Cruise in Dest includes a private suite."
    actual = call(cruise, "describe_package")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"


def test_cru_describe_without_private_suite():
    cruise = make(LuxuryCruise, "Dest", 100, 7, False)
    expected = "The 7 day long Luxury Cruise in Dest does not include a private suite."
    actual = call(cruise, "describe_package")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_cru_cost_with_private_suite():
    cruise = make(LuxuryCruise, "Dest", 100, 6, True)
    expected = 100 * 6 * 1.5
    actual = call(cruise, "calculate_cost")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_cru_cost_without_private_suite():
    cruise = make(LuxuryCruise, "Dest", 100, 6, False)
    expected = 100 * 6 
    actual = call(cruise, "calculate_cost")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_cru_cost_with_private_suite_decimal():
    cruise = make(LuxuryCruise, "Dest", 1.11, 7, True)
    expected = 1.11 * 7 * 1.5
    actual = call(cruise, "calculate_cost")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"


### ################# ###
### ################# ###

# Isinstance-like Test

### ################# ###
def is_instance_of(obj, class_type):
    if obj is not None:
        if obj["_classname"] == class_type:
            return True
        else:
            return is_instance_of(obj["_parent"], class_type)
    return False



### ################# ###
### ################# ###

# Tests for Summary of all Vacations

#because we imported vacation_booking.py by "from vacation_booking import *"
#when we call globals(), we call globals in the "vacation.booking.py" file and import that directly to this file.
#the globals of this file are not considered.
#we need to use a trick: replace the globals with our own dictionary

def test_summary_no_search_term():
    costum_dict1 = {
    "Zurich_Adventure": make(AdventureTrip, "Zurich", 100, 1, "easy"),
    "Uster_Adventure": make(AdventureTrip, "Uster", 100, 1, "hard")
    }
    
    V1=make(VacationBookingSummary, current_dict=costum_dict1)
    
    expected="The 1 day long Adventure trip in Zurich is considered easy.\nThe 1 day long Adventure trip in Uster is considered hard.\n"
    actual=call(V1, "extract_total_vacation_summary")

    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

    


def test_summary_search_term_in_destination():
    costum_dict2 = {
    "Zurich_Adventure": make(AdventureTrip, "Zurich", 100, 1, "easy"),
    "Uster_Adventure": make(AdventureTrip, "Uster", 100, 1, "hard"),
    "Planet Jupiter": make(AdventureTrip, "Planet Jupiter", 100, 1, "hard")
    }
    
    V2=make(VacationBookingSummary, search_term="planet", current_dict=costum_dict2)
    
    actual=call(V2, "extract_total_vacation_summary")
    expected="The 1 day long Adventure trip in Planet Jupiter is considered hard.\n"
    
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"

def test_summary_search_term_in_class():
    costum_dict3 = {
    "Zurich_Adventure": make(AdventureTrip, "Zurich", 100, 1, "easy"),
    "Uster_Adventure": make(AdventureTrip, "Uster", 100, 1, "hard"),
    "Planet Jupiter": make(LuxuryCruise, "Planet Jupiter", 100, 1, "hard")
    }
    
    V2=make(VacationBookingSummary, search_term="cruise", current_dict=costum_dict3)
    
    actual=call(V2, "extract_total_vacation_summary")
    expected="The 1 day long Luxury Cruise in Planet Jupiter includes a private suite.\n"
    
    
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"



def test_summary_calculate_cost():
    costum_dict3 = {
    "Zurich_Adventure": make(AdventureTrip, "Zurich", 100, 1, "easy"),
    "Uster_Adventure": make(AdventureTrip, "Uster", 100, 1, "hard"),
    "Planet Jupiter": make(LuxuryCruise, "Planet Jupiter", 100, 1, "hard")
    }
    V3=make(VacationBookingSummary, current_dict=costum_dict3)
    
    expected= 450.0
    actual=call(V3, "calculate_total_cost")
    
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"



def test_summary_ignore_summary_objects():
    costum_dict4 = {
    "Zurich_Adventure": make(AdventureTrip, "Zurich", 100, 1, "easy"),
    "Uster_Adventure": make(AdventureTrip, "Uster", 100, 1, "hard"),
    "Summary Object": make(VacationBookingSummary, search_term="planet")
    }
    
    V4=make(VacationBookingSummary, current_dict=costum_dict4)

    expected="The 1 day long Adventure trip in Zurich is considered easy.\nThe 1 day long Adventure trip in Uster is considered hard.\n"
    actual=call(V4, "extract_total_vacation_summary")

    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"


def test_summary_inheritance():
    V5=make(VacationBookingSummary)
    
    actual=V5["_class"]["_parent"]
    expected=None
    
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"


def test_not_implemented_functions():
    V5=make(VacationBookingSummary)
    try: 
        actual = call(V5, "vacation_describe_package")
        assert False
    except NotImplementedError:
        assert True


### ################# ###



# Tests of the Testing Framework
def test_test_failing(): #assert equal should fail as they are not equal
    expected = 1
    actual = 2
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual} --- REMARK: This test is supposed to fail. " 

def test_bea_failing(): #should fail due to wrong expected value
    beach = make(BeachResort, "Maldives", 100, 7, True)
    expected = 0 #actually expected 7 * 100 + 100
    actual = call(beach, "calculate_cost")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual} --- REMARK: This test is supposed to fail. "    

def test_test_error(): # should throw an error due to incompatible types for operation
    assert 1-"hello"

def test_adv_error(): #should cause an error due to missing positional argument
    catventure = make(AdventureTrip, "Istanbul", 150, "with_cats")
    expected = "The 4 day long Adventure trip in Istanbul is considered cute."
    actual = call(catventure, "describe_package")
    assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"


# ### ################# ###
    
# # Testing Framework 
    
# ### ################# ###

# def find_tests(prefix = "test_"): #outputs a list of tests
#     all_tests = {}
#     #module_name = __file__.split("")[-1][:-3] # file name / module name
#     #backslash is different in each OS -> let's just use a string

#     for name, test in globals().items():
#         if name.startswith(prefix) and name != "test_vacation_booking": #module_name
#               all_tests[name] = test
#     return all_tests

# def run_tests(all_tests: dict, pattern: str):
#     results = {"pass": 0, "fail": 0, "error":0}
#     results_deets= {"pass": [], "fail": [], "error":[]}



#     if pattern:
#         all_tests = {name: test for name, test in all_tests.items() if pattern.lower() in name.lower()}
    

#     for name, test in all_tests.items():
#         start_time=time.time()
        
#         try:
#             test()
#             results["pass"] +=1 # expected output
#             results_deets["pass"].append(name) 
#             s=f"running {name}... \033[44m'PASS\033[0m"
#         except AssertionError as e: # when output isn't expected
#             results["fail"] += 1
#             results_deets["fail"].append(name)
#             s=f"running {name}... \033[43m'FAIL:\033[0m {e}"
#         except Exception as e: # when something else failed 
#             results["error"] += 1
#             results_deets["error"].append(name)
#             s=f"running {name}... \033[41mERROR:\033[0m {e}"
        
#         end_time=time.time()
#         duration=end_time-start_time
        
#         print(f"{s} (in {duration:.5f}s)")
        
        
#     print (f"\n{results}\n")
#     return results_deets


# ### ################# ###
# ### ################# ###
# if __name__ == "__main__":
    
#     if "--select" in sys.argv:
#         pattern_index = sys.argv.index("--select") + 1

#         if pattern_index < len(sys.argv):
#             pattern1 = sys.argv[pattern_index]

#     else:
#         pattern1=""
        
    
#     tests = find_tests()
#     run_tests(tests, pattern=pattern1)    


if __name__ == "__main__":
    "Usage: python test_vacation_booking.py --select beach"
    pattern = ""
    if "--select" in sys.argv:
        index = sys.argv.index("--select") + 1
        if index < len(sys.argv):
            pattern = sys.argv[index]

    # Pass test_vacations as the module
    tests = find_tests(module=test_vacation_booking)
    run_tests(tests, pattern=pattern)

