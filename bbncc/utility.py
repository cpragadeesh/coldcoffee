def tokenize_file(source):

	tokenized_source = []

	with open(source, "r") as f:
		source_content = f.read()

		source_content = source_content.replace('\n', '')
		source_content = source_content.replace(' ', '')
		source_content = source_content.replace('\t', '')
		source_content = source_content.replace('{', ';')
		source_content = source_content.replace('}', '')

		tokenized_source = source_content.split(";")

		return '\n'.join(tokenized_source)
