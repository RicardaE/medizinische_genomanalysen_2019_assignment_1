import mysql.connector
import pysam

__author__ = 'Ricarda_Erhart'

##
## Concept:
## TODO
##


class Assignment1:

    def __init__(self):
        ## Your gene of interest
        self.gene = "PSMG1"


    def download_gene_coordinates(self, genome_reference, file_name):
        ## TODO concept

        print("Connecting to UCSC to fetch data")

        ## Open connection
        cnx = mysql.connector.connect(host='genome-mysql.cse.ucsc.edu', user='genomep', passwd='password', db=genome_reference)

        ## Get cursor
        cursor = cnx.cursor()

        ## Build query fields
        query_fields = ["refGene.name2",
                        "refGene.name",
                        "refGene.chrom",
                        "refGene.txStart",
                        "refGene.txEnd",
                        "refGene.strand",
                        "refGene.exonCount",
                        "refGene.exonStarts",
                        "refGene.exonEnds"]

        ## Build query
        query = "SELECT DISTINCT %s from refGene" % ",".join(query_fields)

        ## Execute query
        cursor.execute(query)

        ## Write to file
        ## TODO this may need some work
        with open(file_name, "w") as fh:
            for row in cursor:
                if row[0] == self.gene:
                    fh.write(str(row) + "\n")

        ## Close cursor & connection
        cursor.close()
        cnx.close()

        file = open(file_name, "r")
        UCSCstring = file.readline()
        UCSCstring = UCSCstring[2:-2]
        string = UCSCstring.replace('\'', '')
        global UCSClist
        UCSClist = string.split(', ')
        print("Done fetching data")

    def get_coordinates_of_gene(self):
        global UCSClist
        print("Start: ", UCSClist[3])
        print("Stop: ", UCSClist[4])

    def get_gene_symbol(self):
        global UCSClist
        print("Genesymbol: ", UCSClist[0])

    def get_sam_header(self):#
        samfile = pysam.AlignmentFile("chr21.bam", "rb")
        print('Header: ', samfile.header)
        samfile.close()

    def get_properly_paired_reads_of_gene(self):
        global UCSClist
        Start=int(UCSClist[3])
        End=int(UCSClist[4])
        samfile = pysam.AlignmentFile("chr21.bam", "rb")
        count = 0
        for read in samfile.fetch("chr21", Start, End):
            if read.is_proper_pair == True:
                count=count+1
        print('Properly Paired Reads: ', count)
        samfile.close()

    def get_gene_reads_with_indels(self):
        global UCSClist
        Start=int(UCSClist[3])
        End=int(UCSClist[4])
        samfile = pysam.AlignmentFile("chr21.bam", "rb")

        reads = []
        count = 0
        for pileupcolumn in samfile.pileup("chr21", Start, End):
            for pileupread in pileupcolumn.pileups:
                if pileupread.indel != 0 and pileupread not in reads:
                    reads.append(pileupread)
                    count=count+1
        print('Reads with indels: ', count)
        samfile.close()

    def calculate_total_average_coverage(self):
        samfile = pysam.AlignmentFile("chr21.bam", "rb")
        coveragesum=0
        length=0
        for pileupcolumn in samfile.pileup():
            coveragesum=coveragesum+pileupcolumn.n
            length=length+1
        average = coveragesum / length
        print('Total Coverage: ', average)
        samfile.close()

    def calculate_gene_average_coverage(self):
        global UCSClist
        Start=int(UCSClist[3])
        End=int(UCSClist[4])
        length=End-Start
        samfile = pysam.AlignmentFile("chr21.bam", "rb")
        sum=0
        for pileupcolumn in samfile.pileup("chr21", Start, End):
            sum=sum+pileupcolumn.n
        average = sum / length
        print('Gene Coverage: ', average)
        samfile.close()

    def get_number_mapped_reads(self):
        global UCSClist
        Start=int(UCSClist[3])
        End=int(UCSClist[4])
        samfile = pysam.AlignmentFile("chr21.bam", "rb")
        count=samfile.count('chr21', Start, End)
        print('Number of mapped reads: ', count)
        samfile.close()

    def get_region_of_gene(self):
        global UCSClist
        print("Exonstarts: ", UCSClist[7])
        print("Exonends: ", UCSClist[8])


    def get_number_of_exons(self):
        global UCSClist
        print("Number of Exons: ", UCSClist[6])


    def print_summary(self):
        print("Print all results here")
        assignment1 = Assignment1()
        UCSClist = []
        assignment1.download_gene_coordinates('hg38', 'Infofile')
        assignment1.get_coordinates_of_gene()
        assignment1.get_gene_symbol()
        assignment1.get_number_of_exons()
        assignment1.get_region_of_gene()
        assignment1.get_sam_header()
        assignment1.get_number_mapped_reads()
        assignment1.calculate_gene_average_coverage()
        assignment1.get_properly_paired_reads_of_gene()
        assignment1.get_gene_reads_with_indels()
        assignment1.calculate_total_average_coverage()

def main():
    print("Assignment 1")
    assignment1 = Assignment1()
    assignment1.print_summary()
    print("Done with assignment 1")


if __name__ == '__main__':
    main()
