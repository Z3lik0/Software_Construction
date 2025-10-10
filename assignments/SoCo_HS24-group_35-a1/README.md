# 35-Assignment-1

#### 1. Assignment Structure: Division of Tasks
   1. **Part 1 - Class System**
    - **Frame**: Alina
    - **Implementing Methods and Adapting Frame**: Yifu
        - **Adding Abstract Methods**: Alina
   
2. **Part 2 - Vacation Summaryr**
   - **Main Design**: Lisa
        - **Fixing Bugs**: Yifu
        - **Fixing Bugs 2.0**: Lisa

3. **Part 3 - Testing Frame + Tests**

   - **Testing Frame**: Yifu, Alina, Lisa
      - **Initial Test Frame**: Yifu 
         -- Example: 
            test_vacation_booking threw an exception.
            test_test_failing failed.
            test_test_error threw an exception.
            pass: 22
            fail: 1
            error: 2
      - **Format Output: Test name + results are printed at the same time**: Alina 
         -- Example: 
            test_par_abstract_calculate_cost  ----- PASS
      - **Include Error Message**: Alina Example: Alina 
         -- Example: 
            test_test_failing  ----- FAIL: Expected: 1 ≠ Actual: 2 --- REMARK: This test is supposed to fail. 
            test_test_error  ----- ERROR: unsupported operand type(s) for -: 'int' and 'str'
      - **Include Time**: Lisa 
         -- Example: 
            running test_not_implemented_functions... PASS  (in 0.00000s)
      - **Include cmd --select**: Lisa

   - **Tests for Class System (Inheritance and Abstract Classes)**: Yifu, Alina, Lisa 
     - **Beach Resort**: Alina
     - **Adventure Resort**: Lisa
     - **Luxury Cruise**: Yifu
   - **Tests for Testing Frame**: Alina
   - **Tests for Vacation Summary**: Lisa

#### 2. **Explanation of the decisions taken in Step 1: Vacation Package** (written by Yifu)
**vacation_package.py** 

'vacation_describe_package', 'vacation_calculate_cost' are abstract methods of the 'VacationPackage' class. 
'VacationPackage' is the parent class for 'BeachResort', 'AdventureTrip', and 'LuxuryCruise'. 
An abstruct method is a method that is declared in a class, but does not contain any implementation. It is meant to be overridden by subclasses that inherit from the parent class. 

To make sure that when an instance of a class is made correctly, we need to implement constructors. We do this by giving the dictionaries that implement classes a special key '_new', whose value is the function that builds something of that type. 'vacation_package_new' is such a function. This type of functions is also responsible for upcalling the constructor of its parent, if it has one. For instance, the constructor for 'BeachResort' calls the constructor for 'VacationPackage' and adds 'BeachResort' specific values using '|' to combine two dictionaries, as we can see in 'beach_new'. 

We want vacation objects to store different values (e.g. different vacations have different destinations, cost per day, and duration in days) but the same behaviors (all beach resort vacations should have the same methods). We can implement this by storing the methods in a dictionary that corresponds to a class and having each individual vacation contain a reference to that higher-level dictionary. This reference uses the key '_class'. 
We do the same with all three different type of vacations. 

Summary of each class:

`'VacationPackage'` class contains three attributes and two methods.

Attibutes:

 '_classname', something that allows us to identify the class quickly
'_parent', the parent class which in this case there isn't any; 
'_new', the reference to the function that builds an instance of VacationPackage. 

Methods:

'describe_package' stores a reference to the function 'vacation_describe_package'
'calculate_cost' stores a reference to the function 'vacation_calculate_cost'
Both methods are abstrct as mentioned previously. 

`'BeachResort'` class contains four attributes and three methods.

Attributes:

'_classname': a quick identifier for the class
'_parent': points to the parent class 'VacationPackage'
'_new': the reference to the function that builds an instance of 'BeachResort'
'vacation_type': describes the type of vacation as "Beach Resort vacation"

Methods:

'describe_package': stores a reference to 'beach_describe_package'
'calculate_cost': stores a reference to 'beach_calculate_cost'


`'AdventureTrip'` class contains four attributes and two methods.

Attributes:

'_classname': a quick identifier for the class
'_parent': points to the parent class 'VacationPackage'
'_new': the reference to the function that builds an instance of 'AdventureTrip'
'vacation_type': describes the type of vacation as "Adventure trip"

Methods:

'describe_package': stores a reference to 'adventure_describe_destination'
'calculate_cost': stores a reference to 'adventure_calculate_cost'

`'LuxuryCruise'` class contains four attributes and two methods.

Attributes:

'_classname': a quick identifier for the class
'_parent': points to the parent class 'VacationPackage'
'_new': the reference to the function that builds an instance of 'LuxuryCruise'
'vacation_type': describes the type of vacation as "Luxury Cruise"

Methods:

'describe_package': stores a reference to 'cruise_describe_destination'
'calculate_cost': stores a reference to 'cruise_calculate_cost'

In addition to the key-value pairs described in the class dictionaries  above,
An instance of a generic vacation also contains other information about the vacation: destination, cost per day, duration in days. 
An instance of beach resort vacation also contains 'includes_surfing', a Boolean value documenting if the vacation includes surfing.
An instance of adventure trip vacation also contains 'difficulty_level', which can be 'hard' or 'easy'. 
An instance of luxury cruise vacation also contains 'has_private_suite', a Boolean value documenting if the vacation include a private suite. 

To use the "methods" stored in the dictionaries, we use the 'call' function. It first looks up the dictionary, then looks up the function stored in that dictionary, then calls that function.

In order to make an object, we use the 'make' function to call the function associated with its '_new' key.

   
#### 3. **Explanation of the decisions taken in Step 2: Vacation Summary** (written by Lisa)
**vacation_package.py** 

   - At first it was considered to create a Summary class on top of the code. Inside, there would be a permanent list or dictionary, that keeps track of each Object being instantiated.
   To do this in a lean way, we considered modifying the make() function. The second, and chosen, option was using globals().
   We decided to use globals for several reasons. Firstly, it turned out to be difficult to store the name given to an object. (Example: balloonride = AventureTrip(.., ..., ...) here it would be difficult to retrieve the name "balloonride". Because it is not passed to the make() function) Secondly, it seemed like redundant code. We would have one hidden and one new Summary object to use the functions. And thirdly, it simply was the solution we looked at in class.

   - For the search_term implementation an outside search() function was created. Even though it is only used for Summary objects. This was to make the code more structured and easier to expand/modify.

   - The keyword variable current_dict=None was originally not implemented. With it you can replace the globals if you need to. We implemented it later, when writing tests for Summary objects.

   - globals().copy() was used to prevent the dictionary to be dynamic, which easily leads to problems. This way, the dictionary is static from the moment the object is instantiated. 

#### 4. **Explanation of the decisions taken in Step 3: Testing Framework** (written by Alina)
 **vacation_package_test.py**

The `find_tests` function searches the global scope to find tests based on their prefix. It excludes its own file or module name, so it doesn't include itself in the tests (which would lead to an error, as the following function couldn't run it). It searches for any functions with the prefix "test_" in the global scope and creates a dictionary where the key is the test name and the value is the function.

The `run_tests` function takes the output from `find_tests` and works with two dictionaries:

- `results` for summarizing the scores (e.g., `{'pass': 12, 'fail': 1, 'error': 1}`).
- `results_deets` that appends the test names according to their results (`{"pass": [], "fail": [], "error":[]}`)

All the tests collected in the dictionary from `find_tests` are run within a try-except block. If no error occurs, the "pass" count is incremented by 1. If an `AssertionError` happens, the "fail" count is incremented by 1. Any other error increments the "error" count by 1. This process gives us a final score, which is printed at the end of the loop.

In the second dictionary, `results_deets` (`{"pass": [], "fail": [], "error":[]}`), more detailed information is stored. Test names are appended according to their results (pass, fail, or error). Returning this second dictionary isn't necessary, as results are printed directly. However, it can be useful for expanding the framework (e.g., to filter tests by result). This is why we kept and returned the `results_deets` dictionary despite it being redundant.

For every test run, the `run_tests` function prints the test name along with its status (pass, fail, or error), as well as the time it took to run. This was implemented using the time module and lets the user compare the duration it took for each test. In case of an error, the error message is printed. For AssertionErrors (fail), the assertion message is displayed instead. The main result is highlighted with color to improve readability. PASS is highlighted blue, FAIL is highlighted yellow, ERROR is highlighted red

Example Output:
`running test_not_implemented_functions... PASS  (in 0.00000s)`
`running test_test_failing... FAIL: Expected: 1 ≠ Actual: 2 --- REMARK: This test is supposed to fail.  (in 0.00000s)`
`running test_test_error... ERROR: unsupported operand type(s) for -: 'int' and 'str' (in 0.00000s)`
`{'pass': 22, 'fail': 1, 'error': 1}`


 **Selective Test Execution with --select Parameter**: (Lisa)
 Necessary import of sys. Then, the easiest way to filter the tests is through a dictionary comprehension, which we also looked at in class.

**Test Design / Structure** 
Using the format of `actual vs expected` within the tests allows for a quick understanding of what is being tested. Besides this, it makes it easier to implement a standardized AssertionError message (`assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"`)
Implementing such a short message for each assertion helps users by giving further insights as to why the tests are failing and consequently about what should be changed in order to fix the problem. 

Example: 
def test_cru_cost_with_private_suite_decimal():
    cruise = make(LuxuryCruise, "Dest", 1.11, 7, True)
    `expected = 1.11 * 7 * 1.5`
    `actual = call(cruise, "calculate_cost")`
    `assert expected == actual, f"Expected: {expected} ≠ Actual: {actual}"`


        
- **Tests for VacationPackage - Testing Part 1 & 2:**
The tests were chosen to check whether our implementation fullfilled the criteria stated in the Lab1 description. We chose to check whether our methods produce the right strings and calculate correctly. Additionally we tested whether our inheritance system works by checking whether abstract methods were implemented correctly and whether the parent classes were correct also.

    - **Parent Class (VacationBooking)  (Alina):**
      - test_vac_abstract_describe_package: Should raise an error as it is an abstract method: tested with a try-except block (fails if the )
      - test_vac_abstract_calculate_costs: Should raise an error as it is an abstract method: tested with a try-except block
        
    - **BeachResort (Alina):** 
      - test_bea_surfing_included: Tests whether the string is according to the expected output: "..includes surfing"
      - test_bea_surfing_not_included: Tests whether the string is according to the expected output: "..does not include surfing"
      - test_bea_surfing_higher_price: Tests whether the price is adjusted correctly (+100) in `calculate_cost` method if surfing = True
      - test_bea_inheritance: Tests whether the parent of BeachResort Object is VacationPackage

     - **AdventureResort (written by Lisa):** 
      - test_adv_easy_descr: verify that the class properly handles trips with "easy difficulty, ensuring the describe_package method reflects this correctly.

      - test_adv_not_hard_descr: ensure that the AdventureTrip class can accurately represent trips with a "hard" difficulty level in its description.

      - test_adv_higher_price: confirm that the cost calculation method works properly, especially when pricing changes are based on the difficulty level.

      - test_adv_inheritance: ensure that the class structure follows the expected inheritance hierarchy, which is essential for maintaining shared functionality across vacation types.


     - **LuxuryCruise (written by Yifu):** Explain specific cruise-related functionalities being tested
     
         - test_cru_describe_with_private_suite: 
         is chosen to verify that the describe_package method of the LuxuryCruise class correctly describes a cruise when it includes a private suite. It ensures that the method generates the expected description by matching the output (actual) with the predefined expected string. The test checks if the description accurately describes the cruise's destination, duration, and the inclusion of a private suite.

         - test_cru_describe_without_private_suite: This test verifies that the describe_package method of the LuxuryCruise class correctly describes a cruise when a private suite is not included. It checks if the function provides an accurate description of the cruise's destination, duration, and the absence of a private suite by comparing the actual output with the expected description.

         - test_cru_cost_with_private_suite: This test ensures that the calculate_cost method of the LuxuryCruise class correctly calculates the total cost when the cruise includes a private suite. It verifies that the cost is calculated as the cost per day multiplied by the duration and adjusted by a 1.5 factor for the suite.

         - test_cru_cost_without_private_suite: This test verifies that the calculate_cost method properly calculates the total cost when the cruise does not include a private suite. It checks that the cost is simply the cost per day multiplied by the duration without any additional factor.

         - test_cru_cost_with_private_suite_decimal: This test ensures that the calculate_cost method handles decimal in cost per day correctly when a private suite is included, ensuring precision with decimal values.


     - **Vacation Summary (written by Lisa):**  
   
      Because we imported vacation_booking.py by "from vacation_booking import *": when we call globals(), we call globals in the "vacation.booking.py" file and import that directly to this file. The globals of this file are not considered. We had to replace the globals().copy() with a costumized dictionary, just for testing.

         - test_summary_no_search_term: if methods work without a search_term, meaning the search_term is per default "", and objects always contain "".

         - test_summary_search_term_in_destination: if search_term works, if it's in the "destination" variable.

         - test_summary_search_term_in_class: if search_term works, if it's in the the name of the class.

         - test_summary_calculate_cost: if the calculation method works.

         - test_summary_ignore_summary_objects: When instantiating several Summary objects, it could lead to crashes, if it's too similar to - but not - an object we need to consider.

         - test_summary_inheritance: Checks the inheritance.

         - test_not_implemented_functions: If we call a Summary object, with a method of another class, it should raise a NotImplementedError.

- **Tests for Testing Frame - Testing Part 3 (written by Alina):**
   - test_test_failing: Should see how the testing framework reacts when a FAIL occurs. For the fail we're using two different integers and assert if they're equal 1 ≠ 2
   - test_test_error: This test should show how the framework reacts to an ERROR. To create an error, we used an integer and a string to create an operation that would make the code break. 1 -"hello

   # same thing but testing these using our objects
   - test_bea_failing: again, the test should fail, as we made sure to give the wrong expected value
   - test_adv_error: by missing one positional argument in creating the object, this test should raise an error.

#### 6. **Use of Generative AI**
   - Used ChatGPT to for README.md structure suggestions and improving readability in markdown format (Alina)




