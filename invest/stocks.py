import argparse
import datetime as dt
import logging
import pdb
import sqlite3
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

today = dt.datetime.today()
date0 = today - dt.timedelta(days=15) #15 days from today
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
print(dates)

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

def testing_db():
    conn = create_connection()
    insert_data_db(conn, 'ENDESA', 21, 18.4, 12.052)
    query_db(conn, 'objectives')

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
    db.execute('create table {} (stock text, objective double, bottom double, percentage double)'.format(table_name))

def insert_data_db(db, stock, objective, bottom, percentage, table_name='objectives'):
    """ insert a value into the database """
    db.execute('insert into {} (stock, objective, bottom, percentage) values (?, ?, ?, ?)'.format(table_name), (stock, objective, bottom, percentage))
    db.commit()

def query_db(db, table_name):
    """ Queries data from the database """
    cur = db.cursor()
    cur.execute('SELECT * FROM {}'.format(table_name))
    rows = cur.fetchall()
    for row in rows:
        logging.info("This is the row {}".format(row))

def fetch_data(share, retries=5):
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
    max = share.High.max()
    if price <= max:
        return True
    else:
        return False

def check_active_objective(share, lowest_days, lowest):
    share_data_after_bottom = share.ix[lowest_days[1]:dt.datetime.today()]
    objective, maximum_between = objective_maximum_value(share, lowest_days, lowest)
    # We increase a bit the maximum to activate the objective to avoid "al tick"
    maximum_between = maximum_between*1.0015
    if is_price_reached(share_data_after_bottom, maximum_between):
        if not is_price_reached(share_data_after_bottom, objective):
            try:
                price_today = share['Close'].loc[dt.date.today()]
            except:
                logging.info("KAKE")
                price_today = share['Close'].loc[dt.date.today() - dt.timedelta(1)]
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

if __name__ == '__main__':

    pdb.set_trace()
    testing_db()

#    debug = ['GI.MI']
    debug = 0

#    for share in debug:
    for share in IBEX + DAX + CAC + MIB + AEX:
        share_data = fetch_data(share)

        # Check if share_data is the correct object and not None
        if not hasattr(share_data, 'to_sql'):
            continue
        logging.debug(share_data)

        # Fix bug in the low column
        adjusted_data = adjust_values(share_data)
        logging.info("\nAnalyzing %s" % share)

        for date in dates:
            # Grab only from date until today
            share_data_limited = adjusted_data.ix[date:dt.date.today()]
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
                percentage, objective = check_active_objective(share_data_limited, lowest_days, lowest)
                if percentage:
                    print(bcolors.OKGREEN + "Objective to %s already active"
                          %objective + bcolors.ENDC)
                    print("This is the potential gain %s%%" % percentage)
                    print("These are the bottom days %s" % lowest_days)
