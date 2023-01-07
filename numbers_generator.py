#!/usr/bin/python3
import getopt
import json
import math
import os
import requests
import sys
import time

ids = { "MegaMillions": "5xaw-6ayf", "PowerBall" : "d6yy-54nr" }

def get_interquartile_range(lst):
    lstlen = len(lst)
    #print("lstlen:[" + str(lstlen) + "]")
    lst.sort()

    if lstlen % 2 != 0:
        lstfirstlast = int(math.floor(lstlen/2))
        #print("lstfirstlast:[" + str(lstfirstlast) + "]")
        lstsecondfirst = int(math.ceil(lstlen / 2)) + 1
        #print("lstsecondfirst:[" + str(lstsecondfirst) + "]")
    else:
        lstfirstlast = int(lstlen / 2)
        #print("lstfirstlast:[" + str(lstfirstlast) + "]")
        lstsecondfirst = int(lstlen / 2) + 1
        #print("lstsecondfirst:[" + str(lstsecondfirst) + "]")

    if lstfirstlast % 2 != 0:
        #print("lstfirstlast type:",type(lstfirstlast))
        #print("iqdelta type:",type(iqdelta))
        mininterquartilevalue = lst[int(math.ceil(lstfirstlast/2)) - 1 - int(iqdelta)]  # Commented to tweak interquartile
        #mininterquartilevalue = lst[int(math.ceil(lstfirstlast/2)) - 1]  # Commented to tweak interquartile
        #mininterquartilevalue = lst[int(math.ceil(lstfirstlast/2)) + 11] # Reduced range
        #mininterquartilevalue = lst[int(math.ceil(lstfirstlast/2)) - 13]   # Increased range
    else:
        #print("lstfirstlast type:",type(lstfirstlast))
        #print("iqdelta type:",type(iqdelta))
        mininterquartilevalue = (float(lst[int(lstfirstlast/2) - 1 - int(iqdelta)]) + float(lst[int(lstfirstlast/2) - int(iqdelta)])) / 2       # Commented to tweak interquartile
        #mininterquartilevalue = (float(lst[int(lstfirstlast/2) - 1]) + float(lst[int(lstfirstlast/2)])) / 2       # Commented to tweak interquartile
        #mininterquartilevalue = (float(lst[int(lstfirstlast/2)] + 11) + float(lst[int(lstfirstlast/2) + 12])) / 2 # Reduced range
        #mininterquartilevalue = (float(lst[int(lstfirstlast/2)] - 13) + float(lst[int(lstfirstlast/2) - 12])) / 2    # Increased range

    if (lstlen - lstsecondfirst + 1) % 2 != 0:
        #print("iqdelta type:",type(iqdelta))
        maxinterquartilevalue = lst[lstsecondfirst + int((lstlen - lstsecondfirst) / 2) - 1 - int(iqdelta)]  # Comment to tweak interquartile
        #maxinterquartilevalue = lst[lstsecondfirst + int((lstlen - lstsecondfirst) / 2) - 1]  # Comment to tweak interquartile
        #maxinterquartilevalue = lst[lstsecondfirst + int((lstlen - lstsecondfirst) / 2) - 14] # Reduced range
        #maxinterquartilevalue = lst[lstsecondfirst + int((lstlen - lstsecondfirst) / 2) + 11]       # Increase range
    else:
        #print("iqdelta type:",type(iqdelta))
        maxinterquartilevalue = (lst[lstsecondfirst + int(math.floor((lstlen - lstsecondfirst) / 2)) - 1 + int(iqdelta)] + lst[lstsecondfirst + int(math.ceil((lstlen - lstsecondfirst) / 2)) - 1 + int(iqdelta)]) / 2   # Commented to tweak interquartile
        #maxinterquartilevalue = (lst[lstsecondfirst + int(math.floor((lstlen - lstsecondfirst) / 2)) - 1] + lst[lstsecondfirst + int(math.ceil((lstlen - lstsecondfirst) / 2)) - 1]) / 2   # Commented to tweak interquartile
        #maxinterquartilevalue = (lst[lstsecondfirst + int(math.floor((lstlen - lstsecondfirst) / 2)) - 14] + lst[lstsecondfirst + int(math.ceil((lstlen - lstsecondfirst) / 2)) - 14]) / 2 # Reduced range
        #maxinterquartilevalue = (lst[lstsecondfirst + int(math.floor((lstlen - lstsecondfirst) / 2)) + 11] + lst[lstsecondfirst + int(math.ceil((lstlen - lstsecondfirst) / 2)) + 11]) / 2            # Increased range

    return mininterquartilevalue,maxinterquartilevalue

def calculate_winning_probability(lottery, win_num):
    sum = 0.0

    if lottery == "MegaMillions":
        probabilities = MegaMillions_probabilities
        spl_probabilities = MegaMillions_Mega_probabilities

    if lottery == "PowerBall":
        probabilities = PowerBall_probabilities
        spl_probabilities = PowerBall_Power_probabilities


    for i in range(5):
        sum += float(probabilities[win_num[i]-1])
    sum_with_spl = sum + float(spl_probabilities[win_num[5]-1])
    return sum,sum_with_spl

def past_winning_probabilities(lottery, past_winning_numbers):
    sums = [ int(0) for i in range(len(past_winning_numbers)) ]
    sums_with_spl = [ int(0) for i in range(len(past_winning_numbers)) ]
    sums_index = 0

    if lottery == "MegaMillions":
        probabilities = MegaMillions_probabilities
        spl_probabilities = MegaMillions_Mega_probabilities

    if lottery == "PowerBall":
        probabilities = PowerBall_probabilities
        spl_probabilities = PowerBall_Power_probabilities

    for win in past_winning_numbers:
        win_num = win.split()
        win_num = [int(x) for x in win_num]

        for i in range(5):
            sums[sums_index] += float(probabilities[win_num[i]-1])
        sums_with_spl[sums_index] = sums[sums_index] + float(spl_probabilities[win_num[5]-1])
        sums_index += 1

    return sums,sums_with_spl

def check_prime_divisions(win_num):
    for i in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        sum = 0
        for j in range(5):
            if win_num[j]%i == 0:
                sum += 1
            if sum >= 3:
               return False
    return True
            

def check_even_odd(win_num):
    oddcount = win_num[0]%2 + win_num[1]%2 + win_num[2]%2 + win_num[3]%2 + win_num[4]%2
    return oddcount == 2 or oddcount ==3

def check_no_same_reminders(win_num):
    return len(set([int(x%10) for x in win_num[0:4]])) >= 4

def check_2x10_series(win_num):
    return len(set([int(x/10) for x in win_num[0:4]])) >= 3

def check_2x2_series(win_num):
    return not (win_num[0]+1 == win_num[1] and win_num[2]+1 == win_num[3] or win_num[1]+1 == win_num[2] and win_num[3]+1 == win_num[4]) 

def check_3_series(win_num):
    return not (win_num[0]+1 == win_num[1] and win_num[1]+1 == win_num[2] or win_num[1]+1 == win_num[2] and win_num[2]+1 == win_num[3] or win_num[3]+1 == win_num[4] and win_num[4]+1 == win_num[5]) 

def check_no_repeat(win_num):
    return len(win_num[0:4]) == len(set(win_num[0:4]))

def find_sums(lottery, past_winning_numbers):
    sums = [ int(0) for i in range(len(past_winning_numbers)) ]
    sums_with_spl = [ int(0) for i in range(len(past_winning_numbers)) ]
    sums_index = 0

    for win in past_winning_numbers:
        win_num = win.split()
        win_num = [int(x) for x in win_num]

        for i in range(5):
            sums[sums_index] += win_num[i]
        sums_with_spl[sums_index] = sums[sums_index] + win_num[5]
        sums_index += 1

    return sums,sums_with_spl

    
def check_sum(lottery,win_num):
    sum = win_num[0] + win_num[1] + win_num[2] + win_num[3] + win_num[4] 
    sum_with_spl = sum + win_num[5]

    if lottery == "MegaMillions":
        min_sum = min_MegaMillions_sums_interquartile
        max_sum = max_MegaMillions_sums_interquartile
        min_sum_with_spl = min_MegaMillions_sums_with_spl_interquartile
        max_sum_with_spl = max_MegaMillions_sums_with_spl_interquartile

    if lottery == "PowerBall":
        min_sum = min_PowerBall_sums_interquartile
        max_sum = max_MegaMillions_sums_interquartile
        min_sum_with_spl = min_PowerBall_sums_with_spl_interquartile
        max_sum_with_spl = max_PowerBall_sums_with_spl_interquartile

    #print(sum, min_sum, max_sum, sum_with_spl, min_sum_with_spl, max_sum_with_spl)
    #print(sum > min_sum and sum < max_sum)

    return sum > min_sum and sum < max_sum and sum_with_spl > min_sum_with_spl and sum_with_spl < max_sum_with_spl

def check_not_won(lottery,win_num_str):
    #print("check_not_won: " + win_num_str)
    if lottery == "MegaMillions":
        past_winning_numbers = MegaMillions_past_winning_numbers

    if lottery == "PowerBall":
        past_winning_numbers = PowerBall_past_winning_numbers

    return not win_num_str in past_winning_numbers

def check_rules(lottery,win_num):
    win_num_str = f'{win_num[0]:02d} {win_num[1]:02d} {win_num[2]:02d} {win_num[3]:02d} {win_num[4]:02d} {win_num[5]:02d}'

    #print("check_rules:" + win_num_str)
    #print(check_not_won(win_num_str))

    if check_not_won(lottery, win_num_str):
        #print("lottery not won: ",win_num_str)
        if check_sum(lottery,win_num):
            #print("sums in range: ",win_num_str)
            if check_no_repeat(win_num):
                #print("no repeat: ",win_num_str)
                if check_3_series(win_num):
                    #print("no 3 series: ",win_num_str)
                    if check_2x2_series(win_num):
                        #print("no 2x2 series: ",win_num_str)
                        if check_2x10_series(win_num):
                            #print("no 2x10 series: ",win_num_str)
                            if check_no_same_reminders(win_num):
                                #print("no same reminders: ",win_num_str)
                                if check_even_odd(win_num):
                                    #print("no many even odds: ",win_num_str)
                                    if check_prime_divisions(win_num):
                                        #print("no prime divisions: ",win_num_str)
                                        probability,spl_probability = calculate_winning_probability(lottery, win_num)
        
                                        if lottery == "MegaMillions":
                                            min_probability = min_MegaMillions_probability_interquartile
                                            max_probability = max_MegaMillions_probability_interquartile
                                            min_spl_probability = min_MegaMillions_spl_probability_interquartile
                                            max_spl_probability = max_MegaMillions_spl_probability_interquartile

                                        if lottery == "PowerBall":
                                            min_probability = min_PowerBall_probability_interquartile
                                            max_probability = max_PowerBall_probability_interquartile
                                            min_spl_probability = min_PowerBall_spl_probability_interquartile
                                            max_spl_probability = max_PowerBall_spl_probability_interquartile


                                        if probability > min_probability and probability < max_probability and spl_probability > min_spl_probability and spl_probability < max_spl_probability:
                                        #if spl_probability > min_spl_probability and spl_probability < max_spl_probability:
                                        #if probability > min_probability and probability < max_probability:
                                            print(win_num_str)
                                        else:
                                            print("failed: probabilities ",win_num_str,probability,min_probability,max_probability,spl_probability,min_spl_probability,max_spl_probability)
                                            #print("failed: probabilities ",spl_probability,min_spl_probability,max_spl_probability)
                                            #print("failed: probabilities ",win_num_str,probability,min_probability,max_probability)
                                    else:
                                        print("failed: prime divisions ",win_num_str)
                                else:
                                    print("failed: many even odds ",win_num_str)
                            else:
                                print("failed: same reminders ",win_num_str)
                        else:
                            print("failed: 2x10 series ",win_num_str)
                    else:
                        print("failed: 2x2 series ",win_num_str)
                else:
                    print("failed: 3 series ",win_num_str)
            else:
                print("failed: repeat ",win_num_str)
        else:
            print("failed: sums ",win_num_str)
    else:
        print("failed: won ",win_num_str)
#        else:
#            print("probability not in range: ",win_num_str)
#    else:
#        print("check rules failed: ",win_num_str)


def find_probabilities(lottery, past_winning_numbers):
    totaloccurrences = 0
    totalsploccurrences = 0

    if lottery == "MegaMillions":
        max_num = 70
        max_special = 25

    if lottery == "PowerBall":
        max_num = 69
        max_special = 26

    occurrence = [ int(0) for i in range(max_num) ]
    spl_occurrence = [ int(0) for i in range(max_special) ]
    probabilities = [ int(0) for i in range(max_num) ]
    spl_probabilities = [ int(0) for i in range(max_special) ]
    #print(occurrence)
    
    for win in past_winning_numbers:
        win_num = win.split()
        win_num = [int(x) for x in win_num]
        #print(win_num)

        for i in range(5):
            occurrence[win_num[i]-1] += 1
            totaloccurrences += 1
        #print(occurrence)
        spl_occurrence[win_num[5]-1] += 1
        totalsploccurrences += 1
    
    for i in range(max_num):
        probabilities[i] = occurrence[i]*1000/totaloccurrences

    for i in range(max_special):
        spl_probabilities[i] = spl_occurrence[i]*1000/totalsploccurrences

    return probabilities,spl_probabilities


def get_winning_numbers(lottery):
    winning_json_filename = "./" + lottery+ "/" + time.strftime("%Y%m%d") +".json"

    if not (os.path.exists(winning_json_filename) and os.path.getsize(winning_json_filename) > 0):
        URL = "https://data.ny.gov/api/views/LOTTERYID/rows.json?accessType=DOWNLOAD"
        URL = URL.replace("LOTTERYID",ids[lottery])
        try:
            winning_json = requests.get(URL)
        except:
            sys.exit("URL Download failure " + URL)
            
        winning_json_file = open(winning_json_filename, "wb")
        winning_json_file.write(winning_json.content)
        winning_json_file.close()

    winning_json_file = open(winning_json_filename, "r")
    winning_json_data = json.load(winning_json_file)['data']

    winning_json_data.sort(key=lambda x: x[8])
    if lottery == "MegaMillions":
        winning_json_data = filter(lambda x: x[8] > '2017-10-28T', winning_json_data)
    if lottery == "PowerBall":
        winning_json_data = filter(lambda x: x[8] > '2015-10-04T', winning_json_data)
    winning_json_file.close()

    #print(winning_json_data)
    if lottery == "MegaMillions":
        return [data[9] + " " + "{0:02d}".format(int(data[10])) for data in winning_json_data]
    if lottery == "PowerBall":
            return [data[9] for data in winning_json_data]

def generate_winning_numbers(lottery):
    if lottery == "MegaMillions":
        max_num = 71
        max_special = 26

    if lottery == "PowerBall":
        max_num = 70
        max_special = 27

    #print("In generating numbers")
    #for i in range(1, max_num):
    for i in range(3, 4):
#        print("i[" + str(i) + "]")
        for j in range(i+1, max_num):
        #for j in range(20, 21):
#            print("j[" + str(j) + "]")
            if j < 10:
                continue
            for k in range(j+1, max_num):
            #for k in range(46, 47):
#                print("k[" + str(k) + "]")
                if k < 20:
                    continue
                for l in range(k+1, max_num):
                #for l in range(50, 60):
#                    print("l[" + str(l) + "]")
                    if l < 35:
                        continue
                    for m in range(l+1, max_num):
                    #for m in range(60, 64):
#                        print("m[" + str(m) + "]")
                        if m < 50:
                            continue
                        for n in range(1, max_special):
                        #for n in range(1, max_special):
                            win_num=[i,j,k,l,m,n]
                            check_rules(lottery,win_num)
                            #print(f'{i:02d} {j:02d} {k:02d} {l:02d} {m:02d} {n:02d}') 

def sub_main():
    global MegaMillions_past_winning_numbers
    global PowerBall_past_winning_numbers

    global MegaMillions_probabilities
    global MegaMillions_Mega_probabilities
    global PowerBall_probabilities
    global PowerBall_Power_probabilities

    global MegaMillions_sums
    global MegaMillions_sums_with_spl
    global PowerBall_sums
    global MegaMillions_sums_with_spl

    global min_MegaMillions_sums_interquartile
    global min_MegaMillions_sums_with_spl_interquartile
    global min_PowerBall_sums_interquartile
    global min_PowerBall_sums_with_spl_interquartile

    global max_MegaMillions_sums_interquartile
    global max_MegaMillions_sums_with_spl_interquartile
    global max_PowerBall_sums_interquartile
    global max_PowerBall_sums_with_spl_interquartile

    global min_MegaMillions_probability_interquartile
    global min_MegaMillions_spl_probability_interquartile
    global min_PowerBall_probability_interquartile
    global min_PowerBall_spl_probability_interquartile

    global max_MegaMillions_probability_interquartile
    global max_MegaMillions_spl_probability_interquartile
    global max_PowerBall_probability_interquartile
    global max_PowerBall_spl_probability_interquartile

    MegaMillions_past_winning_numbers = get_winning_numbers("MegaMillions")
    #print("Printing MegaMillions Winning Numbers==================================")
    #for numbers in MegaMillions_past_winning_numbers:
    #    print(numbers)
    
    PowerBall_past_winning_numbers = get_winning_numbers("PowerBall")
    #print("Printing PowerBall Winning Numbers==================================")
    #for numbers in PowerBall_past_winning_numbers:
    #    print(numbers)
    
    MegaMillions_probabilities,MegaMillions_Mega_probabilities = find_probabilities("MegaMillions",MegaMillions_past_winning_numbers)
    #print("Printing MegaMillions Probabilities==================================")
    #print(MegaMillions_probabilities)
    #print("Printing MegaMillions Mega Probabilities==================================")
    #print(MegaMillions_Mega_probabilities)
    
    PowerBall_probabilities,PowerBall_Power_probabilities = find_probabilities("PowerBall",PowerBall_past_winning_numbers)
    #print("Printing PowerBall Probabilities==================================")
    #print(PowerBall_probabilities)
    #print("Printing PowerBall Power Probabilities==================================")
    #print(PowerBall_Power_probabilities)
    
    MegaMillions_sums,MegaMillions_sums_with_spl = find_sums("MegaMillions", MegaMillions_past_winning_numbers)
    PowerBall_sums,PowerBall_sums_with_spl = find_sums("PowerBall", PowerBall_past_winning_numbers)
    
    #print("Printing Past Winning MegaMillions Probabilities==================================")
    sums_probability_MegaMillions,sums_with_spl_probability_MegaMillions=past_winning_probabilities("MegaMillions", MegaMillions_past_winning_numbers)
    #print("Printing Past Winning PowerBall Probabilities==================================")
    sums_probability_PowerBall,sums_with_spl_probability_PowerBall=past_winning_probabilities("PowerBall", PowerBall_past_winning_numbers)
    
    #print("Printing interquartile range of MegaMillions Past Winning Probabilities")
    min_MegaMillions_probability_interquartile,max_MegaMillions_probability_interquartile=get_interquartile_range(sums_probability_MegaMillions)
    min_MegaMillions_spl_probability_interquartile,max_MegaMillions_spl_probability_interquartile=get_interquartile_range(sums_with_spl_probability_MegaMillions)
    #print(min_MegaMillions_probability_interquartile, max_MegaMillions_probability_interquartile)
    
    #print("Printing interquartile range of PowerBall Past Winning Probabilities")
    min_PowerBall_probability_interquartile,max_PowerBall_probability_interquartile=get_interquartile_range(sums_probability_PowerBall)
    min_PowerBall_spl_probability_interquartile,max_PowerBall_spl_probability_interquartile=get_interquartile_range(sums_with_spl_probability_PowerBall)
    #print(min_PowerBall_probability_interquartile, max_PowerBall_probability_interquartile)
    
    min_MegaMillions_sums_interquartile,max_MegaMillions_sums_interquartile=get_interquartile_range(MegaMillions_sums)
    min_MegaMillions_sums_with_spl_interquartile,max_MegaMillions_sums_with_spl_interquartile=get_interquartile_range(MegaMillions_sums_with_spl)
    min_PowerBall_sums_interquartile,max_PowerBall_sums_interquartile=get_interquartile_range(PowerBall_sums)
    min_PowerBall_sums_with_spl_interquartile,max_PowerBall_sums_with_spl_interquartile=get_interquartile_range(PowerBall_sums_with_spl)
    #print(min_MegaMillions_sums_interquartile,max_MegaMillions_sums_interquartile,min_MegaMillions_sums_with_spl_interquartile,max_MegaMillions_sums_with_spl_interquartile,min_PowerBall_sums_interquartile,max_PowerBall_sums_interquartile,min_PowerBall_sums_with_spl_interquartile,max_PowerBall_sums_with_spl_interquartile)
    
    #generate_winning_numbers("MegaMillions")
    generate_winning_numbers("PowerBall")

def main(argv):
    global testpercent
    global testcount
    global iqdelta

    testpercent = 0
    testcount   = 0
    iqdelta     = 0

    try:
        opts, args = getopt.getopt(argv,"hp:c:d:")
    except getopt.GetOptError:
        print('number_generator.py -p testpercent -c testcount -d iqdelta')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('number_generator.py -p testpercent -c testcount -d iqdelta')
            sys.exit()
        elif opt == '-p':
            testpercent = arg
        elif opt == '-c':
            testcount = arg
        elif opt == '-d':
            iqdelta = arg

    #print(testpercent, testcount, iqdelta)
    sub_main()

if __name__ == "__main__":
    main(sys.argv[1:])

###### InterQuartile Test ####### 
#randomlist = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
#print(get_interquartile_range(randomlist))

#randomlist = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ]
#print(get_interquartile_range(randomlist))

#randomlist = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ]
#print(get_interquartile_range(randomlist))

#randomlist = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ]
#print(get_interquartile_range(randomlist))

#randomlist = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 ]
#print(get_interquartile_range(randomlist))

#randomlist = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ]
#print(get_interquartile_range(randomlist))
