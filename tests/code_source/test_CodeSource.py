from project.code_source.CodeSource import CodeSource


def test_CodeSource():
    test_file_path = './tests/code_source/test_file.ppp'
    with open(test_file_path) as handle:
        source = CodeSource(handle)
        expected_text = 'sample text'

        char_list = []
        while True:
            try:
                char_list.append(next(source))
            except StopIteration:
                break

        assert ''.join(char_list) == expected_text
