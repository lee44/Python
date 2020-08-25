import pandas as pd
from bs4 import BeautifulSoup
import re
import string
import requests
import xlsxwriter

pd.options.display.float_format = '{:.0f}'.format

ticker = input("Input the ticker of the company you'd like to see the financials of: ")

def yahoo_financial_statements():
    is_link = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    bs_link = f'https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}'
    cf_link = f'https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}'

    statements_list = [is_link,bs_link,cf_link]

    headers = []
    temp_list = []
    label_list = []
    final = []
    index = 0

    df_lists = list()

    for link in statements_list:
        
        source = requests.get(link).text
        soup = BeautifulSoup(source,'lxml')
        
        features = soup.find_all('div', class_='D(tbr)')
        
        #create headers
        for item in features[0].find_all('div', class_='D(ib)'):
            headers.append(item.text)
            
        #statement contents
        while index <= len(features)-1:
            #filter for each line of the statement
            temp = features[index].find_all('div', class_='D(tbc)')
            for line in temp:
                #each item added to a temp list
                temp_list.append(line.text)
            #temp_list added to final list
            final.append(temp_list)
            #clear temp_list
            temp_list = []
            index+=1
        
        df = pd.DataFrame(final[1:])
        df.columns = headers
        # df.index = final[1]
        
        #Removes the commas from all the values
        def convert_to_numeric(column):

            first_col = [i.replace(',','') for i in column]
            second_col = [i.replace('-','') for i in first_col]
            final_col = pd.to_numeric(second_col)

            return final_col
        
        for column in headers[1:]:
            df[column] = convert_to_numeric(df[column])
        
        final_df = df.fillna('-')
        df_lists.append(final_df)
        
        #reset all lists
        headers = []
        temp_list = []
        label_list = []
        final = []
        index = 0

    return df_lists

financials = yahoo_financial_statements()

income_statement = financials[0]
balance_sheet = financials[1]
cash_flow_statement = financials[2]

# Convert income statement list to dataFrame
df_income_statement = pd.DataFrame(income_statement)
# Create a Pandas Excel writer using XlsxWriter as the engine.
income_statement_writer = pd.ExcelWriter('/Users/joshualee/Desktop/Stock_Financials/'+ticker+' income.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
df_income_statement.to_excel(income_statement_writer, index=False,sheet_name='Sheet1')

income_statement_worksheet = income_statement_writer.sheets['Sheet1']
income_statement_worksheet.write_comment('A2', 'All money collected by the company')
income_statement_worksheet.write_url('A2', "https://www.investopedia.com/terms/r/revenue.asp", string='Total Revenue')
income_statement_worksheet.write_comment('A3', 'Total costs from producing, marketing, and distributing products and services')
income_statement_worksheet.write_url('A3', "https://www.investopedia.com/terms/c/cost-of-revenue.asp", string='Cost of Revenue')
income_statement_worksheet.write_comment('A4', 'Total Revenue - Cost of Revenue')
income_statement_worksheet.write_url('A4', "https://www.investopedia.com/terms/g/grossprofit.asp#:~:text=Gross%20profit%20is%20the%20profit,)%20from%20revenue%20(sales).", string='Gross Profit')
income_statement_worksheet.write_comment('A5', 'Total costs for maintaining daily operations like rent, equipment, inventory, marketing, payroll, insurance, step costs, and funds allocated for research and development')
income_statement_worksheet.write_url('A5', "https://www.investopedia.com/terms/o/operating_expense.asp", string='Operating Expense')
income_statement_worksheet.write_comment('A6', 'Gross Income − Operating Expenses (increasing amount of operating income means that the company\'s management is generating more revenue while controlling expenses, productions costs, and overhead')
income_statement_worksheet.write_url('A6', "https://www.investopedia.com/terms/o/operatingincome.asp", string='Operating Income')
income_statement_worksheet.write_comment('A7', 'Expenses incurred from activities unrelated to core operations like monthly charges of interest payments on debt')
income_statement_worksheet.write_url('A7', "https://www.investopedia.com/terms/n/non-operating-expense.asp", string='Net Non Operating Interest Income Expense')
income_statement_worksheet.write_comment('A8', 'Company\'s income after all operating expenses, including interest and depreciation, have been deducted from total sales or revenues, but before income taxes have been subtracted.')
income_statement_worksheet.write_url('A8', "https://www.investopedia.com/terms/p/pretax-earnings.asp#:~:text=Pretax%20earnings%20is%20a%20company's,income%20taxes%20have%20been%20subtracted.&text=Also%20known%20as%20pretax%20income%20or%20earnings%20before%20tax%20(EBT).", string='Pretax Earnings')
income_statement_worksheet.write_comment('A9', 'Company\'s income after all operating expenses, including interest and depreciation, have been deducted from total sales or revenues, but before income taxes have been subtracted.')
income_statement_worksheet.write_url('A9', "https://www.investopedia.com/terms/p/pretax-earnings.asp#:~:text=Pretax%20earnings%20is%20a%20company's,income%20taxes%20have%20been%20subtracted.&text=Also%20known%20as%20pretax%20income%20or%20earnings%20before%20tax%20(EBT).", string='Pretax Income')
income_statement_worksheet.write_comment('A10', 'an amount set aside specifically to pay a company\'s income taxes')
income_statement_worksheet.write_url('A10', "https://www.freshbooks.com/hub/accounting/provisions-accounting#:~:text=Tax%20provisions%20are%20an%20amount,tax%20deductions%20it%20is%20claiming.", string='Tax Provision')
income_statement_worksheet.write_comment('A11', 'Revenue minus expenses, interest, and taxes')
income_statement_worksheet.write_url('A11', "https://www.investopedia.com/terms/n/netincome.asp", string='Net Income Common Stockholders')
income_statement_worksheet.write_comment('A12', 'Net Income that is adjusted by Dilution Adjustment for Diluted EPS computation')
income_statement_worksheet.write_url('A12', "https://www.tradingview.com/support/solutions/43000563516-diluted-net-income-available-to-common-stockholders/", string='Diluted NI Available to Com Stockholders')
income_statement_worksheet.write_comment('A13', 'measurement of the amount of a company\'s profit that can be allocated to one share of its common stock. Different from EPS')
income_statement_worksheet.write_url('A13', "https://www.investopedia.com/terms/b/basic-earnings-per-share.asp", string='Basic EPS')
income_statement_worksheet.write_comment('A14', 'Similar to Basic EPS but includes convertible securities(bonds and preferred stock which can be converted into common stock)')
income_statement_worksheet.write_url('A14', "https://www.investopedia.com/ask/answers/051115/what-difference-between-earnings-share-eps-and-diluted-eps.asp", string='Diluted EPS')
income_statement_worksheet.write_comment('A15', 'weighted average of outstanding shares, is a calculation that takes into consideration any changes in the number of outstanding shares over a specific reporting period. Used in Basic EPS')
income_statement_worksheet.write_url('A15', "http://www.dividendgangster.com/2012/10/14/basic-vs-diluted-weighted-average-number-of-shares/", string='Basic Average Shares')
income_statement_worksheet.write_comment('A16', 'same as Basic Average Shares but including convertible securities')
income_statement_worksheet.write_url('A16', "http://www.dividendgangster.com/2012/10/14/basic-vs-diluted-weighted-average-number-of-shares/", string='Diluted Average Shares')
income_statement_worksheet.write_comment('A17', 'total revenue - cost of goods - operating expenses. Shows amount of profit realized from a business\'s ongoing operations')
income_statement_worksheet.write_url('A17', "https://www.investopedia.com/terms/o/operatingincome.asp#:~:text=Operating%20income%20reports%20the%20amount,and%20subtracts%20all%20operating%20expenses.", string='Total Operating Income as Reported')
income_statement_worksheet.write_comment('A18','cost of operations that a company incurs to generate revenue')
income_statement_worksheet.write_url('A18', "https://www.investopedia.com/terms/e/expense.asp#:~:text=An%20expense%20is%20the%20cost,costs%20money%20to%20make%20money.%E2%80%9D&text=Businesses%20are%20allowed%20to%20write,and%20thus%20their%20tax%20liability.", string='Total Expenses')
income_statement_worksheet.write_comment('A19', 'Company has disposed-off assets that generated this much income and the only income from continuing operations should be expected')
income_statement_worksheet.write_url('A19', "https://xplaind.com/275683/discontinued-operations-income", string='Net Income From Continuing & Discontinued Operations')
income_statement_worksheet.write_comment('A20', 'represent a company\'s earnings that omit the effects of nonrecurring charges or gains e.g a company sells a piece of their property')
income_statement_worksheet.write_url('A20', "https://www.investopedia.com/terms/n/normalizedearnings.asp#:~:text=What%20are%20Normalized%20Earnings%3F,earnings%20from%20its%20normal%20operations.", string='Normalized Income')
income_statement_worksheet.write_comment('A21', 'amount paid to the company for lending its money or letting another entity use its funds')
income_statement_worksheet.write_url('A21', "https://corporatefinanceinstitute.com/resources/knowledge/finance/interest-income/#:~:text=Interest%20income%20is%20usually%20taxable,operating%20and%20non%2Doperating%20activities.", string='Interest Income')
income_statement_worksheet.write_comment('A22', 'represents interest payable on any borrowings – bonds, loans, convertible debt or lines of credit')
income_statement_worksheet.write_url('A22', "https://www.investopedia.com/terms/i/interestexpense.asp#:~:text=Interest%20expense%20is%20a%20non,principal%20amount%20of%20the%20debt.", string='Interest Expense')
income_statement_worksheet.write_comment('A23', 'reflects the difference between the revenue generated from a bank's interest-bearing assets and expenses associated with paying on its interest-bearing liabilities')
income_statement_worksheet.write_url('A23', "https://www.investopedia.com/terms/n/net-interest-income.asp#:~:text=Net%20interest%20income%20is%20a,on%20its%20interest%2Dbearing%20liabilities.&text=The%20liabilities%20are%20interest%2Dbearing%20customer%20deposits.", string='Net Interest Income')
income_statement_worksheet.write_comment('A24', 'revenue - expenses but excluded tax and interest')
income_statement_worksheet.write_url('A24', "https://www.investopedia.com/terms/e/ebit.asp#:~:text=EBIT%20(earnings%20before%20interest%20and,and%20tax%20expenses%20impacting%20profit.", string='EBIT')
income_statement_worksheet.write_comment('A25', 'revenue - expenses but excluded tax, interest on company debt, and amortization, which is the accounting practice of writing off the cost of an asset over a period of years')
income_statement_worksheet.write_url('A25', "https://www.investopedia.com/terms/e/ebita.asp", string='EBITDA')
income_statement_worksheet.write_comment('A26', 'Should match Cost of Revenue. Used for double checking the correct amount of Cost of Revenue')
income_statement_worksheet.write_url('A26', "https://smallbusiness.chron.com/definition-revenue-reconciliation-31190.html", string='Reconciled Cost of Revenue')
income_statement_worksheet.write_comment('A27', 'companies record the loss in value of their fixed assets such as machines, equipment, or vehicles, degrade over time and reduce in value incrementally.')
income_statement_worksheet.write_url('A27', "https://www.thebalance.com/depreciation-and-amortization-on-the-income-statement-357570#:~:text=Depreciation%20expense%20is%20an%20income,their%20fixed%20assets%20through%20depreciation.&text=When%20depreciation%20expenses%20appear%20on,to%20the%20accumulated%20depreciation%20account.", string='Reconciled Depreciation')
income_statement_worksheet.write_comment('A29', 'revenue - expenses but excluded tax, interest on company debt, and amortization while removing non-recurring expenses or revenue')
income_statement_worksheet.write_url('A29', "https://www.divestopedia.com/definition/939/normalization", string='Normalized EBITDA')
income_statement_worksheet.write_comment('B1', 'Trailing Twelve Months')

df_balance_sheet = pd.DataFrame(balance_sheet)
balance_sheet_writer = pd.ExcelWriter('/Users/joshualee/Desktop/Stock_Financials/'+ticker+' balance_sheet.xlsx', engine='xlsxwriter')
df_balance_sheet.to_excel(balance_sheet_writer, index=False,sheet_name='Sheet1')

balance_sheet_worksheet = balance_sheet_writer.sheets['Sheet1']
balance_sheet_worksheet.write_comment('A2', 'resource with economic value that an individual, corporation, or country owns or controls with the expectation that it will provide a future benefit')
balance_sheet_worksheet.write_url('A2', "https://www.investopedia.com/terms/a/asset.asp", string='Total Assets')
balance_sheet_worksheet.write_comment('A3', 'If I owned 80 percent of a company that had $100,000 in assets and $60,000 in liabilities. Eight Perecent of liabilities is mine while twenty percent is minority interest')
balance_sheet_worksheet.write_url('A3', "https://smallbusiness.chron.com/minority-interest-asset-liability-65891.html", string='Total Liabilities Net Minority Interest')
balance_sheet_worksheet.write_comment('A4', 'If I owned 80 percent of a company that had $100,000 in assets and $60,000 in liabilities -- and therefore $40,000 in equity. Eighty percent($32,000) is mine while 20%($8000) belongs to other owners. This 20% is minority interest')
balance_sheet_worksheet.write_url('A4', "https://smallbusiness.chron.com/minority-interest-asset-liability-65891.html", string='Total Equity Gross Minority Interest')
balance_sheet_worksheet.write_comment('A5', 'cost is included in the value of an asset and expensed over the useful life of that asset, rather than being expensed in the period the cost was originally incurred')
balance_sheet_worksheet.write_url('A5', "refers to recording costs as assets", string='Total Capitalization')
balance_sheet_worksheet.write_comment('A6', 'measures the amount of money that would be distributable to common shareholders if a company were to liquidate its assets')
balance_sheet_worksheet.write_url('A6', "https://pocketsense.com/included-common-stockholders-equity-12086765.html", string='Common Stock Equity')
balance_sheet_worksheet.write_comment('A7', 'total assets of a company minus intangible assets such as goodwill, patents, and trademarks, less all liabilities and the par value of preferred stock. In other words, its focus is on physical assets such as property, plant, and equipment')
balance_sheet_worksheet.write_url('A7', "https://www.investopedia.com/terms/n/nettangibleassets.asp#:~:text=Net%20tangible%20assets%20are%20calculated,par%20value%20of%20preferred%20stock.", string='Net Tangible Assets')
balance_sheet_worksheet.write_comment('A8', 'current assets - liabilities. Positive value means company can fund its current operations and invest in future growth or business has too much inventory and not investing in future growth')
balance_sheet_worksheet.write_url('A8', "https://www.investopedia.com/terms/w/workingcapital.asp", string='Working Capital')
balance_sheet_worksheet.write_comment('A9', 'refers to the combined value of equity and debt capital raised by a firm, inclusive of capital leases')
balance_sheet_worksheet.write_url('A9', "https://www.investopedia.com/terms/i/invested-capital.asp#:~:text=Invested%20capital%20is%20the%20total,of%20equity%20issued%20to%20investors.", string='Invested Capital')
balance_sheet_worksheet.write_comment('A10', 'measures a firm’s net asset value excluding the intangible assets and goodwill. In other words, it’s how much all of the physical assets of a company are worth.')
balance_sheet_worksheet.write_url('A10', "https://www.myaccountingcourse.com/accounting-dictionary/tangible-book-value", string='Tangible Book Value')
balance_sheet_worksheet.write_comment('A11', 'sum of all short- and long-term debt')
balance_sheet_worksheet.write_url('A11', "https://smallbusiness.chron.com/determine-companys-total-debt-balance-sheet-42435.html#:~:text=Total%20debt%20is%20the%20sum%20of%20all%20short%2D%20and%20long,in%20less%20than%2012%20months.", string='Total Debt')
balance_sheet_worksheet.write_comment('A12', 'shows how much cash would remain if all debts were paid off using all their cash and liquid assets converted to cash')
balance_sheet_worksheet.write_url('A12', "https://www.investopedia.com/terms/n/netdebt.asp", string='Net Debt')
balance_sheet_worksheet.write_comment('A13', 'authorized shares sold to and held by the shareholders of a company')
balance_sheet_worksheet.write_url('A13', "https://www.investopedia.com/terms/i/issuedshares.asp", string='Share Issued')
balance_sheet_worksheet.write_comment('A14', 'represent the basic voting shares of a corporation. Holders of ordinary shares are typically entitled to one vote per share and only receive dividends at the discretion of the company’s management')
balance_sheet_worksheet.write_url('A14', "https://www.investopedia.com/terms/o/ordinaryshares.asp", string='Ordinary Shares Number')


df_cash_flow_statement = pd.DataFrame(cash_flow_statement)
cash_flow_statement_writer = pd.ExcelWriter('/Users/joshualee/Desktop/Stock_Financials/'+ticker+' cash_flow.xlsx', engine='xlsxwriter')
df_cash_flow_statement.to_excel(cash_flow_statement_writer, index=False,sheet_name='Sheet1')

cash_flow_statement_worksheet = cash_flow_statement_writer.sheets['Sheet1']
cash_flow_statement.write_comment('A2', 'amount of cash generated by a company's normal business operations')
cash_flow_statement.write_url('A2', "https://www.investopedia.com/terms/o/operatingcashflow.asp", string='Operating Cash Flow')
cash_flow_statement.write_comment('A3', 'how much cash has been generated or spent from various investment-related activities in a specific period. Investing activities include purchases of physical assets, investments in securities, or the sale of securities or assets.')
cash_flow_statement.write_url('A3', "https://www.investopedia.com/terms/c/cashflowfinvestingactivities.asp", string='Investing Cash Flow')
cash_flow_statement.write_comment('A4', 'cash flow used to pay back loans')
cash_flow_statement.write_url('A4', "https://www.investopedia.com/terms/c/cash-flow-financing.asp", string='Financing Cash Flow')
cash_flow_statement.write_comment('A5', 'portion of their investment portfolio assets that reside in cash or cash equivalents')
cash_flow_statement.write_url('A5', "https://www.investopedia.com/terms/c/cash_position.asp", string='End Cash Position')
cash_flow_statement.write_comment('A8', 'funds used by a company to acquire, upgrade, and maintain physical assets such as property, plants, buildings, technology, or equipment')
cash_flow_statement.write_url('A8', "https://www.investopedia.com/terms/c/capitalexpenditure.asp", string='Capital Expenditure')
cash_flow_statement.write_comment('A9', 'total amount of shares a company is authorized to issue')
cash_flow_statement.write_url('A9', "https://www.investopedia.com/ask/answers/050115/whats-difference-between-capital-stock-and-treasury-stock.asp", string='Issuance of Capital Stock')
cash_flow_statement.write_comment('A10', 'deferred costs, which are recorded as long-term assets on the balance sheet and amortized over the term of a debt instrument')
cash_flow_statement.write_url('A10', "https://smallbusiness.chron.com/debt-issuance-costs-cash-flow-statement-38540.html#:~:text=Debt%2Dissuance%20costs%20go%20on,on%20the%20operating%2Dactivities%20section.", string='Issuance of Debt')
cash_flow_statement.write_comment('A11', 'how much debt is repayed')
cash_flow_statement.write_url('A11', "https://www.investopedia.com/terms/r/repayment.asp#:~:text=Repayment%20is%20the%20act%20of,include%20an%20early%20repayment%20fee.", string='Repayment of Debt')
cash_flow_statement.write_comment('A12', 'company buys back its shares from the marketplace with its accumulated cash')
cash_flow_statement.write_url('A12', "https://www.investopedia.com/articles/02/041702.asp#:~:text=A%20stock%20buyback%2C%20also%20known,on%20the%20market%20is%20reduced.", string='Repurchase of Capital Stock')
cash_flow_statement.write_comment('A13', 'represents the cash available for the company to repay creditors or pay dividends and interest to investors')
cash_flow_statement.write_url('A13', "https://www.investopedia.com/terms/f/freecashflow.asp", string='Free Cash Flow')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
writer2.save()
writer3.save()