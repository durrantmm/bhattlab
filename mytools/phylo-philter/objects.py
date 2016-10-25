

class pairedEnd:

    def __init__(self, read1_in, read2_in):
        self.read1 = read1_in
        self.read2 = read2_in

        self.read1_title = read1_in[0]
        self.read2_title = read2_in[0]

        self.read1_seq = read1_in[1]
        self.read2_seq = read1_in[1]

        raise ValueError("The input information does not represent a valid paired-"
                         "end read")



    def __str__(self):
        return "\n".join(["\n".join(self.read1), "\n".join(self.read2)])

    def getTitles(self):
        return [self.read1_title, self.read2_title]

    def getSequences(self):
        return [self.read1_title, self.read2_title]
