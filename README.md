Before you start, these are applications that used to make this program :
-Jupyter notebook
-Anaconda Prompt or any terminal that can run python command
-Forest SDK (please download first at https://www.rigetti.com/forest)
-Visual Studio Code or any text editor

And these are the dependencies:
-Python version 3+
-Pyquil (you can install it via pip)
-Numpy
-Flask (you can install it via pip)

How to run Grover's Implementation Program :
-Clone this project
-Run forest-sdk.msi to install Forest SDK (for Windows)
-Open terminal (e.g. Command Prompt), run quantum virtual machine with command "qvm --server"
-Open other terminal, run quil compiler with command "quilc -S"
-Open Anaconda Prompt, go to directory where you save webservice.py
-Run the webservice with command "python webservice.py"
-Open your browser and go to localhost:5002
-There are 2 input, dataset and target, there are some rules you must follow for dataset:
---Separate the input with comma "," and don't use whitespace " "
---If you want to input character use quotation mark ''
---Make sure the target is in dataset
---The range input is from 0-1023
---e.g. for input : 
-----numbers only : 1,8,5,3
-----characters only : 'a','A','Z'
-----mixed input : 1,'1','+',10
-For target input, just input one target. E.g. : 1 or 'a'
-For output, there will be information result, amplitude graph, and user time

*Since qvm use port 5000 and flask also use port 5000, I change the port to 5002 for flask
*If you have any question, feel free to ask me through email : anthonyant97@gmail.com

R. Smith, M. J. Curtis and W. J. Zeng, "A Practical Quantum Instruction Set Architecture," (2016), 
  arXiv:1608.03355 [quant-ph], https://arxiv.org/abs/1608.03355


