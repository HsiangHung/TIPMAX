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




