__author__ = 'visoft'

import sf.fh as fh

def test_localConfigLoading():
    assert fh.localConfigObject is not None

def test_load_some_paths():
    import sf.fh as fh
    assert fh.localConfigObject.source_dir is not None

def test_how_to_write_a_file():
    file_name = fh.get_out_path("sample_writable_file.txt")
    with open(file_name,"w") as file:
        file.write("Some string in the file\n")

def test_are_the_paths_present():
    """
    TODO:
    Tests if the paths exist and the output path is writable
    """
    pass

