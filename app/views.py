from app import app
from flask import jsonify
from cassandra.cluster import Cluster
cluster = Cluster(['52.72.109.43','52.22.233.5','52.21.15.67','52.2.153.27'])
session2009 = cluster.connect('taxi_2009')
session2010 = cluster.connect('taxi_2010')
session2011 = cluster.connect('taxi_2011')
session2012 = cluster.connect('taxi_2012')
session2013 = cluster.connect('taxi_2013')
session2014 = cluster.connect('taxi_2014')
session2015 = cluster.connect('taxi_2015')


from flask import render_template, request
from datetime import datetime
#import MySQLdb as mdb



@app.route('/realtime')
def realtime():
    return render_template("realtime.html")


################################################################################################

@app.route("/")
def map():
    return render_template('basemap.html')#, my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


@app.route("/index")
def template_test():
    return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])



@app.route('/output') 
def output():
       date = request.args.get('date')
       time = request.args.get('time')
       year  = datetime.strptime(date,'%Y-%m-%d').strftime('%Y')
       month = datetime.strptime(date,'%Y-%m-%d').strftime('%m')
       day   = datetime.strptime(date,'%Y-%m-%d').strftime('%d')
       table = 'y_'+str(year)+'_'+str(month)+'_'+str(day)
       hour  = datetime.strptime(time,'%H:%M:%S').strftime('%H')
       min   = datetime.strptime(time,'%H:%M:%S').strftime('%M')
       sec   = datetime.strptime(time,'%H:%M:%S').strftime('%S')
       Time = int(str(hour)+str(min)+str(sec))
       Date = date#"2009-05-15"
       #table='y_2009_05_15'
       #Time = 182900
       Time_1 = Time
       Time_2 = int(Time)+500
       if Time_1 >= 235500: Time_2 = 235959
#       print time_1, time_2
       stmt= "SELECT * FROM "+table+" WHERE apick_date=%s and bpick_time >= %s and bpick_time <= %s"
       if year == '2009': response = session2009.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2010': response = session2010.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2011': response = session2011.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2012': response = session2012.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2013': response = session2013.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2014': response = session2014.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2015': response = session2015.execute(stmt,parameters=[Date, Time_1, Time_2])
       #response = session.execute(stmt,parameters=[Date, Time_1, Time_2])
       taxi = []
       for val in response:
#            val = val
            taxi.append([float(val.pick_loc.replace('[','').replace(']','').split(',')[1].encode('utf-8')),\
                         float(val.pick_loc.replace('[','').replace(']','').split(',')[0].encode('utf-8')),\
                         float(val.tipsratio.encode('utf-8'))] )
#       jsonresponse = [{"x ": x.pick_loc.replace('[','').replace(']','').split(',')[1], \
#                        "y ": x.pick_loc.replace('[','').replace(']','').split(',')[0], \
#                       "tips ratio ": x.tipsratio} for x in taxi]
#       jsonresponse = [{"x ": x[0], "y ": x[1], "tips rate ": x[2]} for x in taxi]
#       return jsonify(data=jsonresponse)
       return render_template('output.html', taxidata=taxi, date=date, time=time)



#######################################################################################################


@app.route('/tipinput')
def tipinput():
       return render_template("tipinput.html")



@app.route('/tipoutput')
def tipoutput():
       date = request.args.get('date')
       time = request.args.get('time')
       year  = datetime.strptime(date,'%Y-%m-%d').strftime('%Y')
       month = datetime.strptime(date,'%Y-%m-%d').strftime('%m')
       day   = datetime.strptime(date,'%Y-%m-%d').strftime('%d')
       table = 'y_'+str(year)+'_'+str(month)+'_'+str(day)
       hour  = datetime.strptime(time,'%H:%M:%S').strftime('%H')
       min   = datetime.strptime(time,'%H:%M:%S').strftime('%M')
       sec   = datetime.strptime(time,'%H:%M:%S').strftime('%S')
       Time = int(str(hour)+str(min)+str(sec))
       Date = date#"2009-05-15"
       Time_1 = Time
       Time_2 = int(Time)+500
       if Time_1 >= 235500: Time_2 = 235959
       stmt= "SELECT * FROM "+table+" WHERE apick_date=%s and bpick_time >= %s and bpick_time <= %s"
       if year == '2009': response = session2009.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2010': response = session2010.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2011': response = session2011.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2012': response = session2012.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2013': response = session2013.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2014': response = session2014.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2015': response = session2015.execute(stmt,parameters=[Date, Time_1, Time_2])
       #response = session.execute(stmt,parameters=[Date, Time_1, Time_2])
       taxi = []
       for val in response:
#            val = val
            taxi.append([float(val.pick_loc.replace('[','').replace(']','').split(',')[1].encode('utf-8')),\
                         float(val.pick_loc.replace('[','').replace(']','').split(',')[0].encode('utf-8')),\
                         50*float(val.tipsratio.encode('utf-8'))] )
       return render_template('tipoutput.html', taxidata=taxi, date=date, time=time)



######################################################################################################                 


@app.route('/fareinput')
def fareinput():
       return render_template("fareinput.html")


@app.route('/fareoutput')
def fareoutput():
       date = request.args.get('date')
       time = request.args.get('time')
       year  = datetime.strptime(date,'%Y-%m-%d').strftime('%Y')
       month = datetime.strptime(date,'%Y-%m-%d').strftime('%m')
       day   = datetime.strptime(date,'%Y-%m-%d').strftime('%d')
       table = 'y_'+str(year)+'_'+str(month)+'_'+str(day)
       hour  = datetime.strptime(time,'%H:%M:%S').strftime('%H')
       min   = datetime.strptime(time,'%H:%M:%S').strftime('%M')
       sec   = datetime.strptime(time,'%H:%M:%S').strftime('%S')
       Time = int(str(hour)+str(min)+str(sec))
       Date = date
       Time_1 = Time
       Time_2 = int(Time)+500
       if Time_1 >= 235500: Time_2 = 235959
       stmt= "SELECT * FROM "+table+" WHERE apick_date=%s and bpick_time >= %s and bpick_time <= %s"
       if year == '2009': response = session2009.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2010': response = session2010.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2011': response = session2011.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2012': response = session2012.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2013': response = session2013.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2014': response = session2014.execute(stmt,parameters=[Date, Time_1, Time_2])
       if year == '2015': response = session2015.execute(stmt,parameters=[Date, Time_1, Time_2])
       #response = session.execute(stmt,parameters=[Date, Time_1, Time_2])
       taxi = []
       for val in response:
            taxi.append([float(val.pick_loc.replace('[','').replace(']','').split(',')[1].encode('utf-8')),\
                         float(val.pick_loc.replace('[','').replace(']','').split(',')[0].encode('utf-8')),\
                         float(val.totalpay.encode('utf-8'))] )
       return render_template('fareoutput.html', taxidata=taxi, date=date, time=time)



################################################################################################

@app.route('/api/rt/')
def realtimeoutput2():
       now_time = datetime.now(timezone('US/Eastern'))

       year  = now_time.strftime('%Y')
       month = now_time.strftime('%m')
       day   = now_time.strftime('%d')
       realDate = str(str(year)+str(month).zfill(2)+str(day).zfill(2))

       hour = now_time.strftime('%H')
       mins = now_time.strftime('%M')
       sec  = now_time.strftime('%S')

       realTime = int(str(hour)+str(mins)+str(sec))

       if int(mins) >= 4:
           pastTime = int(str(hour)+str(int(mins)-4).zfill(2)+str(sec).zfill(2))
       else:
           pastTime = int(str(int(hour)-1)+str(int(mins)+60-4).zfill(2)+str(sec).zfill(2))


       #stmt= "SELECT * FROM agg WHERE date=%s and time = %s"                                                           
       #response = session.execute(stmt,parameters=[realDate,realTime])                                                 

       stmt= "SELECT * FROM agg WHERE date=%s and time >= %s"
       response = session.execute(stmt,parameters=[realDate,pastTime])

       taxi = []
       #date and time                                                                                                   
       for val in response:
            date= val.date.encode('utf-8')
            time= str(val.time)
            #print time                                                                                                 
            year = date[:4]
            month= date[4:6]
            day  = date[6:]
            if len(time) == 6:
                hour = time[:2]
                mins = time[2:4]
                sec  = time[4:]
            elif len(time) == 5:
                hour = time[:1]
                mins = time[1:3]
                sec  = time[3:]
            elif len(time) == 4:
                hour = '00'
                mins = time[:2]
                sec  = time[2:]
            elif len(time) == 3:
                hour = '00'
                mins = '0'+time[:1]
                sec  = time[1:]
           elif len(time) == 2:
                hour = '00'
                mins = '00'
                sec  = time[:]
            tstamp= str(year+'-'+month+'-'+day+' '+hour+':'+mins+':'+sec)
            taxi.append([tstamp,float(val.avg.encode('utf-8')),float(val.max.encode('utf-8')\
)  ] )
      
       ###### -------------------------------------------------------
       
       stmt= "SELECT * FROM agg_cash WHERE date=%s and time >= %s"
       response = session.execute(stmt,parameters=[realDate,pastTime])

       cash = []
       for val in response:
            date= val.date.encode('utf-8')
            time= str(val.time)
            #print time                                                                                                 
            year = date[:4]
            month= date[4:6]
            day  = date[6:]
            if len(time) == 6:
                hour = time[:2]
                mins = time[2:4]
                sec  = time[4:]
            elif len(time) == 5:
		        hour = time[:1]
                mins = time[1:3]
                sec  = time[3:]
            elif len(time) == 4:
                hour = '00'
                mins = time[:2]
                sec  = time[2:]
            elif len(time) == 3:
                hour = '00'
                mins = '0'+time[:1]
                sec  = time[1:]
            elif len(time) == 2:
                hour = '00'
                mins = '00'
                sec  = time[:]
                
            tstamp= str(year+'-'+month+'-'+day+' '+hour+':'+mins+':'+sec)
            cash.append([tstamp,float(val.avg.encode('utf-8')),float(val.max.encode('utf-8'))  ] )
                                                                                  
        return render_template('realtimegraph.html', taxidata=taxi, cashdata=cash)


###################################################################################################### 


@app.route('/tipshistory')
def timeseriesplot():
       #numData = request.args.get('numData')

       now_time = datetime.now(timezone('US/Eastern'))

       hour = now_time.strftime('%H')
       mins = now_time.strftime('%M')
       sec  = now_time.strftime('%S')

       currentTime = int(str(hour)+str(mins)+str(sec))
       earlyTime   = int(currentTime)+6000
       if currentTime >= 235500: earlyTime = 235959
       tipsavg = []
       for i in range(100):
           if i ==0:
               ## put the followings ints
               year  = 2015#now_time.strftime('%Y')
               month = 2#now_time.strftime('%m')
               day   = 23#now_time.strftime('%d')              
           else:
               if day > 7:
                   day = day-7
               else:
                   if month >1:
                      day = day-7+numdays[month-1]
                      month = month -1
                   else:
                      day = day-7 +numdays[12]  ## back to a year
                      month = 12
                      year= year -1


           Date = str(str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2))
           table = 'y_'+str(year)+'_'+str(month).zfill(2)+'_'+str(day).zfill(2)


           #print Date, currentTime

          stmt= "SELECT * FROM "+table+" WHERE apick_date=%s and bpick_time >= %s and bpick_time <= %s"

           if year == 2009: response = session2009.execute(stmt,parameters=[Date, currentTime, earlyTime])
           if year == 2010: response = session2010.execute(stmt,parameters=[Date, currentTime, earlyTime])
           if year == 2011: response = session2011.execute(stmt,parameters=[Date, currentTime, earlyTime])
           if year == 2012: response = session2012.execute(stmt,parameters=[Date, currentTime, earlyTime])
           if year == 2013: response = session2013.execute(stmt,parameters=[Date, currentTime, earlyTime])
           if year == 2014: response = session2014.execute(stmt,parameters=[Date, currentTime, earlyTime])
           if year == 2015: response = session2015.execute(stmt,parameters=[Date, currentTime, earlyTime])

           taxi = []
           for val in response:
               taxi.append(float(val.tipsratio.encode('utf-8')))

           print len(taxi), sum(taxi), sum(taxi)/len(taxi)
           tipsavg.append([Date,sum(taxi)/len(taxi)])

       #return jsonify(taxidata=tipsavg) 
       return render_template('singlePlot.html', taxidata=tipsavg)
