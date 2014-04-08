
.. _Appendix E:

################################
APPENDIX E: Problem and Tool XML
################################

This appendix provides information about the XML tags for most problem and tool types in Studio:

* :ref:`General`
* :ref:`Checkbox Problem XML`
* :ref:`Chemical Equation Problem XML`
* :ref:`Drag and Drop Problem XML`
* :ref:`Dropdown Problem XML`
* :ref:`Image Mapped Input Problem XML`
* :ref:`JS Input Problem XML`
* :ref:`Multiple Choice Problem XML`
* :ref:`Numerical Input Problem XML`
* :ref:`Math Expression Input Problem XML`
* :ref:`Text Input Problem XML`

.. _General:

=======
General
=======
 
Most problems have the following tags.

.. list-table::
   :widths: 20 80

   * - ``<problem> </problem>``
     - These must be the first and last tags for any content created in the Advanced Editor in a Problem component.
   * - ``<startouttext/>``
     - The ``<startouttext />`` tag indicates the beginning of a line or block of text.
   * - ``<endouttext/>``
     - The ``<endouttext />`` tag indicates the end of a line or block of text.
   * - ``<solution> <div class="detailed-solution"> </div> </solution>`` (optional)
     - If you want to include more information in the problem, such as a detailed explanation of the problem's answer, you'll enter the text between the two ``<div>`` tags, which are inside the ``<solution>`` tags. (These tags do not have to be on the same line.)

Additionally, all problems must include a **label** attribute. This attribute adds a descriptive label that helps visually impaired students navigate through the problem.

You'll add a **label** attribute to one of the XML tags for the problem. Each example problem below includes a label.




.. _Chemical Equation Problem XML:

=============================
Chemical Equation Problem XML
=============================

Template
--------

.. code-block:: xml

  <problem>
    <startouttext/>
    <p>Problem text</p>

    <customresponse>
      <chemicalequationinput size="NUMBER" label="LABEL TEXT"/>
      <answer type="loncapa/python">

  if chemcalc.chemical_equations_equal(submission[0], 'TEXT REPRESENTING CHEMICAL EQUATION'):
      correct = ['correct']
  else:
      correct = ['incorrect']

      </answer>
    </customresponse>

    <endouttext/>
  
   <solution>
   <div class="detailed-solution">
   <p>Solution or Explanation Header</p>
   <p>Solution or explanation text</p>
   </div>
   </solution>
  </problem>

Tags
----
* ``<customresponse>``: Indicates that this problem has a custom response. 
* ``<chemicalequationinput>``: Specifies that the answer to this problem is a chemical equation. 
* ``<answer type=loncapa/python>``: Contains the Python script that grades the problem.

**Tag:** ``<customresponse>``

Indicates that this problem has a custom response. The ``<customresponse>`` tags must surround the ``<chemicalequation>`` tags.

  Attributes

  (none)

  Children

  * ``<chemicalequationinput>``
  * ``<answer>``

**Tag:** ``<chemicalequationinput>``

Indicates that the answer to this problem is a chemical equation and creates a response field where the student enters an answer.

  Attributes

  .. list-table::
     :widths: 20 80

     * - Attribute
       - Description
     * - size 
       - Specifies the size of the response field, in characters.
     * - label (required)
       - Contains the text of the principal question in the problem.

  Children
  
  (none)

**Tag:** ``<answer>``

Contains the Python script that grades the problem.

  Attributes

  .. list-table::
     :widths: 20 80

     * - Attribute
       - Description
     * - type (required) 
       - Must be "loncapa/python".

  Children
  
  (none)
     









