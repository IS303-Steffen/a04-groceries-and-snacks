max_score = 15  # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_student_code, format_error_message, exception_message_for_students
from conftest import default_module_to_test_2

# Checks if a correct dictionary is created given certain inputs
def test_06_dictionary_properly_updated(current_test_name, input_test_cases):
    try:
       # Ensure test_cases is valid and iterable
        if not isinstance(input_test_cases, list):
            input_test_case = {"id_input_test_case": None}
            exception_message_for_students(ValueError("input_test_cases should be a list of dictionaries. Contact your professor."), input_test_case, current_test_name) 
            return  # Technically not needed, as exception_message_for_students throws a pytest.fail Error, but included for clarity that this ends the test.

        for input_test_case in input_test_cases[2:4]:
            try:

                inputs = input_test_case["inputs"]
                # This provides a dictionary of dictionaries. Each key is a variable name,
                # the value is the actual dictionary we care about.
                expected_dictionaries = input_test_case["dicts"].values()

                # Normalize expected dictionaries
                normalized_expected_dicts = []
                for expected_dictionary in expected_dictionaries:
                    if expected_dictionary is not None:
                        normalized_expected_dict = {normalize_text(key): normalize_text(value) for key, value in expected_dictionary.items()}
                        normalized_expected_dicts.append(normalized_expected_dict)

                        expected_dicts_string = ''

                for idx, normalized_expected_dict in enumerate(normalized_expected_dicts, 1):
                    expected_dicts_string += f"Expected Dictionary {idx}: {normalized_expected_dict}\n\n"
                

                # Load in the student's code and get globals
                manager_payload = load_student_code(current_test_name, inputs, input_test_case, module_to_test=default_module_to_test_2)
                
                student_globals = manager_payload.get('module_globals')

                # Get the locals from 'main' function
                student_locals = student_globals.get('__main_locals__', {})

                # Find all variables in student's code that are of type dictionary
                student_dictionaries = {name: value for name, value in student_globals.items() if isinstance(value, dict) and name != "__builtins__" and name != "__main_locals__"}

                # Also include dictionaries from student_locals
                student_dictionaries.update({name: value for name, value in student_locals.items() if isinstance(value, dict)})

                # Assert that there is at least one dictionary
                assert student_dictionaries, format_error_message(
                        custom_message=(
                            f"The tests couldn't find any dictionary variables in your code.\n\n" 
                            f"Make sure you are storing the snacks/counts in a dictionary, or that you aren't overwriting "
                            f"your dictionary by calling another variable the same name as your dictionary.\n"),
                        current_test_name=current_test_name,
                        input_test_case=input_test_case,
                        display_inputs=True
                    )

                dictionary_match_found = False
                dictionary_length_matched = False
                student_dictionaries_string = ''  # Used to provide details if the test fails

                # Iterate over all dictionaries found in the student's code
                for dict_name, student_dict in student_dictionaries.items():
                    # String is useful for error reporting if test fails
                    normalized_student_dict = {normalize_text(key): normalize_text(value) for key, value in student_dict.items()}

                    student_dictionaries_string += f"{dict_name}: {normalized_student_dict}\n\n"

                    # Check if student_dict matches any of the expected dictionaries
                    for normalized_expected_dict in normalized_expected_dicts:
                        if 'starburst' in normalized_student_dict or input_test_case.get('id_input_test_case') == 3:
                            dictionary_match_found = True
                            break  # Stop once we find a matching dictionary
                    if dictionary_match_found:
                        break
                
                # If a dictionary with the correct value is found, make sure it has the proper number of elements too
                if dictionary_match_found:
                    if len(normalized_student_dict) == len(normalized_expected_dict):
                        dictionary_length_matched = True

                assert dictionary_match_found, format_error_message(
                    custom_message=(
                        f"None of the dictionaries found in your code "
                        f"had the expected updated value for this input test case.\n\n"
                        f"EXPECTED DICTIONARY VALUE:\n"
                        f"--------------------------\n"
                        f"The test expects your dictionary to have this value (ignoring capitalization / punctuation):\n\n"
                        f"starburst\n\n"
                        f"YOUR DICTIONARY VALUES:\n"
                        f"-----------------------\n"
                        f"Your dictionary/dictionaries (ignoring capitalization / punctuation) look like this:\n\n"
                        f"{student_dictionaries_string}\n"
                        f"Make sure you are correctly adding values to your dictionary, or "
                        f"that you aren't transforming the inputs in an unexpected way.\n"),
                    current_test_name=current_test_name,
                    input_test_case=input_test_case,
                    display_inputs=True
                )

                assert dictionary_length_matched, format_error_message(
                    custom_message=(
                        f"None of the dictionaries found in your code "
                        f"had the expected number of elements expected for this input test case.\n\n"
                        f"EXPECTED DICTIONARY ELEMENTS:\n"
                        f"-----------------------------\n"
                        f"The test expects your dictionary to have this # of elements:\n\n"
                        f"{len(normalized_expected_dict)}\n\n"
                        f"YOUR DICTIONARY VALUES:\n"
                        f"-----------------------\n"
                        f"Your dictionary has {len(normalized_student_dict)} elements and looks like this (ignoring capitalization / punctuation):\n\n"
                        f"{student_dictionaries_string}\n"
                        f"Make sure you are correctly adding values to your dictionary, or "
                        f"that you aren't transforming the inputs in an unexpected way.\n"),
                    current_test_name=current_test_name,
                    input_test_case=input_test_case,
                    display_inputs=True
                )

            # assert raises an AssertionError, but I don't want to actually catch it
            # this is just so I can have another Exception catch below it in case
            # anything else goes wrong.
            except AssertionError:
                raise
            
            except Exception as e:
                # Handle other exceptions
                exception_message_for_students(e, input_test_case)
    
    # assert raises an AssertionError, but I don't want to actually catch it
    # this is just so I can have another Exception catch below it in case
    # anything else goes wrong.
    except AssertionError:
        raise
    
    except Exception as e:
        # Handle other exceptions
        exception_message_for_students(e, input_test_case)