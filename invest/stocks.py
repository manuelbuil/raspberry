import argparse
import datetime as dt
import logging
import pdb
import sqlite3
import sys
import time

from pandas_datareader import data, wb

IBEX = ['ABE.MC','ACS.MC','ACX.MC','AENA.MC','AMS.MC','ANA.MC','BBVA.MC',
'BKIA.MC','BKT.MC','CABK.MC','CLNX.MC','COL.MC','DIA.MC','ELE.MC','ENG.MC',
'FER.MC','GAS.MC','GRF.MC','IAG.MC','IBE.MC','IDR.MC','ITX.MC','MAP.MC',
'MEL.MC','MRL.MC','MTS.MC','REE.MC','REP.MC','SAB.MC','SAN.MC','SGRE.MC',
'TEF.MC','TL5.MC','TRE.MC','VIS.MC']

DAX = ['ADS.DE','ALV.DE','BAS.DE','BAYN.DE','BEI.DE','BMW.DE','CBK.DE','CON.DE',
'DAI.DE','DB1.DE','DBK.DE','DPW.DE','DTE.DE','EOAN.DE','FME.DE','FRE.DE',
'HEI.DE','HEN3.DE','IFX.DE','LHA.DE','LIN.DE','MRK.DE','MUV2.DE','PSM.DE',
'RWE.DE','SAP.DE','SIE.DE','TKA.DE','VNA.DE','VOW3.DE']

CAC = ['AC.PA','ACA.PA','AI.PA','AIR.PA','ATO.PA','BN.PA','BNP.PA','CA.PA',
'CAP.PA','CS.PA','DG.PA','EI.PA','EN.PA','ENGI.PA','FP.PA','FR.PA','FTI.PA',
'GLE.PA','KER.PA','LHN.PA','LR.PA','MC.PA','ML.PA','OR.PA','ORA.PA','PUB.PA',
'RI.PA','RNO.PA','SAF.PA','SAN.PA','SGO.PA','STM.PA','SU.PA','SW.PA','UG.PA',
'VIE.PA','VIV.PA']

MIB = ['A2A.MI','ATL.MI','AZM.MI','G.MI','BMED.MI','BAMI.MI','BPE.MI','BRE.MI',
'BZU.MI','CPR.MI','CNHI.MI','ENEL.MI','ENI.MI','EXO.MI','RACE.MI','FCA.MI',
'FBK.MI','G.MI','ISP.MI','IG.MI','LDO.MI','LUX.MI','MS.MI','MB.MI','MONC.MI',
'PST.MI','PRY.MI','REC.MI','SPM.MI','SFER.MI','SRG.MI','STM.MI','TIT.MI',
'TEN.MI','TRN.MI','UBI.MI','UCG.MI','UNI.MI','US.MI','YNAP.MI']

AEX = ['AALB.AS','ABN.AS','AD.AS','AGN.AS','AKZA.AS','ASML.AS','ATC.AS','BOKA.AS',
'DSM.AS','GLPG.AS','GTO.AS','HEIA.AS','INGA.AS','KPN.AS','MT.AS','NN.AS',
'RAND.AS','PHIA.AS','REN.AS','RDSA.AS','SBMO.AS','UL.AS','UNA.AS','VPK.AS',
'WKL.AS']

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(
    description='Nothing'
)
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logging.debug('Only shown in debug mode')

def get_dates(reference=dt.datetime.today()):
    date0 = reference - dt.timedelta(days=15) #15 days from today
    date1 = date0 - dt.timedelta(days=15) #30 days from today
    date2 = date1 - dt.timedelta(days=15) #45 days from today
    date3 = date2 - dt.timedelta(days=15) #2 months from today
    date4 = date3 - dt.timedelta(days=15) #2.5 months from today
    date5 = date4 - dt.timedelta(days=15) #3 months from today
    date6 = date5 - dt.timedelta(days=30) #4 months from today
    date7 = date6 - dt.timedelta(days=30) #5 months from today
    date8 = date7 - dt.timedelta(days=30) #6 months from today
    date9 = date8 - dt.timedelta(days=30) #7 months from today
    date10 = date9 - dt.timedelta(days=30) #8 months from today
    date11 = date10 - dt.timedelta(days=30) #9 months from today
    date12 = date11 - dt.timedelta(days=30) #10 months from today
    date13 = date12 - dt.timedelta(days=60) #12 months from today

    dates = [date0, date1, date2, date3, date4, date5, date6, date7, date8, date9, date10, date11, date12]
    return dates

def testing_db():
    db_conn = create_connection()
    insert_data_db(db_conn, 'SAN.MC', 21, 17.45, 11.448)
    query_db(db_conn)
    rows = query_results(db_conn, 'SAN.MC')
    print("Here are the rows {}".format(rows))


def create_connection(db_file='stocks_db'):
    """ create a database connection to a SQLite database """
    #db_file=':memory:'
    try:
        db = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        logging.error(e)

    create_table_db(db)

    return db


def create_table_db(db, table_name='objectives'):
    """ create a table in our database """
    db.execute('drop table if exists {}'.format(table_name))
    db.execute('create table {} (stock text, objective double, bottom double, activationDay datetime, percentage double)'.format(table_name))


def insert_data_db(db, stock, objective, bottom, activation_day, percentage, table_name='objectives'):
    """ insert a value into the database """
    db.execute('insert into {} (stock, objective, bottom, activationDay, percentage) values (?, ?, ?, ?, ?)'.format(table_name), (stock, objective, bottom, activation_day.to_pydatetime(), percentage))
    db.commit()


def query_db(db, table_name='objectives'):
    """ Queries data from the database """
    cur = db.cursor()
    cur.execute('SELECT * FROM {}'.format(table_name))
    rows = cur.fetchall()
    for row in rows:
        logging.info("This is the row {}".format(row))


def query_results(db_conn, share, table_name='objectives'):
    """ Fetches the objectives from the db """
    cur = db_conn.cursor()
    cur.execute('SELECT * FROM {} WHERE stock = "{}"'.format(table_name, share))
    rows = cur.fetchall()
    for row in rows:
        logging.info("This is the row {}".format(row))

    return rows


def delete_entry_db(db_conn, share, maxim, table_name='objectives'):
    """ Deletes the entry which we already read """
    cur = db_conn.cursor()
    cur.execute('DELETE FROM {} WHERE objective={} and stock="{}"'.format(table_name, maxim, share))


def fetch_data(share, dates, retries=5):
    """ fetches the values from oldest date until today (big amount of data!)"""
    while retries > 0:
        try:
            share_data = data.DataReader(share, 'yahoo', dates[-1], dt.datetime.today())
            break
        except Exception as e:
            #Sometimes the connection is not good, that's why retry
            logging.debug("Trying again %s. Retries remaining %s" %(share, retries))
            time.sleep(2)
            retries -= 1
            if retries == 0:
                logging.info("No more retries for %s" %(share))
                return None
    return share_data


def filter_days(share_data_limited, lowest_days):
    '''
    If there are several days whose value is a bottom, we just want the two
    furthest away because those will give the highest objective
    '''

    final_days = [lowest_days[0]]
    for i,day in enumerate(lowest_days[:-1]):
        # Check if it is the next day. If not, we continue (I compare the value to know if it is the next day)
        if not share_data_limited['Low'].shift(-1).loc[day] == share_data_limited['Low'].loc[lowest_days[i+1]]:
            try:
                final_days[1] = lowest_days[-1]
            except IndexError:
                # The first time we add a second bottom, final_days[1] does not exist
                final_days.append(lowest_days[-1])

    return final_days

def range_maximum(share, dates):
    data_between_min = share.ix[dates[0]:dates[-1]]
    maximum = data_between_min.High.max()
    return maximum

def objective_maximum_value(share, lowest_days, lowest):
    maximum = range_maximum(share, lowest_days)
    objective = 2*maximum - lowest
    logging.debug("The objective is %s and the maximum value is %s" % (objective, maximum))
    return objective, maximum

def is_price_reached(share, price):
    """ Checks if a specific share reached the priced"""

    max = share.High.max()
    if price <= max:
        return True
    else:
        return False

def check_active_objective(share, lowest_days, lowest, today):
    '''
    Checks two things:
      * If the double bottom is activated (it overtook the maximum between double bottom)
      * If the objective was not already reached
    '''

    share_data_after_bottom = share.ix[lowest_days[1]:today]
    objective, maximum_between = objective_maximum_value(share, lowest_days, lowest)

    # We increase a bit the maximum to activate the objective to avoid "al tick"
    maximum_between = maximum_between*1.0015
    if is_price_reached(share_data_after_bottom, maximum_between):
        if not is_price_reached(share_data_after_bottom, objective):
            try:
                price_today = share['Adj Close'].loc[today]
            except:
                logging.info("KAKE")
                price_today = share['Adj Close'].loc[today - dt.timedelta(1)]
            percentage = ((objective - price_today)/price_today)*100
            return percentage, objective
        else:
            logging.debug("Objective %s already reached" % objective)
    else:
        logging.debug("Maximum %s not yet reached. Double bottom not activated yet" %maximum_between)
    return 0,0

def adjust_values(share):
    '''
    Low column is not adjusted to dividends
    '''
    for index, row in share.iterrows():
        if row['Close'] != row['Adj Close']:
            diff = row['Close'] - row['Adj Close']
            logging.debug("The dividend is %s on %s" %(diff, index))
            share.loc[index,'Low'] = share.loc[index,'Low'] - diff
            share.loc[index,'High'] = share.loc[index,'High'] - diff
            share.loc[index,'Open'] = share.loc[index,'Open'] - diff
    return share

def find_double_bottom(dates, data, today=dt.date.today()):
    """ Finds double bottoms """

    results = {}
    for date in dates:

        # today might be the same as date. If it is weekend, it will fail
        if (date == today):
            continue

        logging.debug("\nAnalyzing between dates %s - %s" %(date, today))

        # Grab only from date until today
        share_data_limited = data.ix[date:today]

        # From the set of data, take the smallest value
        lowest = share_data_limited.Low.min()
        logging.debug("\nThis is the date: %s" % date)
        logging.debug("This is the min %s" % lowest)

        # Some tolerance is given, we don't expect exact double bottom
        lowestMin = lowest - lowest * 0.0012
        lowestMax = lowest + lowest * 0.0012

        # Find the day which gave the lowest value
        lowest_day = share_data_limited.idxmin()['Low']

        logging.debug("This is the lowest_day %s" %lowest_day)
        logging.debug("This is the lowestMin %s" %lowestMin)
        logging.debug("This is the lowestMax %s" %lowestMax)

        # Find the days whose value is between the range
        lowest_days = share_data_limited.index[(lowestMin < share_data_limited['Low']) & (lowestMax > share_data_limited['Low'])].tolist()
        lowest_days = filter_days(share_data_limited, lowest_days)
        if len(lowest_days) == 1:
            continue
        else:
            logging.debug(("Potential double bottom in %s on days %s" %(share, lowest_days)))
            percentage, objective = check_active_objective(share_data_limited, lowest_days, lowest, today)
            if percentage:
                results[date] = [percentage, objective, lowest_days, lowest]

    return results


def print_results(results):
    '''
    Print the found objectives, the percentage and the lowest days
    results is a dictionary of lists that contain:
      * [0] --> percentage
      * [1] --> objective
      * [2] --> lowest_days
      * [3] --> bottom value
    '''

    for k, value in results.items():
        print(bcolors.OKGREEN + "Objective to %s already active"
              %value[1] + bcolors.ENDC)
        print("This is the potential gain %s%%" % value[0])
        print("These are the bottom days %s" % value[2])

def store_results(results, db_conn, share):
    '''
    Store the found objectives in sqlite, the percentage and the
    lowest days results is a dictionary of lists that contain:
      * [0] --> percentage
      * [1] --> objective
      * [2] --> lowest_days: [2][1] is the activation day
      * [3] --> bottom value
    '''
    for k, value in results.items():
        insert_data_db(db_conn, share, value[1], value[3], value[2][1], value[0])

    print_results(results)


def check_prev_objectives(db_conn, share, data, dates):
    rows = query_results(db_conn, share)
    for row in rows:
        maxim = row[1]
        minim = row[2]
        activation_day = row[3]
        share_data_limited = data.ix[activation_day:dates[0]]

        lowest = share_data_limited.Low.min()
        highest = share_data_limited.High.max()

        if (lowest < minim) and (highest > maxim):
            print("FUUUCKKK")
            delete_entry_db(db_conn, share, maxim)
        elif (lowest < minim):
            print("CANCELLED OBJECTIVE")
            delete_entry_db(db_conn, share, maxim)
        elif (highest > maxim):
            print("OBJECTIVE ACHIEVED. CONGRATULATIONS!!")
            delete_entry_db(db_conn, share, maxim)


if __name__ == '__main__':

    debug = ['SAN.MC']
#    debug = 0

#    testing_db()
#    sys.exit(0)

    start_date = dt.datetime(2013, 1, 1) #we would start one year earlier
    days_delay = 0
    historic_analysis = True

    if historic_analysis:
            db_conn = create_connection()

    for share in debug:
#    for share in IBEX + DAX + CAC + MIB + AEX:

        if historic_analysis:
            reference_print = start_date + dt.timedelta(days=1920)
            dates_print = get_dates(reference_print)
            logging.info("The historic analisys will be made from {} until {}\n".format(start_date, dates_print[0]))
            dates = get_dates(start_date)
            share_data = fetch_data(share, dates)

            # Check if share_data is the correct object and not None
            if not hasattr(share_data, 'to_sql'):
                continue
            logging.debug(share_data)

            # Fix bug in the low column
            adjusted_data = adjust_values(share_data)

            # 2000 is a bit more than 5 years
            while(days_delay<2000):
                reference = start_date + dt.timedelta(days=days_delay)
                dates = get_dates(reference)
                days_delay += 120 #4 months in next iteration

                logging.info("\nAnalyzing %s between dates %s - %s" %(share, dates[-1], dates[0]))

                check_prev_objectives(db_conn, share, adjusted_data, dates)

                results = find_double_bottom(dates, adjusted_data, today=dates[0])
                store_results(results, db_conn, share)

        else:
            dates = get_dates()
            share_data = fetch_data(share, dates)

            # Check if share_data is the correct object and not None
            if not hasattr(share_data, 'to_sql'):
                continue
            logging.debug(share_data)

            # Fix bug in the low column
            adjusted_data = adjust_values(share_data)
            logging.info("\nAnalyzing %s" % share)

            results = find_double_bottom(dates, adjusted_data)
            print_results(results)
