# 35-Assignment-2

Note: Alina Vanessa Brüllhardt and Z3lik0 are the same person

#### 1. Assignment Structure: Division of Tasks
1. **Step-01 - Support Infix Structure**
    - **Main Design (Arithmetic + Bool)**: Alina
   
2. **Step-02 - Simple Lexical Scoping in LGL**
   - **Main Design**: Yifu & Lisa
        - **Version1**: Yifu
        - **Version2"**: Lisa
        bugfixes: everyone


3. **Step-03 - Tracing**
     - **Main Design Tracer**: Lisa 
     - **Main Design Reporter**: Alina 

Additionally:

**test_file.py:**
     Chatgpt, Lisa, Alina
     Lisa: Prompting ChatGPT to create test file
     Alina: clearer function names + introspection to find tess so we can run new tests more seamlessly.


------------------------------------------------------------------

#### 2. **Explanation of the decisions taken in Step 1: Infix Structure** (written by Alina)
Initially, we considered using the notation ["1 + 2"] for infix functions. However, we realized that this would complicate both the implementation and future extensions. As a result, we opted for the notation [1, "+", 2].

We also explored ways to simplify the process of handling operators and found Python’s eval() function, which we chose over using multiple if statements. This approach avoids repetitive code and improves readability.

In the first version, we implemented the functionality directly in the do function. However, this approach did not align with the course's emphasis on separating tasks to reduce errors and maintain clarity. Therefore, we decided to refactor the code.

We initially considered adding separate entries to the OPS dictionary for each arithmetic and boolean operator, along with individual do functions for each. However, this would have led to unnecessary repetition. Instead, we grouped the arithmetic and boolean infix operations together, as they share similar structures. To maintain organization and ensure these operations were included in the OPS dictionary, we created the do_infix_arithmetic and do_infix_bool functions. These are then called by a single do_infix function, which eliminates the need for additional if statements in the main do function. The do_infix function essentially just decides which of the others should be called.
#### 3. **Explanation of the decisions taken in Step 2: Lexical Scoping** (written by Yifu & Lisa)
In lexical scoping, the scope of a variable is determined by the physical structure of the code. When looking up a variable, we first check the current function's scope, then the scope of the function in which the current function is defined, and so on, until we reach the global environment.
<br/>
<br/>
We define a class object, *Environment*, to capture the physical structure of the code as it is written. This class has three member variables: a dictionary that stores variable names and their values as key-value pairs; *parent*, which is the scope in which the function is defined; and *name*, which is the name of the function or 'global' if the environment is the global environment. To get and set values in the dictionary, we also include *get* and *set* member functions within the *Environment* class. In the *get* function, if we can't find a specific variable, we recursively attempt to retrieve it from the parent scope.

Instead of passing a stack of Environments, we actually only pass one Environment at the time. But the Environments point to each other, like in a linked list. This enables a tree like structure.
<br/>
<br/>
First, we create a global environment by instantiating *Environment* with the name 'global', an empty dictionary, and a *parent* set to *None*. 
Each time a function is called, a new scope for the function is created. In *do_call*, we create a new instance of *Environment* as the local environment of the function, called *local_env*. Its *name* variable is the name of the function being called, and its *parent* is the scope of the environment in which the current function is defined, or 'global' if it is not nested within another function. 

The environment, in which the function is defined, is stored when we first set the fuction in "do_func". We don't only store parameter and body, but also environment. This is essential, because we implemented true lexical scoping. Multiple nested functions will still output the correct lexical scoping. As seen in the test "test_lexical_scoping_nested_function".

This local environment is then passed into the *do* function when evaluating the body of the current function, thereby establishing the physical structure of the code.

#### 4. **Explanation of the decisions taken in Step 3: Tracing** (written by Lisa)

**Building the String**

Rather than writing each line directly to the trace file, we opted to declare a global string at the top of the code, editing and using this string across functions via globals(). Although using globals is generally discouraged, it was the most straightforward solution here. It also simplifies debugging, as we can easily print the global string to the terminal. Additionally, frequently opening and closing a file increases the risk of introducing errors.

**Wrapping the Function**

When an action must occur before ("start") and after ("stop") each function call, a decorator is ideal. We used a basic decorator structure already present in the lecture to achieve this.

Within the wrapper function, a unique call ID is generated by choosing a random number between 100000 and 999999. We considered using hashing (based on function name and timestamp) to ensure uniqueness, as random numbers could theoretically repeat. However, the simple random approach was sufficient, as the likelihood of duplicate IDs is extremely low.

The helper function log_event() is called twice per function call, generating a timestamp and updating the global log string (logstring).

By using the @wrap decorator, we can wrap the do_call function seamlessly.

**Generating the trace_file.log**

The sys module (specifically sys.argv) retrieves information provided by the user in the command line, including the path to the source file, whether a trace file should be generated, and the desired file name.

If the user includes --trace without specifying a file name, the default is set to trace_file.log.

After the code completes, the global string (logfile) contains the necessary log entries, including newline characters (\n). The final step is to write this global string to the trace file using a context manager.


### 5. Use of Generative AI
Lisa -> 
     - Generated test_file.py
     - Translating "little german language" to python and vice versa, because it is very error prone.
     - Help with modules datetime and sys

Alina -> structuring README.md report & to help me understand / debug functions that use the sys module

