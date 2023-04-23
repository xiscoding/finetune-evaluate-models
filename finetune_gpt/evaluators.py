class Eval_rulofinf:
    def __init__(self):
        # List of valid rules of inference
        self.valid_rules = [
            "modus ponens",
            "modus tollens",
            "hypothetical syllogism",
            "disjunctive syllogism",
            "addition",
            "simplification",
            "conjunction",
            "resolution",
            "equivalence",
            "negation introduction",
            "negation elimination",
            "double negative elimination",
            "De Morgan's law",
            "transposition",
            "material implication",
            "exportation",
            "importation",
            "distribution"
        ]

    def evaluate_answers(self, gpt_responses, actual_proofs):
        """
        Evaluate the accuracy of GPT-generated answers against actual proofs.

        Parameters:
        gpt_responses (list): A list of strings representing the GPT-generated responses.
        actual_proofs (list): A list of strings representing the actual proofs.

        Returns:
        A float between 0 and 1 representing the percentage of correct proofs.
        """
        num_correct = 0
        total_proofs = len(gpt_responses)

        for gpt_response, actual_proof in zip(gpt_responses, actual_proofs):
            if self.validate_proof(gpt_response.strip(), actual_proof.strip()):
                num_correct += 1

        accuracy = num_correct / total_proofs

        return accuracy

    def validate_proof(self, gpt_proof, actual_proof):
        """
        Validate whether a GPT-generated proof matches the actual proof.

        Parameters:
        gpt_proof (str): A string representing the GPT-generated proof.
        actual_proof (str): A string representing the actual proof.

        Returns:
        A boolean indicating whether the GPT-generated proof matches the actual proof.
        """
        gpt_lines = gpt_proof.split('\n')
        actual_lines = actual_proof.split('\n')

        # Remove empty lines and leading/trailing whitespace
        gpt_lines = [line.strip() for line in gpt_lines if line.strip()]
        actual_lines = [line.strip() for line in actual_lines if line.strip()]

        # Check if the number of lines matches
        if len(gpt_lines) != len(actual_lines):
            return False

        # Check if each line matches the corresponding line in the actual proof
        for gpt_line, actual_line in zip(gpt_lines, actual_lines):
            if not self.validate_line(gpt_line, actual_line):
                return False

        # All lines match, so the proof is valid
        return True

    def validate_line(self, gpt_line, actual_line):
        """
        Validate whether a single line of a GPT-generated proof matches the corresponding line in the actual proof.

        Parameters:
        gpt_line (str): A string representing a single line of the GPT-generated proof.
        actual_line (str): A string representing the corresponding line in the actual proof.

        Returns:
        A boolean indicating whether the GPT-generated line matches the actual line.
        """
        # Check if the line is a valid rule of inference
        if not self.is_valid_rule(gpt_line):
            return False

        # Check if the line matches the actual line
        if gpt_line.strip().lower() == actual_line.strip().lower():
            return True
        
        return True

    def is_valid_rule(self, line):
        """
        Check if a single line of a GPT-generated proof represents a valid rule of inference.

        Parameters:
        line (str): A string representing a single line of the GPT-generated proof.

        Returns:
        A boolean indicating
        whether the line represents a valid rule of inference.
        """
        # Check if the line matches any of the valid rules
        for rule in self.valid_rules:
            if rule in line.lower():
                return True
        # Line does not match any valid rule
        return False
    
class EvalProof:
    def __init__(self, premises, conclusion):
        self.premises = premises
        self.conclusion = conclusion

    def validate_proof(self, steps):
        # Create a dictionary of available variables
        variables = {}
        for premise in self.premises:
            variables.update(premise)
        variables.update(self.conclusion)

        # Check each step in the proof
        for i, step in enumerate(steps, start=1):
            # Check if the step is a valid rule of inference
            if step[0] in ['modus ponens', 'modus tollens', 'hypothetical syllogism', 'disjunctive syllogism', 'constructive dilemma', 'destructive dilemma']:
                # Check that the step is valid based on the previous steps
                if not self.validate_rule(i, step, steps, variables):
                    return False
            # Check if the step is a valid line of logic
            else:
                # Check that the step is valid based on the previous steps and available variables
                if not self.validate_line(i, step, steps, variables):
                    return False

        # Check that the last step is the conclusion
        if steps[-1][1] != self.conclusion['conclusion']:
            return False

        return True

    def validate_rule(self, i, step, steps, variables):
        # Check that the rule is valid based on the previous steps and available variables
        if step[0] == 'modus ponens':
            if steps[step[1]-1][1] != f"{steps[step[2]-1][1]} → {step[3]}" or steps[step[2]-1][1] != variables[step[2]]:
                return False
        elif step[0] == 'modus tollens':
            if steps[step[1]-1][1] != f"{step[2]} → {steps[step[3]-1][1]}" or steps[step[3]-1][1] != f"¬{variables[step[3]]}":
                return False
        elif step[0] == 'hypothetical syllogism':
            if steps[step[1]-1][1] != f"{step[2]} → {step[3]}" or steps[step[2]-1][1] != f"{step[4]} → {variables[step[3]]}":
                return False
        elif step[0] == 'disjunctive syllogism':
            if steps[step[1]-1][1] != f"{step[2]} ∨ {step[3]}" or (variables[step[2]] == True and variables[step[3]] == True) or (variables[step[2]] == False and variables[step[3]] == False):
                return False
        elif step[0] == 'constructive dilemma':
            if steps[step[1]-1][1] != f"{step[2]} → {step[3]}" or steps[step[4]-1][1] != f"{step[5]} → {variables[step[3]]}" or (variables[step[2]] == False and variables[step[5]] == False):
                return False
        elif step[0] == 'destructive dilemma':
            if steps[step[1]-1][1] != f"{step[2]} → {step[3]}" or steps[step[4]-1][1] != f"{step[5]} → ¬{variables[step[3]]}" or steps[step[6]-1][1] != f"¬{variables[step[6]]} ∨ ¬{variables[step[5]]}" or (variables[step[2]] == False and variables[step[6]] == False):
                return False

        return True

    def validate_line(self, i, step, steps, variables):
        # Check that the logic of the step is valid based on the previous steps and available variables
        if step[1] in variables.keys():
            if variables[step[1]] != step[2]:
                return False
        elif step[2] in variables.keys():
            if variables[step[2]] != step[1]:
                return False
        elif step[1] in steps[i-2][1]:
            if steps[i-2][1] != f"{step[2]} ∧ {variables[step[1]]}":
                return False
        elif step[1] in steps[i-2][1] or step[2] in steps[i-2][1]:
            if steps[i-2][0] not in ['∨-elim', '∨-intro']:
                return False
        elif step[1] == f"¬{step[2]}" or step[2] == f"¬{step[1]}":
            if steps[i-2][1] != f"¬{step[2]}" and steps[i-2][1] != f"¬{step[1]}":
                return False
        elif step[1] == f"{step[2]} ∧ {variables[step[1]]}":
            if steps[i-2][1] != variables[step[1]]:
                return False
        elif step[1] == f"{step[2]} ∨ {variables[step[1]]}":
            if steps[i-2][0] != '∨-intro' or steps[i-2][1] not in [step[2], variables[step[1]]]:
                return False
        else:
            return False

        return True