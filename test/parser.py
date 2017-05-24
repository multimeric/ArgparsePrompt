from argparse_prompt import PromptParser

parser = PromptParser()
parser.add_argument('--something', '-s')
print(parser.parse_args())
