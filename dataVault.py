import psycopg2 ##library

#connect to the local database
databasename = input("please input your database name ")
user = input("please input your  user ")
password = input("please input your  password ")
host = input("please input your host ")
port = input("please input your port ")
conn = psycopg2.connect(database=databasename, user=user, password=password, host=host, port=port)

## finish connect
print('postgreSQL connect success!')
cursor=conn.cursor()
##use cursor method to operate the database
#can change the right of database
cursor.execute('''create table if not exists public.HubExperiment(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
primary key(sequencehash,timestamptime,sourcehash)
)''')
cursor.execute('''create table if not exists public.HubFactor(
sequencehash varchar(100) UNIQUE not null ,
timestamptime varchar(50)  not null,
sourcehash varchar(100)  not null,
experimenthash varchar(100) not null,
isCofactor boolean DEFAULT false,
FOREIGN KEY (experimenthash) references HubExperiment(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatExperimentTitle(
sequencehash varchar(100) unique not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
title varchar(255),
FOREIGN KEY (sequencehash) references HubExperiment(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatExperimentAcronym(
sequencehash varchar(100) unique not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
acronym varchar(15),
FOREIGN KEY (sequencehash) references HubExperiment(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')
###---
cursor.execute('''create table if not exists public.HubTreatment(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
experimenthash varchar(100) not null references HubExperiment(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')


cursor.execute('''create table if not exists public.SatFactorName(
sequencehash varchar(100) unique not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
name varchar(40),
FOREIGN KEY (sequencehash) references HubFactor(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatFactorLevel(
sequencehash varchar(100) unique not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
levelValue varchar(40),
FOREIGN KEY (sequencehash) references HubFactor(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.HubExperimentUnit(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
primary key (sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.Participatesln(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
experimentalUnithash varchar(100) not null,
grouphash varchar(100) not null,
FOREIGN KEY (experimentalUnithash) references HubExperimentUnit(sequencehash),
FOREIGN KEY (grouphash) references HubExperiment(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatExperimentUnitidentifier(
sequencehash varchar(100) unique not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
ID varchar(15),
FOREIGN KEY (sequencehash) references Participatesln(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.HubSubject(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
name varchar(40),
primary key(sequencehash,timestamptime,sourcehash,name)
)''')

cursor.execute('''create table if not exists public.SatSubjectAge(
sequencehash varchar(100) unique not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
age int,
FOREIGN KEY (sequencehash) references HubSubject(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatSubjectName(
sequencehash varchar(100) unique not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
name varchar(40),
FOREIGN KEY (sequencehash) references HubSubject(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')
###---
cursor.execute('''create table if not exists public.SatTreatmentFactorLevel(
sequencehash varchar(100) unique not null,
timestamptime varchar(50)  not null, 
sourcehash varchar(100)  not null,
levelValue varchar(40), 
FOREIGN KEY (sequencehash) references HubTreatment(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.HubGroup(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
treatmenthash varchar(100) not null,
FOREIGN KEY (treatmenthash) references HubTreatment(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatGroupName(
sequencehash varchar(100) unique not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
name varchar(40) not null,
FOREIGN KEY (sequencehash) references HubGroup(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.AssignedTo(
sequencehash varchar(100) unique not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
experimentalUnithash varchar(100) not null,
grouphash varchar(100) not null,
FOREIGN KEY (experimentalUnithash) references HubExperimentUnit(sequencehash),
FOREIGN KEY (grouphash) references HubGroup(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.HubSession(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatSessionName(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
name varchar(40),
FOREIGN KEY (sequencehash) references HubSession(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.AttendsSession(
sequencehash varchar(100) unique not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
experimentalUnithash varchar(100) not null,
grouphash varchar(100) not null,
sessionhash varchar(100) not null,
FOREIGN KEY (experimentalUnithash) references HubExperimentUnit(sequencehash),
FOREIGN KEY (grouphash) references HubGroup(sequencehash),
FOREIGN KEY (sessionhash) references HubSession(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.HubMetadata(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatMetaDataKeyValuePair(
sequencehash varchar(100) unique not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100) not null,
key varchar(200) not null,
valueobject text[],
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.HubObservation(
sequencehash varchar(100) UNIQUE not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
collecedAtSessionhash varchar(100) not null,
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.ObservationMetaData(
sequencehash varchar(100) unique not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
observationhash varchar(100) not null,
metadatahash varchar(100) not null,
FOREIGN KEY (observationhash) references HubObservation(sequencehash),
FOREIGN KEY (metadatahash) references HubMetadata(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SessionMetaData(
sequencehash varchar(100) unique not null,
timestamptime varchar(50) not null, 
sourcehash varchar(50)  not null,
sessionhash varchar(100) not null,
metadatahash varchar(100) not null,
FOREIGN KEY (sessionhash) references HubSession(sequencehash),
FOREIGN KEY (metadatahash) references HubMetadata(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')

cursor.execute('''create table if not exists public.SatObservationName(
sequencehash varchar(100) unique not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
name varchar(40) not null,
FOREIGN KEY (sequencehash) references HubObservation(sequencehash),
primary key(sequencehash,timestamptime,sourcehash)
)''')


cursor.execute('''create table if not exists public.SatObservationValue(
sequencehash varchar(100) unique not null,
timestamptime varchar(50) not null, 
sourcehash varchar(100)  not null,
valuearray varchar[5000],
timestampsarray varchar[5000],
FOREIGN KEY (sequencehash) references HubObservation(sequencehash),
primary key (sequencehash,timestamptime,sourcehash)
)''')

conn.commit()  ##send order to postgreSQL database
conn.close()
print('finish')
