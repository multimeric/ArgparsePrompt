from argparse_prompt import PromptParser

parser = PromptParser()
parser.add_argument('--argument', '-a', help='An argument you could provide', default='foo')
print(parser.parse_args().argument)
