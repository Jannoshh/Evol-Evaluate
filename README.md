# Evolv-Evaluate

This project is a proof of concept for using Evolv-Instruct as a way to generate datasets for Evals. 

## Installation

- install pipenv: `pip install pipenv`
- create the virtual environment with pipenv: `pipenv install`
- change to the virtual environment: `pipenv shell` (in VS Code you can do this with `Ctrl+Shift+P` and then `Python: Select Interpreter` and then select the one with `pipenv` in the name)
- 

## Usage

- Copy the .env.template as .env and fill in the values
- Copy the input\template.json as input\XXX.json and enter the values that you want for your project:
  - "title": title of your project 
  - "desired_size_dataset": The size of the intermediate datasets that you want to generate  
  - "instruction": The goal of the project and how you would like the dataset to look. You can take inspiration by the examples in the input folder.  
  - "few_shots": few shots for the LM to learn from  
- Run create_datasets.py: this will create the intermediate datasets and save them in the results folder. The intermediate datasets are DS1 (using LM without few shots prompting), DS2 (using LM with few shots prompting), DS1_evolvinstruct (using Evolv-Instruct over the DS1 dataset), DS2_evolvinstruct (using Evolv-Instruct over the DS2 dataset).
- Run eliminator.py: this cleans the datasets. The cleaning criteria can be seen and expanded in the file itself.
- Run evaluator.py: this evaluates the questions in the datasets using an LM and create the final datasets with the questions that scored the best.


## Future Work
- Add more visualizations to compare better the scores of the questions.
- Expand the functionality to accommodate non-binary questions.
- Experiment further with various combinations of Evolv instructions.
- Conduct more extensive testing with different evaluators.
- Evaluate the performance of different Language Models.
