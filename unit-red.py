import os

def get_top_dir() -> str:
    """returns PWD if current directory is 'src' directory"""
    pwd:str = os.getcwd()
    if pwd.endswith('src'):
        return pwd
    elif os.path.isdir(pwd + '/src'):
        return pwd + '/src'
    else:
        print('"src" directory NOT FOUND')
        exit()

def mk_subdir(parentdir:str, subdir:str=None) -> str:
    """ returns tests directory"""
    if subdir:
        testdir:str = f'{parentdir}/{subdir}'
    else:
        # directory /tests/unit/ per https://docs.phpunit.de/en/12.4/organizing-tests.html
        testdir:str = f'{parentdir.split("src")[0]}tests/unit'
    os.makedirs(testdir,exist_ok=True)
    return testdir

def mk_testfile(srcfile:str, testdir:str) -> None:
    """ Makes test file for each PHP file in src."""
    if not srcfile.endswith('.php'): # Only make test files for PHP files
        return
    if '-' in srcfile: # Remove '-' and capitalize
        srcfile = srcfile.replace("-", " ").title().replace(" ", "")
    elif '_' in srcfile: # Remove '_' and capitalize
        srcfile = srcfile.replace("_", " ").title().replace(" ", "")
    elif srcfile.islower(): # Capitalize
        srcfile = srcfile.title()

    phpclassname:str = srcfile.split('.')[0] + 'Test' # rm '.php'from file name and add 'Test'
    targetfile:str = f'{testdir}/{phpclassname}.php' # PHP file name needs to match class name
    if os.path.isfile(targetfile): # Do not change existing files
        return
    
    testfile_content = f"""<?php declare(strict_types=1);
use PHPUnit\Framework\TestCase;
final class {phpclassname} extends TestCase
{{
    public function testDefaultFail(): void
    {{
        //Default Fail Test
        $this->assertTrue(false, 'Default Fail Test');
    }}
}}
"""

    with open(targetfile, 'a') as f:
       f.write(testfile_content)
    return

top:str = get_top_dir()
test_dir:dir = mk_subdir(top)

for root, dirs, files in os.walk(top):
    test_subdir = test_dir if root.endswith('src') else mk_subdir(test_dir, root.split('/src/')[-1])
    print(test_subdir)
    for name in files:
        mk_testfile(name, test_subdir)
