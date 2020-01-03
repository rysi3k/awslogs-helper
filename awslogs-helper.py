#!/usr/bin/env python3

import sys
sys.path.append('/usr/local/Cellar/awslogs/0.11.0/libexec/lib/python3.7/site-packages')
sys.path.append('~/Library/Python/3.7/lib/python/site-packages')

from awslogs.core import AWSLogs
import awslogs.bin as AWSLogsBin

import inquirer

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Please provide log name")
        exit(1)

    searched = sys.argv[1];

    logs = AWSLogs()
    found = []

    for group in logs.get_groups():
        if searched in group:
            found.append(group)

    if len(found) == 0:
        print("No logs found for "+searched)
        exit(1)

    if len(found) == 1:
        group = found[0];

    if len(found) > 1:
        questions = [inquirer.List('group',
                                     message="%s%s%s (enter to select)" % ("\033[1m", "Which log?", "\033[0m"),
                                     choices=found,
                                     )
                    ]

        answers = None
        try:
            answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
            group = answers['group']
        except KeyboardInterrupt:
            print("Cancelled by user")
            sys.exit(1)

    opts = sys.argv[2:]
    opts.insert(0, sys.argv[0])
    opts.insert(1, "get")
    opts.insert(2, group)
    opts.insert(3, 'ALL')
    exit(AWSLogsBin.main(opts))
