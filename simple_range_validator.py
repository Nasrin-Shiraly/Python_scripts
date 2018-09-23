import functools
import sys


def argument_range_validator(_func=None, **deco_kwargs):
    def argument_range_validator_decorator(func):

        if not __debug__:
            """
            Making sure this doesn't run when we're not debugging, e.g on production. comment this is you're not running the code in debug mode
            """
            return func
        else:
            @functools.wraps(func)
            def argument_range_validator_wrapper(*args, **kwargs):
                code = func.__code__ if sys.version_info[0] == 3 else func.func_code
                all_args = code.co_varnames[:code.co_argcount]
                local_variable = locals()

                """
                below is one solution to make a dictionary of items
                # value_dictionary = dict()
                # value_dictionary = local_variable['kwargs']
                # i = 0
                # for each in all_args:
                #     if each not in value_dictionary:
                #         value_dictionary[each] = local_variable['args'][i]
                #         i += 1
                
                and then pass value_dictionary to return func(**value_dictionary)
                """

                """
                Below is just the above commented code with a compressed code
                """
                positional_args = [each for each in list(all_args) if each not in list(local_variable['kwargs'].keys())]
                value_dictionary = local_variable['kwargs']
                positional_args_dictionary = dict(zip(positional_args, local_variable['args']))
                value_dictionary_args = {**value_dictionary, **positional_args_dictionary}

                """
                one way for validating arguments is to add conditions here. 
                I didn't add them here because I've also used factory, so I didn't need to check here.
                Here we can have some validations. For example you can single out functions and their arguments:
                
                if func.__name__ == 'test_func_1' and a<10:
                    throw some error!
                    
                or maybe we just have generic rules and regardless of the function we want to check them:
                
                if pass is None:
                    throw some error!
                """
                for (argument, (condition_one, condition_two)) in deco_kwargs.items():

                    if argument in positional_args:
                        if positional_args_dictionary[argument] not in range(condition_one, condition_two):
                            """throw some exception, passing and just printing below for the sake of execution now"""
                            print(f"{positional_args_dictionary[argument]} was not in the acceptable range for {argument}!")

                    elif argument in local_variable['kwargs'].keys():
                        if value_dictionary[argument] not in range(condition_one, condition_two):
                            """throw some exception, passing and just printing below for the sake of execution now"""
                            print(f"{value_dictionary[argument]} was not in the acceptable range for {argument}!")

                return func(**value_dictionary_args)
            return argument_range_validator_wrapper

    if _func is None:
        return argument_range_validator_decorator
    else:
        return argument_range_validator_decorator(_func)

"""
1, 2, 3 will be passed as positional arguments to this function 
"""
@argument_range_validator(a=(2,10))
def test_func_1(a, b, c):
    x = a + b
    y = c
    print(f"{x} inside test_func_1")
    print(f"{y} inside test_func_1")


"""
(2, a=1, b=3) will be passed to this function and it's decorator will have no arguments
"""
@argument_range_validator
def test_func_2(a, b, c):
    x = a
    y = b
    z = c
    print(f"{x} inside test_func_2")
    print(f"{y} inside test_func_2")
    print(f"{z} inside test_func_2")

"""
Passing (2, c=3) to this one with no decorator arguments
"""
@argument_range_validator
def test_func_3(b, c, a=1):
    x = a
    y = b
    z = c
    print(f"{x} = a inside test_func_3")
    print(f"{y} = b inside test_func_3")
    print(f"{z} = c inside test_func_3")


"""
Neither the function nor the decorator will have any arguments for this test
"""
@argument_range_validator
def test_func_4():
    print(f"{test_func_4.__name__} says Hi!")


"""
Both the function and the decorator have arguments for this test
"""
@argument_range_validator(age=(18, 70), department=(40, 48))
def test_func_for_personnel(name, age, last_name, department):
    print(f"{name} {last_name} is {age} years old. She works at building No. {department}")


if __name__ == '__main__':

    test_func_1(1, 2, 3)
    test_func_2(2, a=1, b=3)
    test_func_3(2, c=3)
    test_func_4()
    test_func_for_personnel('Nasrin', 31, department=39, last_name='Shirali')
