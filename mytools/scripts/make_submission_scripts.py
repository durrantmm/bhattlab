import argparse




if __name__ == "__main__":

    # setup the option parser
    parser = argparse.ArgumentParser(description='Quickly get the taxon id for a given')
    parser.add_argument('-c','--commands', required = True,
                        help='FILL THIS OUT')
    parser.add_argument('-t', '--time', required=True,
                        help='FILL THIS OUT')
    parser.add_argument('-m', '--memory', required=True,
                        help='FILL THIS OUT')
    parser.add_argument('-e', '--email', required=True,
                        help='FILL THIS OUT')


    args = parser.parse_args()
    args = vars(args)

    print args