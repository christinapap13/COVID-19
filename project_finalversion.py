import pandas as pd                             # import pandas library and define pd as its shortcut
from tabulate import tabulate                   # import tabulate library to improve the appearance of tabular data
import matplotlib.pyplot as plt                 # import matplotlib.pyplot library to plot and define plt as its shortcut
from matplotlib.ticker import FuncFormatter     # import matplotlib.ticker library to the appearance of axes labels (e.g. logarithmic scale e.t.c)
from calendar import monthrange                 # import monthrage function from calendar library to define the dates in a certain period
from datetime import datetime                   # import datetime function to get the current date
import numpy as np                              # import numpy library and define np as its shortcut
import sys                                      # import sys library (for command line arguments' handling)

#general prefix of all related files (url prefix) defines a collection of files
#one per day since 22/01/2020
file_prefix='https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/'

TotalFiles = 0 # number of total files read

#----------------------------------------------------------------------
# Attempt to open the filename  with a  name given by its arguments
# Returns a positive number on success or -1 in failure
# using an apropriate exception handling 
def load_csv_file(fname):
    file_name = file_prefix+fname 
    str1=" "
    global ColNames
    global TotalFiles
    global TotalKbytes
    try:
        print("Reading file " + fname,end = ' ')
        total_confirmed = pd.read_csv(file_name)[['Confirmed']].sum().iloc[0]
        print("...ok")
        TotalFiles += 1
        return total_confirmed
    except IOError as e:
        print(e)
        return(-1)

#----------------------------------------------------------------------
# Returns a filename (string) constructed from the given arguments
# dd: day e.g 23
# mm: month e.g 7
# yyyy: year e.g. 2021
# On the above example returns "07-23-2021.csv"
def get_filename(dd, mm, yyyy):
    dec2 = "{:02d}"
    return dec2.format(mm) + "-" + dec2.format(dd) + "-" + str(yyyy) + ".csv"

#----------------------------------------------------------------------
# Iterate all available files described by the dates from the starting date of logging (22nd January, 2020)
# up to the current date
# (Used in question 14 of the project)
def iterate_all_files():
    start_year = 2020
    start_month = 1
    start_day = 22

    start_from = f"{start_year}-{start_month}-{start_day}"

    dates_files = pd.date_range(start=start_from, end = datetime.today()).to_frame(index=False)
    cases=[]
    dates=[]
    for index, row in dates_files.iterrows():
        fname = row[0].strftime("%m-%d-%Y") + ".csv"
        confirmed = load_csv_file(fname)
        print("Q14, Reading file: " + fname, file=sys.stderr)
        if (confirmed>0):
            cases.append(confirmed)
            dates.append(row[0].strftime("%m-%d-%Y"))
    print("TotalFiles read : ", TotalFiles)
    return(pd.DataFrame(cases,index=dates, columns=['Confirmed']))
#----------------------------------------------------------------------
# Returns the date before the current date that is constructed as dd/mm/yyyy
def OneDayBack():
    global dd, mm, yyyy #global variables holding the current day, current month and the current year
    dd -= 1
    if (dd==0):
        mm-=1
        if (mm==0):
            yyyy-=1
            mm=12
            dd=monthrange(yyyy,mm)
#----------------------------------------------------------------------
# Returns a list with the names of the last -n- available files
# Most recents files appear at the front
# Hence last_files[0] contains the name ofe the most recent available file e.t.c
def find_last_update(n):
    last_files = []
    global yyyy 
    yyyy = datetime.now().year
    global mm 
    mm = datetime.now().month
    global dd
    dd = datetime.now().day
    k=0
    while (k<n):
        while (1):
            try:
                fname = get_filename(dd, mm, yyyy)
                pd_file = pd.read_csv(file_prefix + fname)
                last_files.append(file_prefix + fname)
                break;
            except IOError as e:
                OneDayBack()
        OneDayBack()
        k+=1
    return(last_files)
#----------------------------------------------------------------------
# tabular printing of the df dataframe
def tab_print(df):
    print(tabulate(df, headers="keys", tablefmt="github", floatfmt="10.0f"))

#----------------------------------------------------------------------
# Load a csv file on a dataframe. 
# Returns the filled dataframe
def get_dataframe(fname):
    return(pd.read_csv(fname))
#----------------------------------------------------------------------  
# Returns its x argument in logarithm scale
def millions(x, pos):
	'The two args are the value and tick position'
	return '%1.1fM' % (x*1e-6)
#
#---------------------------------------------------------------------- 
# Subroutine q1: Answer in question #1 of the project
def q1(file_name): 
    df=get_dataframe(file_name)     # loads the most recent file in a dataframe named df
    print(tabulate(df.iloc[:5,]))   # prints the first 5 lines of the df
    print(df[["Deaths","Recovered","Confirmed","Active"]].sum()) # prints the columns "Deaths","Recovered","Confirmed","Active", sum their contents
    print(df[df.isna().any(axis=1)]) #print the null values of the dataframe
#----------------------------------------------------------------------	
# Subroutine q2: Answer in question #2 of the project
def q2(file_name, file_name_prev):
    df=get_dataframe(file_name)[["Confirmed","Deaths","Recovered","Active"]].sum().tolist();
    dfprev=get_dataframe(file_name_prev)[["Confirmed","Deaths","Recovered","Active"]].sum().tolist();
    print("Most recent confirmed cases = " + str(int(df[0] - dfprev[0])))
    print("Most recent deaths = " + str(int(df[1] - dfprev[1])));
    print("Most recent recovered cases = " + str(int(df[2] - dfprev[2])));
    print("Most recent actice cases = " + str(int(df[3] - dfprev[3])));
#----------------------------------------------------------------------	
# Subroutine q3: Answer in question #3 of the project
def q3(file_name, file_name_prev):
    df1=get_dataframe(file_name)[["Province_State","Country_Region","Deaths","Recovered"]]
    df2=df1.groupby(['Country_Region','Province_State']).sum()
    df1prev=get_dataframe(file_name_prev)[["Province_State","Country_Region","Deaths","Recovered"]]
    df2prev=df1prev.groupby(['Country_Region','Province_State']).sum()

    df=pd.merge(df2,df2prev,on=['Country_Region','Province_State'],how='left')
    df['Recent_Deaths']=df['Deaths_x']-df['Deaths_y']
    df['Recent_Recovered']=df['Recovered_x']-df['Recovered_y']
    tab_print(df[['Recent_Deaths', 'Recent_Recovered']])
#----------------------------------------------------------------------	
# Subroutine q4: Answer in question #4 of the project
def q4(file_name):
    df=get_dataframe(file_name)[["Province_State","Country_Region","Confirmed","Deaths","Recovered"]]
    Chinadf = df.loc[(df.Country_Region == "China")]
    tab_print(Chinadf)
#----------------------------------------------------------------------
# Subroutine q5: Answer in question #5 of the project
def q5(file_name,file_name_prev):
    df=get_dataframe(file_name)[["Admin2","Province_State","Country_Region","Deaths"]]
    dfprev=get_dataframe(file_name_prev)[["Admin2","Province_State","Country_Region","Deaths"]]

    d=df["Deaths"].sum()
    d1=dfprev["Deaths"].sum()
    df=pd.merge(df,dfprev,on=['Country_Region','Province_State','Admin2'],how='left')
    df['Recent_Deaths']=df['Deaths_x']-df['Deaths_y']
    tab_print(df[["Admin2","Province_State","Country_Region","Recent_Deaths"]])
    print(d-d1)

#----------------------------------------------------------------------
# Subroutine q6: Answer in question #6 of the project
def q6(file_name):
    df=get_dataframe(file_name)[["Admin2","Province_State","Country_Region","Confirmed"]].groupby(['Country_Region']).sum()
    df.rename(index={'US':'United States'},inplace=True)
    dfallcountries=pd.read_csv('https://raw.githubusercontent.com/datasets/country-list/master/data.csv')
    df2 = pd.merge(dfallcountries, df, left_on = 'Name', right_index=True, how = 'left')
    df3 = df2[df2['Confirmed'].isna()][['Name']]
    df3.index = range(1, len(df3.index)+1)
    tab_print(df3)
#----------------------------------------------------------------------  
# Subroutine q7: Answer in question #7 of the project
def q7(file_name):
    df=get_dataframe(file_name)[["Admin2","Province_State","Country_Region","Deaths"]].groupby(['Country_Region']).sum()
    df1 = df.loc[(df.Deaths != 0)]
    tab_print(df1)
#----------------------------------------------------------------------  
# Subroutine q8: Answer in question #8 of the project
def q8(file_name):
    df=get_dataframe(file_name)[["Admin2","Province_State","Country_Region","Recovered"]].groupby(['Country_Region']).sum()
    df1 = df.loc[(df.Recovered != 0)]
    tab_print(df1)
#----------------------------------------------------------------------
# Subroutine q9: Answer in question #9 of the project
def q9(file_name):
    df=get_dataframe(file_name)[["Admin2","Province_State","Country_Region","Recovered","Confirmed","Deaths"]].groupby(['Country_Region']).sum()
    df.sort_values(by='Confirmed', ascending=False, inplace=True)
    tab_print(df.iloc[:10,])

#---------------------------------------------------------------------- 
# Subroutine q10: Answer in question #10 of the project 
def q10(file_name,n):
    df1=get_dataframe(file_name)[["Admin2","Province_State","Country_Region","Confirmed", "Recovered", "Deaths", "Active"]].groupby(['Country_Region']).sum()
    df0 = df1.loc[(df1.Deaths>150)]
                                                                        
    df = df0.head(n)                        #top n rows
    plot_title = 'Top '+ str(n) + ' Cases)' #the title of the plot
    x = np.arange(n)                        # the label locations in x-axis
    fig, ax = plt.subplots()                # Create a figure and a set of subplots
    
    df.plot.line(y='Confirmed', color='red', label='Cd',ax=ax) #draw a bar for Confirmed cases
    df.plot.line(y='Recovered', color='green', label='Rd', ax=ax)     #draw a bar for Recovered cases
    df.plot.line(y='Deaths', color='blue', label='Dts',ax=ax)  #draw a bar for Deaths cases
    df.plot.line(y='Active', color='cyan', label='Act',ax=ax)  #draw a bar for Deaths cases

# Formatting plot
    ax.set_xticks(x)                                #set the ticks in x-axis arithmeticaly
    ax.set_xticklabels(df.index)                    #set the labels of ticks in x-axis
    ax.legend()                                     #Place a legend on the axes
    formatter = FuncFormatter(millions)             #formating number in millions
    ax.yaxis.set_major_formatter(formatter)         #format labels in y-axis in millions

    plt.xlabel('X Label')                           #set the label of x-axis
    plt.ylabel('Y Label')                           #set the label of y-axis
    plt.title(plot_title)                           #set the label of the plot
    plt.xticks(rotation=90)                         #rotate labels of xticks
    fig.tight_layout()                              #Adjust the padding between and around subplots.
    plt.show()
    plt.savefig('q10.png')
#---------------------------------------------------------------------- 
# Subroutine q11: Answer in question #11 of the project  
def q11(file_name, n):
    df=get_dataframe(file_name)[["Province_State","Country_Region","Deaths"]]
    USdf = df.loc[(df.Country_Region == "US")].groupby(['Province_State']).sum()
    df = USdf.sort_values(by=["Deaths"], ascending=False).head(n)   #sort read dataframe in descending order by 
                                                                    #'sorted_by_col' and take the top n rows
    plot_title = 'Top '+ str(n) + ' States (Deaths) in US'          #the title of the plot

    x = np.arange(n)                        # the label locations in x-axis
    width = 0.30                            # the width of the bars
    fig, ax = plt.subplots()                # Create a figure and a set of subplots
    
    ax.bar(x + width, df.Deaths, width, color='blue', label='Deaths')  #draw a bar for Deaths cases

# Formatting plot
    ax.set_xticks(x)                                #set the ticks in x-axis arithmeticaly
    ax.set_xticklabels(df.index)                      #set the labels of ticks in x-axis
    ax.legend()                                     #Place a legend on the axes
    #formatter = FuncFormatter(millions)             #formating number in millions
    #ax.yaxis.set_major_formatter(formatter)         #format labels in y-axis in millions

    plt.xlabel('States')                           #set the label of x-axis
    plt.ylabel('Cases in millions')                           #set the label of y-axis
    plt.title(plot_title)                           #set the label of the plot
    plt.xticks(rotation=90)                         #rotate labels of xticks
    fig.tight_layout()                              #Adjust the padding between and around subplots.
    plt.show()
    plt.savefig('q11.png')
#----------------------------------------------------------------------
# Subroutine q12: Answer in question #12 of the project 
def q12(file_name,n):
    q12Country(file_name,n, "US")
    q12Country(file_name,n, "China")
    q12Country(file_name,n, "India")

def q12Country(file_name, n, country_name):
    df0=get_dataframe(file_name)[["Province_State","Country_Region","Active"]]
    df1 = df0.loc[(df0.Country_Region == country_name)].groupby(['Province_State']).sum()

    df = df1.sort_values(by=["Active"], ascending=False).head(n)   #sort read dataframe in descending order by 
                                                                        #'sorted_by_col' and take the top n rows
    plot_title = 'Top '+ str(n) + ' States (Active) ' + 'for ' + country_name        #the title of the plot

    x = np.arange(n)                        # the label locations in x-axis
    width = 0.30                            # the width of the bars
    fig, ax = plt.subplots()                # Create a figure and a set of subplots
    
    ax.bar(x  , df.Active, width, color='green', label='Active')     #draw a bar for Recovered cases

# Formatting plot
    ax.set_xticks(x)                                #set the ticks in x-axis arithmeticaly
    ax.set_xticklabels(df.index)                      #set the labels of ticks in x-axis
    ax.legend()                                     #Place a legend on the axes
    formatter = FuncFormatter(millions)             #formating number in millions
    ax.yaxis.set_major_formatter(formatter)         #format labels in y-axis in millions

    plt.xlabel('States')                           #set the label of x-axis
    plt.ylabel('Cases in millions')                 #set the label of y-axis
    plt.title(plot_title)                           #set the label of the plot
    plt.xticks(rotation=90)                         #rotate labels of xticks
    fig.tight_layout()                              #Adjust the padding between and around subplots.
    plt.show()    
    plt.savefig('q12_' + country_name + '.png')

#----------------------------------------------------------------------  
# Subroutine q13: Answer in question #13 of the project 
def q13(file_name, n, sorted_by_col):
    df0=get_dataframe(file_name)[["Admin2","Province_State","Country_Region","Deaths","Recovered","Confirmed","Active"]]
    df1 = df0.loc[(df0.Country_Region == "US")].groupby(['Province_State']).sum()

    df = df1.sort_values(by=[sorted_by_col], ascending=False).head(n)   #sort read dataframe in descending order by 
                                                                        #'sorted_by_col' and take the top n rows
    plot_title = 'Top '+ str(n) + ' States ('+sorted_by_col+')'          #the title of the plot

    df['aux'] = df.index                    #create a new column in dataframe for its index
    x = np.arange(n)                        # the label locations in x-axis
    width = 0.30                            # the width of the bars
    fig, ax = plt.subplots()                # Create a figure and a set of subplots
    
    ax.bar(x - width, df.Confirmed, width, color='red', label='Confirmed') #draw a bar for Confirmed cases
    ax.bar(x  , df.Active, width, color='green', label='Active')     #draw a bar for Recovered cases
    ax.bar(x + width, df.Deaths, width, color='blue', label='Deaths')  #draw a bar for Deaths cases

# Formatting plot
    ax.set_xticks(x)                                #set the ticks in x-axis arithmeticaly
    ax.set_xticklabels(df.aux)                      #set the labels of ticks in x-axis
    ax.legend()                                     #Place a legend on the axes
    formatter = FuncFormatter(millions)             #formating number in millions
    ax.yaxis.set_major_formatter(formatter)         #format labels in y-axis in millions

    plt.xlabel('States')                           #set the label of x-axis
    plt.ylabel('Cases in millions')                           #set the label of y-axis
    plt.title(plot_title)                           #set the label of the plot
    plt.xticks(rotation=90)                         #rotate labels of xticks
    fig.tight_layout()                              #Adjust the padding between and around subplots.
    plt.show()  
    plt.savefig('q13.png')  
#----------------------------------------------------------------------
# Subroutine q14: Answer in question #14 of the project 
def q14(file_name):
    df=iterate_all_files()
    plot_title = 'Confirmed cases worldwide'        #the title of the plot
    x = np.arange(len(df.index))                    # the label locations in x-axis
    fig, ax = plt.subplots()                        # Create a figure and a set of subplots
    
    df.plot.line(y='Confirmed', color='red', label='Confirmed',ax=ax) #draw a bar for Confirmed cases

# Formatting plot
    ax.set_xticks(x)                                #set the ticks in x-axis arithmeticaly
    #ax.set_xticklabels(df.index)                    #set the labels of ticks in x-axis
    ax.legend()                                     #Place a legend on the axes
    formatter = FuncFormatter(millions)             #formating number in millions
    ax.yaxis.set_major_formatter(formatter)         #format labels in y-axis in millions

    plt.xlabel('Time')                              #set the label of x-axis
    plt.ylabel('Confirmed Cases Worldwide')         #set the label of y-axis
    plt.title(plot_title)                           #set the label of the plot
    plt.xticks(rotation=90)                         #rotate labels of xticks
    fig.tight_layout()                              #Adjust the padding between and around subplots.
    plt.show()
    plt.savefig('q14.png')

#----------------------------------------------------------------------
# Analyze command line arguments of the program itself (given by the user)
# and returns a sorted list of the desired questions to be answered.
def DisplayQuestions(n, sys_argv):
    args = str(sys_argv[1::])
    display_questions = {}
    if (len(sys_argv)>1):
        for arg in sys_argv[1::]:
            ar = arg.split(',')
            for a in ar:
                if (a.isnumeric()):
                    k = int(a)
                    if (k in range(1, n+1)):
                        display_questions[k] = 0
                    else:
                        print('Rejecting : ' + a)
            #args = args.replace(str(k),'$')
            #print(str(k) + ':' + args)
    else:
        for k in range(n, 0, -1):
            display_questions[k] = 0
    return sorted (display_questions.keys())
#----------------------------------------------------------------------
if __name__ == "__main__":
    displayed_questions = DisplayQuestions(14,sys.argv)
    filenames = find_last_update(2)
    file_name = filenames[0]
    file_name_prev = filenames[1]
    print("Last update = " + file_name)
    print("\t(" + file_name_prev + ')')

    if (1 in displayed_questions): # test if question 1 should be asnwered e.t.c
        print("Q1...", file=sys.stderr)
        print("Q1...")
        q1(file_name)
    if (2 in displayed_questions):
        print("Q2...", file=sys.stderr)
        print("Q2...")
        q2(file_name, file_name_prev)
    if (3 in displayed_questions):
        print("Q3...", file=sys.stderr)
        print("Q3...")
        q3(file_name, file_name_prev)
    if (4 in displayed_questions):
        print("Q4...", file=sys.stderr)
        print("Q4...")
        q4(file_name)
    if (5 in displayed_questions):
        print("Q5...", file=sys.stderr)
        print("Q5...")
        q5(file_name,file_name_prev)
    if (6 in displayed_questions):
        print("Q6...", file=sys.stderr)
        print("Q6...")
        q6(file_name)
    if (7 in displayed_questions):
        print("Q7...", file=sys.stderr)
        print("Q7...")
        q7(file_name)
    if (8 in displayed_questions):
        print("Q8...", file=sys.stderr)
        print("Q8...")
        q8(file_name)
    if (9 in displayed_questions):
        print("Q9...", file=sys.stderr)
        print("Q9...")
        q9(file_name)
    if (10 in displayed_questions):
        print("Q10...", file=sys.stderr)
        print("Q10...")
        q10(file_name,30)
    if (11 in displayed_questions):
        print("Q11...", file=sys.stderr)
        print("Q11...")
        q11(file_name,20)
    if (12 in displayed_questions):
        print("Q12...", file=sys.stderr)
        print("Q12...")
        q12(file_name,20)
    if (13 in displayed_questions):
        print("Q13...", file=sys.stderr)
        print("Q13...")
        q13(file_name,15, "Confirmed")
    if (14 in displayed_questions):
        print("Q14...", file=sys.stderr)
        print("Q14...")
        q14(file_name)
