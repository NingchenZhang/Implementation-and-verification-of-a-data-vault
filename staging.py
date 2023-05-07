import csv
import os
import psycopg2  ##library
import time
import string
import numpy as np
import pandas as pd
from hashlib import md5
from io import StringIO


def encrypt_md5(s):
    # create md5 object
    new_md5 = md5()
    new_md5.update(s.encode(encoding='utf-8'))
    # encrypt
    return new_md5.hexdigest()


class AmiraReader(object):
    # Class constructor
    def __init__(self, _filename):
        """Class constructor"""
        # Initialize private attributes unique to this instance
        ##COMPLETE THIS PART
        self._filename = ''


class AmiraReader(AmiraReader):
    def _findField(self, file, fieldName):
        """Parses the Amira file to find a field name"""
        ##COMPLETE THIS PART
        try:
            while True:
                text_line = file.readline()
                if fieldName in text_line:
                    return text_line
                    break
        finally:
            print('')


class AmiraReader(AmiraReader):
    def CorrectStr(self, fieldName, p):
        line = p.replace(',', '')
        line = line.replace(fieldName, '')
        result = line.strip()
        return result


factor = ['']
compare = []
Namecompare = []

object = AmiraReader('')
# connect to the local database ----------------------------------
databasename = input("please input your database name ")
user = input("please input your  user ")
password = input("please input your  password ")
host = input("please input your host ")
port = input("please input your port ")
conn = psycopg2.connect(database=databasename, user=user, password=password, host=host, port=port)
# conn = psycopg2.connect(database="smdvault", user="postgres", password="chunji520", host="localhost", port="5432")
## finish connect
print('postgreSQL connect success!')
folder = input('please input the name of data folder: ')
file = folder
source = {}

i = 0
##--First should processed data from csv files
for root, dirs, files in os.walk(file):
    for file in files:
        path = os.path.join(root, file)
        # -------get the source of file
        source[i] = file
        with open('Dataset1_VM_BlindedAndReduced\VMData_Blinded' +'/' + source[i], 'r') as file:
            item = 0
            initial = object._findField(file, 'ID')
            ID = object.CorrectStr('ID', initial)
            nextline = file.readline()
            Name = object.CorrectStr('Name', nextline)
            nextline = file.readline()
            Age = object.CorrectStr('Age', nextline)
            nextline = file.readline()
            Sex = object.CorrectStr('Sex', nextline)
            nextline = file.readline()
            AnalyzeMode = object.CorrectStr('AnalyzeMode', nextline)
            nextline = file.readline()
            PreTimes = object.CorrectStr('Pre Time[s]', nextline)
            nextline = file.readline()
            PostTimes = object.CorrectStr('Post Time[s]', nextline)
            nextline = file.readline()
            RecoveryTimes = object.CorrectStr('Recovery Time[s]', nextline)
            nextline = file.readline()
            BaseTimes = object.CorrectStr('Base Time[s]', nextline)
            nextline = file.readline()
            Date = object.CorrectStr('Date', nextline)
            nextline = file.readline()
            Mode = object.CorrectStr('Mode', nextline)
            nextline = file.readline()
            Wave = object.CorrectStr('Wave[nm]', nextline)
            nextline = file.readline()
            SamplingPeriod = object.CorrectStr('Sampling Period[s]', nextline)
            nextline = file.readline()
            StimType = object.CorrectStr('StimType', nextline)
            nextline = file.readline()
            nextline = file.readline()
            StimTime = object.CorrectStr('', nextline)
            nextline = file.readline()
            RepeatCount = object.CorrectStr('Repeat Count', nextline)
            factor = [AnalyzeMode,PreTimes, PostTimes, RecoveryTimes, BaseTimes, Mode, SamplingPeriod, StimType, StimTime, RepeatCount]
            factorName = ['AnalyzeMode', 'PreTimes', 'PostTimes', 'RecoveryTimes', 'BaseTimes',
                           'Mode', 'SamplingPeriod', 'StimType', 'StimTime', 'RepeatCount']
            keyvalue = [ID, Name, Age, Sex, AnalyzeMode, PreTimes, PostTimes, RecoveryTimes, BaseTimes, Mode, SamplingPeriod,
                        StimType, StimTime, RepeatCount]
            valueobject = ['ID', 'Name', 'Age', 'Sex', 'AnalyzeMode', 'PreTimes', 'PostTimes', 'RecoveryTimes', 'BaseTimes',
                           'Mode', 'SamplingPeriod', 'StimType', 'StimTime', 'RepeatCount']
            Group = ['Moto_HBA_Probe1_Deoxy','Moto_HBA_Probe1_Oxy','Rest_HBA_Probe1_Deoxy','Rest_HBA_Probe1_Oxy','ViMo_HBA_Probe1_Deoxy',
                     'ViMo_HBA_Probe1_Oxy','Viso_HBA_Probe1_Deoxy','Viso_HBA_Probe1_Oxy']
            Groupobservation = ['Moto_MES','Rest_MES','ViMo_MES','Viso_MES']
            file.close()
        # ------------------------Finish reading the Header
        # ------------------------Get the data from excel

        df = pd.read_csv(path, index_col=0, header=27)
        df.head()
        #if 'Deoxy' or 'Oxy' in source[i]:
        df.dropna(axis=1, inplace=True)
        #print(df)
        timeObserve = df['Time']  # --get observation time Time
        timeObserve = np.array(timeObserve)
        timeObserve = timeObserve.tolist()
        del df['Time']
        Data = np.array(df)
        Data = Data.tolist()


        sequenceid = encrypt_md5(ID + str(i))
        sourcehash = encrypt_md5(source[i])

        # ------prepare to insert
        cursor = conn.cursor()
        ##use cursor method to operate the database
        # ---insert data into database

        # ----PK (sequenceid,Date,source)
        subjecthash = encrypt_md5(Name)
        Age = Age[0:2]
        try:
            age = int(Age)
        except:
            age = int(Age[0:1])

        insert_sql = """INSERT INTO public.HubExperiment values(%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(sequenceid,Date,sourcehash))
        insert_sql = """INSERT INTO public.SatExperimentTitle values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(sequenceid,Date,sourcehash,ID))

        insert_sql = """INSERT INTO public.SatExperimentAcronym values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(sequenceid,Date,sourcehash,ID))

        # C:\Users\11847\Desktop\LM\project\Dataset1_VM_BlindedAndReduced\VMData_Blinded
        s = ID[0:6]

        # ---finish Session
        session = encrypt_md5(s)  #


        insert_sql = """INSERT INTO public.HubSession values(%s,%s,%s) ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(session,Date,sourcehash))

        insert_sql = """INSERT INTO public.SatSessionName values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(session,Date,sourcehash,s))


        # ---observation
        observationhash = encrypt_md5('observationhash' + str(i))

        insert_sql = """INSERT INTO public.HubObservation values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(observationhash,Date,sourcehash,session))
        insert_sql = """INSERT INTO public.SatObservationName values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(observationhash,Date,sourcehash,source[i]))
        insert_sql = """INSERT INTO public.SatObservationValue values(%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(observationhash,Date,sourcehash,Data,timeObserve))


        # ------------------------------------------------------------------------------
        # --ExperimentUnit and Subject
        insert_sql = """INSERT  INTO  public.HubExperimentUnit values(%s,%s,%s) ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(subjecthash,Date,sourcehash))
        insert_sql = """INSERT INTO public.HubSubject values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(subjecthash,Date,sourcehash,Name))

        insert_sql = """INSERT INTO public.SatSubjectAge values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(subjecthash,Date,sourcehash,(age,)))
        insert_sql = """INSERT INTO public.SatSubjectName values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(subjecthash,Date,sourcehash,[]))#for the privacy policy


        # ---Participatesln
        Participatslnhash = encrypt_md5('Participatslnhash' + str(i))
        insert_sql = """INSERT INTO public.Participatesln values(%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(Participatslnhash,Date,sourcehash,subjecthash,sequenceid))
        insert_sql = """INSERT INTO public.SatExperimentUnitIdentifier values(%s,%s,%s,%s) ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql,(Participatslnhash,Date,sourcehash,ID))

        # ---HubMetadata
        insert_sql = """INSERT INTO public.HubMetadata values(%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql, (sequenceid, Date, sourcehash))
        insert_sql = """INSERT INTO public.SatMetaDataKeyValuePair values(%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql, (sequenceid, Date, sourcehash, valueobject, keyvalue))
        insert_sql = """INSERT INTO public.SessionMetaData values(%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql, (sequenceid, Date, sourcehash, session, sequenceid))
        insert_sql = """INSERT INTO public.ObservationMetaData values(%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
        cursor.execute(insert_sql, (sequenceid, Date, sourcehash, observationhash, sequenceid))

        #--Factor
        j = 0
        while j < len(factorName):
            factornumber = 'factorName' + str(j)
            treatmenthash = encrypt_md5('treatment' + str(j))
            factornumber_hash = encrypt_md5(str(factornumber))
            insert_sql = """INSERT INTO public.HubFactor values(%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
            cursor.execute(insert_sql, (factornumber_hash, Date, sourcehash, sequenceid, False))
            insert_sql = """INSERT INTO public.SatFactorName values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
            cursor.execute(insert_sql, (factornumber_hash, Date, sourcehash, [factorName[j],]))
            insert_sql = """INSERT INTO public.SatFactorLevel values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
            cursor.execute(insert_sql, (factornumber_hash, Date, sourcehash, factor[j]))
            insert_sql = """INSERT INTO public.HubTreatment values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
            cursor.execute(insert_sql, (treatmenthash, Date, sourcehash, sequenceid))
            insert_sql = """INSERT INTO public.SatTreatmentFactorLevel values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
            cursor.execute(insert_sql, (treatmenthash, Date, sourcehash, factor[j]))
            j = j+1
        k = 0#loop control
        g = 0

        while k<len(Group):

            if Group[k] in source[i]:
                grouphash = encrypt_md5('group' + str(k))
                insert_sql = """INSERT INTO public.HubGroup values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
                cursor.execute(insert_sql, (grouphash, Date, sourcehash, treatmenthash))
                insert_sql = """INSERT INTO public.SatGroupName values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
                cursor.execute(insert_sql, (grouphash, Date, sourcehash, [Group[k],]))
                insert_sql = """INSERT INTO public.AssignedTo values(%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
                cursor.execute(insert_sql, (sequenceid, Date, sourcehash, subjecthash,grouphash))
                insert_sql = """INSERT INTO public.AttendsSession values(%s,%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
                cursor.execute(insert_sql, (sequenceid, Date, sourcehash, subjecthash, grouphash, session))

            k = k+1
        while g < len(Groupobservation):
            if Groupobservation[g] in source[i]:
                grouphash = encrypt_md5('groupGroupobservation' + str(g))
                insert_sql = """INSERT INTO public.HubGroup values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
                cursor.execute(insert_sql, (grouphash, Date, sourcehash, treatmenthash))
                insert_sql = """INSERT INTO public.SatGroupName values(%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
                cursor.execute(insert_sql, (grouphash, Date, sourcehash, [Groupobservation[g], ]))
                insert_sql = """INSERT INTO public.AssignedTo values(%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
                cursor.execute(insert_sql, (sequenceid, Date, sourcehash, subjecthash, grouphash))
                insert_sql = """INSERT INTO public.AttendsSession values(%s,%s,%s,%s,%s,%s)ON conflict(sequencehash) do nothing"""
                cursor.execute(insert_sql, (sequenceid, Date, sourcehash, subjecthash, grouphash, session))
            g = g + 1
        #---AssignedTo


        # ## send SQL order
            conn.commit()
        print('Finish file: ', source[i])
        i = i + 1
print('Finish input data from folder')




