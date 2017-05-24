from argparse_prompt import PromptParser

parser = PromptParser()
parser.add_argument('--something', '-s')
parser.parse_args([])
