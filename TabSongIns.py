from flask import Flask, render_template, request, send_file, url_for , request,flash
import sqlite3 as sql
from werkzeug.utils import secure_filename
import os
from distutils.log import debug
from fileinput import filename
from flask import * 

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['mp3'])
UPLOAD_FOLDER = '\\Upload\\static'

app.config['UPLOAD_FOLDER']='Upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(os.path.dirname(__file__))
print(os.path.dirname(__file__)+'\static')
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))
print(ROOT_DIR)

@app.route('/')
   
def home():
    return render_template('song.html')

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/enternew')
def new_song():
   return render_template('song.html')
   
   
   
# create addrec function for Add files
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         
         # Get the list of files from webpage
         files = request.files.getlist("file")
         print("Stored blob data file location: ", files, "\n")
                 
         #Iterate for each file in the files List, and Save them
         for file in files:
            file.save(os.path.join(ROOT_DIR, secure_filename(file.filename)))
                     
         print("File Name: ", file.filename, "\n")
         
         #song = convertToBinaryData(file.filename)
         song = convertToBinaryData(os.path.join(ROOT_DIR, secure_filename(file.filename)))
         title = request.form['title']
         artist = request.form['artist']
         album = request.form['album']
         song_name =file.filename.replace(' ', '_')
         
         
         with sql. connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO songs (title,artist,album,song_name,song) VALUES (?,?,?,?,?)",(title,artist,album,song_name,song) )
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("resultSong.html",msg = msg)
         con.close()
    
         
def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
    #with open(os.path.join(ROOT_DIR, secure_filename(file.filename)), 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")
    

# create list function for list files
@app.route('/listSong')
def list():
 try: 
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from songs")
   
   
   rows = cur.fetchall();
   for row in rows:
            print("Id = ", row[0], "Name = ", row[1], "Song Name = ", row[4])
            id = row[0]
            title = row[1]
            artist = row[2]
            album = row[3]
            song_name= row[4]
            song = row[5]
            audio_files = song_name 	# an mp3 extension
           
               
   #songPath = "E:\TestBlob\\" + song_name 
   #writeTofile(song, songPath)
 except:
         con.rollback()
         msg = "error in insert operation"
 finally:
   return render_template("listSong.html",rows = rows,file=audio_files)
   con.close()    
   
   
   
   
# create upload function for upload files
@app.route('/upload', methods=['POST'])   
def upload():
    if request.method == 'POST':
  
        # Get the list of files from webpage
        files = request.files.getlist("file")
        print("Stored blob data file location: ", files, "\n")
        
        # Iterate for each file in the files List, and Save them
        for file in files:
            file.save(file.filename)
        msg = "Song Uploaded Successfully.!"    
        #return "<h1>Song Uploaded Successfully.!</h1>"   
        return render_template("Song.html",msg = msg)




# create download function for download files
@app.route("/download/<int:sond_id>")
def download_file(sond_id):
 try:
   print("App Path in Download",app.root_path)
   app.root_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))
   print(app.root_path)
     
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from songs where sond_id = ?;",[sond_id])
      
   rows = cur.fetchall();
   for row in rows:
            print("Id = ", row[0], "Name = ", row[1])
            id = row[0]
            song_name= row[4]
            song = row[5]
	
  
   path = song_name
 
 except:
         con.rollback()
         msg = "error in insert operation"  
         
 finally:
   return send_file(path, as_attachment=True)
   con.close()         
  
     

# create track function for search files     
@app.route("/listSong", methods=['GET', 'POST'])
def track():
 try:
    if request.method == "POST":
        
        app.root_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))
        print(app.root_path) 
        
        print(request.form['Song_name'])
        name =request.form['Song_name']
               
        search_data='%'+ name +'%'
        print("search_data======",search_data)
        
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        
        cur = con.cursor()
        cur.execute("SELECT *  FROM songs WHERE title LIKE ? OR artist LIKE  ? OR album LIKE ?;",(search_data,search_data,search_data,))
        #cur.execute("SELECT *  FROM songs WHERE title LIKE ? ;",(search_data,))
        
        rows = cur.fetchall();
        for row in rows:
            print("Id = ", row[0], "Name = ", row[1], "Song Name = ", row[4])
            id = row[0]
            title = row[1]
            artist = row[2]
            album = row[3]
            song_name= row[4]
            song = row[5]
            audio_files = song_name 	# an .mp3 extension
        
                     
 except:
         con.rollback()
         msg = "error in insert operation"  
         
 finally:
        #return render_template("listSong.html",rows = rows)
        return render_template("listSong.html",rows = rows,file=audio_files)
        con.close()           



# create deleteRecord function for delete files   
@app.route("/deleteRecord/<int:sond_id>")
def deleteRecord(sond_id):
    try:
        
        app.root_path = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))
        print(app.root_path) 
        
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        print("Connected to Database")
        print("sond_id in Delete",sond_id)
        
        # Deleting single record now
        cur = con.cursor()
        cur.execute('DELETE FROM songs WHERE sond_id = ?;',[sond_id])
        con.commit()
        print("Record deleted successfully ")
        cur.close()
        con.close()        
        
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT *  FROM songs')
        
        rows = cur.fetchall();
        for row in rows:
            print("Id = ", row[0], "Name = ", row[1], "Song Name = ", row[4])
            id = row[0]
            title = row[1]
            artist = row[2]
            album = row[3]
            song_name= row[4]
            song = row[5]
            audio_files = song_name
        
    except sql.Error as error:
        print("Failed to Delete Record from Table", error)
    finally:
        return render_template("listSong.html",rows = rows,file=audio_files)
        con.close() 
        #return render_template("listSong.html",rows = rows)  
        print("Connection is closed")
          
            
if __name__ == '__main__':
   app.run(debug = True)