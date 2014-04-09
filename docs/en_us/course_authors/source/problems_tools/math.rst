.. _Math Problems:

########################
Math Problems
########################

.. _Numerical Input:

*******************
Numerical Input
*******************

In numerical input problems, students enter numbers or specific and
relatively simple mathematical expressions to answer a question. 

.. image:: ../Images/image292.png
 :alt: Image of a numerical input problem

Note that students' responses don't have to be exact for these problems. You can specify a margin of error, or tolerance. You can also specify a correct answer explicitly, or use a Python script. For more information, see the instructions below.

Responses for numerical input problems can include integers, fractions,
and constants such as *pi* and *g*. Responses can also include text
representing common functions, such as square root (sqrt) and log base 2
(log2), as well as trigonometric functions and their inverses, such as
sine (sin) and arcsine (arcsin). For these functions, Studio changes the
text that the student enters into mathematical symbols. The following
example shows the way Studio renders students' text responses in
numerical input problems. 

.. image:: ../Images/Math5.png
 :alt: Image of a numerical input probem rendered by Studio

The following are a few more examples of the way that Studio renders numerical input
text that students enter.

.. image:: ../Images/Math1.png
 :alt: Image of a numerical input probem rendered by Studio
.. image:: ../Images/Math2.png
 :alt: Image of a numerical input probem rendered by Studio
.. image:: ../Images/Math3.png
 :alt: Image of a numerical input probem rendered by Studio
.. image:: ../Images/Math4.png
 :alt: Image of a numerical input probem rendered by Studio
.. image:: ../Images/Math5.png
 :alt: Image of a numerical input probem rendered by Studio

=================================
Create a Numerical Input Problem 
=================================

You can create numerical problems in the Simple Editor and in the Advanced Editor regardless of the answer to the problem. If the text of your problem doesn't include any italics, bold formatting, or special characters, you can create the problem in the Simple Editor. If the text of your problem contains special formatting or characters, or if your problem contains a Python script, you'll use the Advanced Editor.

For example, the following example problems require the Advanced Editor. 

.. image:: ../Images/NumericalInput_Complex.png
 :alt: Image of a more complex numerical input problem

For more information about including a Python script in your problem, see :ref:`Custom Python Evaluated Input`.

.. note:: All problems must include labels for accessibility. The label generally includes the text of the main question in your problem. To add a label for a common problem, surround the text of the label with angle brackets pointed toward the text (>>*label text*<<).

Simple Editor
-------------

#. Under **Add New Component**, click **Problem**.
#. In the **Select Problem Component Type** screen, click **Numerical
   Input** on the **Common Problem Types** tab.
   
3. When the new Problem component appears, click **Edit**.
#. In the component editor, replace the sample problem text with your own text.
#. Determine the text of the problem to use as a label, and then surround that text with two sets of angle brackets (>><<).
#. Select the text of the answer, and then click the numerical input button. 

.. image:: ../Images//ProbCompButton_NumInput.png
    :alt: Image of the numerical input button
   
When you do this, an equal sign appears next to the answer.
        
7. (Optional) Specify a margin of error, or tolerance. You can specify a percentage, number, or range.

   * To specify a percentage on either side of the correct answer, add **+-NUMBER%** after the answer. For example, if you want to include a 2% tolerance, add **+-2%**. 

   * To specify a number on either side of the correct answer, add **+-NUMBER** after the answer. For example, if you want to include a tolerance of 5, add **+-5**.

   * To specify a range, use brackets [] or parentheses (). A bracket indicates that range includes the number next to it. A parenthesis indicates that the range does not include the number next to it. For example, if you specify **[5, 8)**, correct answers can be 5, 6, and 7, but not 8. Likewise, if you specify **(5, 8]**, correct answers can be 6, 7, and 8, but not 5.

8. In the component editor, select the text of the explanation, and then click the 
   explanation button to add explanation tags around the text.

   .. image:: ../Images/ProbCompButton_Explanation.png
    :alt: Image of athe explanation button

9. On the **Settings** tab, specify the settings that you want. 
#. Click **Save**.

For the first example problem above, the text in the Problem component is the
following.

::

   >>What base is the decimal numeral system in?<<

   = 10
    
   [explanation]
   The decimal numerial system is base ten.
   [explanation]


Advanced Editor
---------------

To create this problem in the Advanced Editor, click the **Advanced** tab in the Problem component editor, and then replace the existing code with the following code.

**Problem Code**:

.. code-block:: xml

  <problem>
    <p><b>Example Problem</b></p>

  <p>What base is the decimal numeral system in?
      <numericalresponse answer="10">
          <formulaequationinput label="What base is the decimal numeral system in?"/>
      </numericalresponse>
  </p>

    <p>What is the value of the standard gravity constant <i>g</i>, measured in m/s<sup>2</sup>? Give your answer to at least two decimal places.
    <numericalresponse answer="9.80665">
      <responseparam type="tolerance" default="0.01" />
      <formulaequationinput label="Give your answer to at least two decimal places"/>
    </numericalresponse>
  </p>

  <!-- Use python script spacing. The following should not be indented! -->
  <script type="loncapa/python">
  computed_response = math.sqrt(math.fsum([math.pow(math.pi,2), math.pow(math.e,2)]))
  </script>

  <p>What is the distance in the plane between the points (pi, 0) and (0, e)? You can type math.
      <numericalresponse answer="$computed_response">
          <responseparam type="tolerance" default="0.0001" />
          <formulaequationinput label="What is the distance in the plane between the points (pi, 0) and (0, e)?"/>
      </numericalresponse>
  </p>
  <solution>
    <div class="detailed-solution">
      <p>Explanation</p>
      <p>The decimal numerical system is base ten.</p>
      <p>The standard gravity constant is defined to be precisely 9.80665 m/s<sup>2</sup>.
      This is 9.80 to two decimal places. Entering 9.8 also works.</p>
      <p>By the distance formula, the distance between two points in the plane is
         the square root of the sum of the squares of the differences of each coordinate.
        Even though an exact numerical value is checked in this case, the
        easiest way to enter this answer is to type
        <code>sqrt(pi^2+e^2)</code> into the editor.
        Other answers like <code>sqrt((pi-0)^2+(0-e)^2)</code> also work.
      </p>
    </div>
  </solution>
  </problem>

.. _Numerical Input Problem XML:

===========================
Numerical Input Problem XML
===========================

Templates
---------

The following templates represent problems with and without a decimal or percentage tolerance.

Problem with no tolerance
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: xml

  <p>TEXT OF PROBLEM
      <numericalresponse answer="ANSWER (NUMBER)">
          <formulaequationinput label="TEXT OF PROBLEM"/>
      </numericalresponse>
  </p>
   
    <solution>
    <div class="detailed-solution">
    <p>TEXT OF SOLUTION</p>
    </div>
  </solution>
  </problem>

Problem with a decimal tolerance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: xml

  <problem>
   
    <p>TEXT OF PROBLEM
    <numericalresponse answer="ANSWER (NUMBER)">
      <responseparam type="tolerance" default="NUMBER (DECIMAL, e.g., .02)" />
      <formulaequationinput label="TEXT OF PROBLEM"/>
    </numericalresponse>
  </p>
   
    <solution>
    <div class="detailed-solution">
    <p>TEXT OF SOLUTION</p>
    </div>
  </solution>
  </problem>

Problem with a percentage tolerance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: xml

  <problem>
   
   <p>TEXT OF PROBLEM
    <numericalresponse answer="ANSWER (NUMBER)">
      <responseparam type="tolerance" default="NUMBER (PERCENTAGE, e.g., 3%)" />
      <formulaequationinput label="TEXT OF PROBLEM"/>
    </numericalresponse>
   </p>

    <solution>
    <div class="detailed-solution">
    <p>TEXT OF SOLUTION</p>
    </div>
  </solution>
  </problem>

Answer created with a script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: xml

  <problem>

  <!-- Use python script spacing. The following should not be indented! -->
  <script type="loncapa/python">
  computed_response = math.sqrt(math.fsum([math.pow(math.pi,2), math.pow(math.e,2)]))
  </script>

  <p>TEXT OF PROBLEM
      <numericalresponse answer="$computed_response">
          <responseparam type="tolerance" default="0.0001" />
          <formulaequationinput label="TEXT OF PROBLEM"/>
      </numericalresponse>
  </p>

    <solution>
    <div class="detailed-solution">
     <p>TEXT OF SOLUTION</p>
    </div>
  </solution>
  </problem>

Tags
----

* ``<numericalresponse>`` (required): Specifies that the problem is a numerical input problem.
* ``<formulaequationinput />`` (required): Provides a response field where the student enters a response.
* ``<responseparam>`` (optional): Specifies a tolerance, or margin of error, for an answer.
* ``<script>`` (optional):

.. note:: Some older problems use the ``<textline math="1" />`` tag instead of the ``<formulaequationinput />`` tag. However, the ``<textline math="1" />`` tag has been deprecated. All new problems should use the ``<formulaequationinput />`` tag.

**Tag:** ``<numericalresponse>``

Specifies that the problem is a numerical input problem. The ``<numericalresponse>`` tag is similar to the ``<formularesponse>`` tag, but the ``<numericalresponse>`` tag does not allow unspecified variables.

  Attributes

  .. list-table::
     :widths: 20 80

     * - Attribute
       - Description
     * - answer (required)
       - The correct answer to the problem, given as a mathematical expression. 

  .. note:: If you include a variable name preceded with a dollar sign ($) in the problem, you can include a script in the problem that computes the expression in terms of that variable.

  The grader evaluates the answer that you provide and the student's response in the same way. The grader also automatically simplifies any numeric expressions that you or a student provides. Answers can include simple expressions such as "0.3" and "42", or more complex expressions such as "1/3" and "sin(pi/5)". 

  Children
  
  * ``<responseparam>``
  * ``<formulaequationinput>``

**Tag:** * ``<formulaequationinput>``

Creates a response field in the LMS where students enter a response.

  Attributes

  .. list-table::
     :widths: 20 80

     * - size (optional)
       - Defines the width, in characters, of the response field in the LMS.
  
  Children

  (none)

**Tag:** ``<responseparam>``

Specifies a tolerance, or margin of error, for an answer.

  Attributes

  .. list-table::
     :widths: 20 80

     * - type (optional)
       - "tolerance": Defines a tolerance for a number
     * - default (optional)
       - A number or a percentage specifying a numerical or percent tolerance.

  Children
  
  (none)

**Tag:** ``<script>``

Specifies a script that the grader uses to evaluate a student's response. A problem behaves as if all of the code in all of the script tags were in a single script tag. Specifically, any variables that are used in multiple ``<script>`` tags share a namespace and can be overriden.

As with all Python, indentation matters, even though the code is embedded in XML.

  Attributes

  .. list-table::
     :widths: 20 80

     * - type (required)
       - Must be set to "loncapa/python".

  Children
  
  (none)

==================
Student Answers
==================

.. _Math Expression Syntax:

Math Expression Syntax
----------------------

In numerical input problems, the **student's input** may be more complicated than a
simple number. Expressions like ``sqrt(3)`` and even ``1+e^(sin(pi/2)+2*i)``
are valid, and evaluate to 1.73 and -0.13 + 2.47i, respectively.

A summary of the syntax follows:

Numbers
~~~~~~~

Accepted number types:

- Integers: '2520'
- Normal floats: '3.14'
- With no integer part: '.98'
- Scientific notation: '1.2e-2' (=0.012)
- More s.n.: '-4.4e+5' = '-4.4e5' (=-440,000)
- Appending SI suffixes: '2.25k' (=2,250). The full list:

  ====== ========== ===============
  Suffix Stands for One of these is
  ====== ========== ===============
  %      percent    0.01 = 1e-2
  k      kilo       1000 = 1e3
  M      mega       1e6
  G      giga       1e9
  T      tera       1e12
  c      centi      0.01 = 1e-2
  m      milli      0.001 = 1e-3
  u      micro      1e-6
  n      nano       1e-9
  p      pico       1e-12
  ====== ========== ===============

The largest possible number handled currently is exactly the largest float
possible (in the Python language). This number is 1.7977e+308. Any expression
containing larger values will not evaluate correctly, so it's best to avoid
this situation.

Default Constants
~~~~~~~~~~~~~~~~~

Simple and commonly used mathematical/scientific constants are included by
default. These include:

- ``i`` and ``j`` as ``sqrt(-1)``
- ``e`` as Euler's number (2.718...)
- ``pi``
- ``k``: the Boltzmann constant (~1.38e-23 in Joules/Kelvin)
- ``c``: the speed of light in m/s (2.998e8)
- ``T``: the positive difference between 0K and 0°C (285.15)
- ``q``: the fundamental charge (~1.602e-19 Coloumbs)

Operators and Functions
~~~~~~~~~~~~~~~~~~~~~~~

The normal operators apply (with normal order of operations):
``+ - * / ^``. Also provided is a special "parallel resistors" operator given
by ``||``. For example, an input of ``1 || 2`` would represent the resistance
of a pair of parallel resistors (of resistance 1 and 2 ohms), evaluating to 2/3
(ohms).

At the time of writing, factorials written in the form '3!' are invalid, but
there is a workaround. Students can specify ``fact(3)`` or ``factorial(3)`` to
access the factorial function.

The default included functions are the following:

- Trig functions: sin, cos, tan, sec, csc, cot
- Their inverses: arcsin, arccos, arctan, arcsec, arccsc, arccot
- Other common functions: sqrt, log10, log2, ln, exp, abs
- Factorial: ``fact(3)`` or ``factorial(3)`` are valid. However, you must take
  care to only input integers. For example, ``fact(1.5)`` would fail.
- Hyperbolic trig functions and their inverses: sinh, cosh, tanh, sech, csch,
  coth, arcsinh, arccosh, arctanh, arcsech, arccsch, arccoth



.. _Math Expression Input:

Math Expression Input
---------------------

In math expression input problems, students enter text that represents a mathematical expression into a field, and the LMS changes that text to a symbolic expression that appears below that field. 


.. image:: ../Images/MathExpressionInputExample.png
 :alt: Image of math expression input problem

Unlike numerical input problems, which only allow integers and a few select constants, math expression problems can include unknown variables and more complicated symbolic expressions. The grader uses a numerical sampling to determine whether the student's response matches the instructor-provided math expression, to a specified numerical tolerance. The instructor must specify the allowed variables in the expression as well as the range of values for each variable.

.. warning:: Math expression input problems cannot currently include negative numbers raised to fractional powers, such as (-1)^(1/2). Math expression input problems can include complex numbers raised to fractional powers, or positive non-complex numbers raised to fractional powers.

When you create a math expression input problem in Studio, you'll use `MathJax <http://www.mathjax.org>`_ to change your plain text into "beautiful math." For more information about how to use MathJax in Studio, see :ref:`MathJax in Studio`.



Create a Math Expression Input Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a math expression input problem:

#. In the unit where you want to create the problem, click **Problem**
   under **Add New Component**, and then click the **Advanced** tab.
#. Click **Math Expression Input**.
#. In the component that appears, click **Edit**.
#. In the component editor, replace the example code with your own code.
#. Click **Save**.

**Problem Code**

.. code-block:: xml

  <problem>
    <p>Some problems may ask for a mathematical expression. Practice creating mathematical expressions by answering the questions below.</p>

    <p>Write an expression for the product of R_1, R_2, and the inverse of R_3.</p>
    <formularesponse type="ci" samples="R_1,R_2,R_3@1,2,3:3,4,5#10" answer="$VoVi">
      <responseparam type="tolerance" default="0.00001"/>
      <formulaequationinput size="40" label="Enter the equation"/>
    </formularesponse>

  <script type="loncapa/python">
  VoVi = "(R_1*R_2)/R_3"
  </script>

    <p>Let <i>x</i> be a variable, and let <i>n</i> be an arbitrary constant. What is the derivative of <i>x<sup>n</sup></i>?</p>
  <script type="loncapa/python">
  derivative = "n*x^(n-1)"
  </script>
    <formularesponse type="ci" samples="x,n@1,2:3,4#10" answer="$derivative">
      <responseparam type="tolerance" default="0.00001"/>
      <formulaequationinput size="40"  label="Enter the equation"/>
    </formularesponse>

    <solution>
      <div class="detailed-solution">
        <p>Explanation or Solution Header</p>
        <p>Explanation or solution text</p>
      </div>
    </solution>
  </problem>

**Notes for Students**

When you answer a math expression input problem, follow these guidelines.

* Use standard arithmetic operation symbols.
* Indicate multiplication explicitly by using an asterisk (*).
* Use a caret (^) to raise to a power.
* Use an underscore (_) to indicate a subscript.
* Use parentheses to specify the order of operations.

The LMS automatically converts the following Greek letter names into the corresponding Greek characters when a student types them in the answer field:

.. list-table::
   :widths: 20 20 20 20
   :header-rows: 0

   * - alpha
     - beta
     - gamma
     - delta
   * - epsilon
     - varepsilon
     - zeta
     - eta
   * - theta
     - vartheta
     - iota
     - kappa
   * - lambda
     - mu
     - nu
     - xi
   * - pi
     - rho
     - sigma
     - tau
   * - upsilon
     - phi
     - varphi
     - chi
   * - psi
     - omega
     - 
     - 

note:: ``epsilon`` is the lunate version, whereas ``varepsilon`` looks like a backward 3.


.. _Math Expression Input Problem XML:

==================================
Math Expression Input Problem XML
==================================

Templates
---------

.. code-block:: xml

  <problem>
    <p>Write an expression for the product of R_1, R_2, and the inverse of R_3.</p>
    <formularesponse type="ci" samples="R_1,R_2,R_3@1,2,3:3,4,5#10" answer="R_1*R_2/R_3">
      <responseparam type="tolerance" default="0.00001"/> 
      <formulaequationinput size="40" />
    </formularesponse>
  </problem>

.. code-block:: xml

  <problem>
    <p>Problem text</p>
    <formularesponse type="ci" samples="VARIABLES@LOWER_BOUNDS:UPPER_BOUNDS#NUMBER_OF_SAMPLES" answer="$VoVi">
      <responseparam type="tolerance" default="0.00001"/>
      <formulaequationinput size="20"  label="Enter the equation"/>
    </formularesponse>

  <script type="loncapa/python">
  PYTHON SCRIPT
  </script>

    <solution>
      <div class="detailed-solution">
        <p>Explanation or Solution Header</p>
        <p>Explanation or solution text</p>
      </div>
    </solution>
  </problem>

Tags
----

* ``<formularesponse>``
* ``<formulaequationinput />``
* ``<responseparam>``
* ``<script>``

**Tag:** ``<formularesponse>``

Specifies that the problem is a math expression input problem. The ``<formularesponse>`` tag is similar to ``<numericalresponse>``, but ``<formularesponse>`` allows unknown variables.

  Attributes

  **type**: Can be "cs" (case sensitive, the default) or "ci" (case insensitive, so that capitalization doesn't matter in variable names).

  **answer**: The correct answer to the problem, given as a mathematical expression. If you precede a variable name in the problem with a dollar sign ($), you can include a script in the problem that computes the expression in terms of that variable.

  **samples**: Specifies important information about the problem in four lists:

    * **variables**: A set of variables that students can enter.
    * **lower_bounds**: For every defined variable, a lower bound on the numerical tests to use for that variable.
    * **upper_bounds**: For every defined variable, an upper bound on the numerical tests to use for that variable.
    * **num_samples**: The number of times to test the expression.

    Commas separate items inside each of the four individual lists, and the at sign (@), colon (:), and pound sign (#) characters separate the four lists. The format is the following:

    ``"variables@lower_bounds:upper_bounds#num_samples``

    For example, a ``<formularesponse>`` tag that includes the **samples** attribute may look like either of the following.

    ``<formularesponse samples="x,n@1,2:3,4#10">``

    ``<formularesponse samples="R_1,R_2,R_3@1,2,3:3,4,5#10">``

  Children

  * ``<formulaequationinput />``

**Tag:** ``<formulaequationinput />``

Creates a response field where a student types an answer to the problem in plain text, as well as a second field below the response field where the student sees a typeset version of the plain text. The parser that renders the student's plain text into typeset math is the same parser that evaluates the student's response for grading.

  Attributes

  .. list-table::
     :widths: 20 80

     * - Attribute
       - Description
     * - size (optional)
       - Specifies the width, in characters, of the response field where students enter answers.

  Children
  
  (none)

**Tag:** ``<responseparam>``

Used to define an upper bound on the variance of the numerical methods used to approximate a test for equality.

  Attributes

  .. list-table::
     :widths: 20 80

     * - Attribute
       - Description
     * - default (required)
       - A number or a percentage specifying how close the student and grader expressions must be. Failure to include a tolerance leaves expressions vulnerable to unavoidable rounding errors during sapling, causing some student input to be graded as incorrect, even if it is algebraically equivalent to the grader's expression.
     * - type
       - "tolerance"--defines a tolerance for a number

  Children
  
  (none)



