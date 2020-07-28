#!/usr/bin/python3

#Summarize complaints for each product-year in report
import csv
import math
import sys

#Include a rounding function that always rounds x.5 up to x+1
def round_half_up(n, decimals=0):
    multiplier=10**decimals
    return math.floor(n*multiplier+0.5)/multiplier

#Build a nested dictionary with product-years as 1st keys, companies as 2nd keys, and number of complaints as values
def nest(filename):
    company_complaints={}
    with open(filename) as csv_input_file:
        csv_reader=csv.reader(csv_input_file,delimiter=',')
    
        line_count=0
        for row in csv_reader:
            if line_count>0:
                product=row[1].lower()
                year=row[0][:4]
                company=row[7].lower()
                product_year=product+", "+year

                if not product_year in company_complaints:
                    company_complaints[product_year]={}
                    
                    company_complaints[product_year][company]=1
                else:
                    if not company in company_complaints[product_year]:
                        company_complaints[product_year][company]=1
                    else:
                        company_complaints[product_year][company]+=1

            line_count+=1
        return company_complaints

#Calculate the maximum and total complaints for each product-year and print to csv file
def organize(company_complaints,filename):
    with open(filename,'w',newline='') as csv_output_file:
        csv_writer=csv.writer(csv_output_file,delimiter=',')

        sorted_product_years=sorted(company_complaints.keys())
        for product_year_no in range(len(sorted_product_years)):
            product_year=sorted_product_years[product_year_no]
            product=sorted_product_years[product_year_no][:-6]
            if "," in product:
                product='\"'+product+'\"'
            year=sorted_product_years[product_year_no][-4:]
            product_year_total=sum(company_complaints[product_year].values())
            product_year_companies=len(company_complaints[product_year])
            product_year_max=max(company_complaints[product_year].values())
            product_year_high_per=round_half_up(100*product_year_max/product_year_total)
            csv_writer.writerow([product,year,product_year_total,product_year_companies,product_year_high_per])

#Summarize complaints
def summarize(input_filename,output_filename):
    company_complaints=nest(input_filename)
    organize(company_complaints,output_filename)
    
if __name__ == "__main__":
    input_filename=sys.argv[1]
    output_filename=sys.argv[2]
    summarize(input_filename,output_filename)




        
