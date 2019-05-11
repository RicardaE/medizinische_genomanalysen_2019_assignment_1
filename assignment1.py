import mysql.connector

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
                        
    def get_sam_header(self):
        print("todo")
        #pysam
        
    def get_properly_paired_reads_of_gene(self):
        print("todo")
        #pysam

    def get_gene_reads_with_indels(self):
        print("todo")
        
    def calculate_total_average_coverage(self):
        print("todo")
        #pybedtools
        
    def calculate_gene_average_coverage(self):
        print("todo")
        
    def get_number_mapped_reads(self):
        print("todo")

    def get_region_of_gene(self):
        print("todo")
        
    def get_number_of_exons(self):
        print("ads")
    
    
    def print_summary(self):
        print("Print all results here")
    
    
def main():
    print("Assignment 1")
    UCSClist=[]
    assignment1 = Assignment1()
    assignment1.download_gene_coordinates('hg38', 'Infofile')
    assignment1.print_summary()
    assignment1.get_coordinates_of_gene()
    assignment1.get_gene_symbol()
    
    
    print("Done with assignment 1")
    
        
if __name__ == '__main__':
    main()
    
    
