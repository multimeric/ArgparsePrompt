from argparse_prompt import PromptParser

parser = PromptParser()
parser.add_argument('--something', '-s', type=int)
parser.parse_args([])
