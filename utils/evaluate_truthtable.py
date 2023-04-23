def evaluate_answers(gpt_responses, actual_proofs):
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
        if validate_proof(gpt_response.strip(), actual_proof.strip()):
            num_correct += 1

    accuracy = num_correct / total_proofs

    return accuracy

def validate_proof(gpt_proof, actual_proof):
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
        if not validate_line(gpt_line, actual_line):
            return False

    # All lines match, so the proof is valid
    return True

def validate_line(gpt_line, actual_line):
    """
    Validate whether a single line of a GPT-generated proof matches the corresponding line in the actual proof.

    Parameters:
    gpt_line (str): A string representing a single line of the GPT-generated proof.
    actual_line (str): A string representing the corresponding line in the actual proof.

    Returns:
    A boolean indicating whether the GPT-generated line matches the actual line.
    """
    # Check if the line is a valid rule of inference
    if not is_valid_rule(gpt_line):
        return False

    # Check if the line matches the actual line
    return gpt_line.strip().lower() == actual_line.strip().lower()

def is_valid_rule(line):
    """
    Check if a single line of a GPT-generated proof represents a valid rule of inference.

    Parameters:
    line (str): A string representing a single line of the GPT-generated proof.

    Returns:
    A boolean indicating whether the line represents a valid rule of inference.
    """
    # List of valid rules of inference
    valid_rules = [
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

    # Check if the line matches any of the valid rules
    for rule in valid_rules:
        if rule in line.lower():
            return True

    # Line does not match any valid rule
    return False