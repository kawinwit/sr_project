from flask import Flask , render_template , request , url_for ,redirect,flash
from function import Project
import pyorient


app = Flask(__name__)

@app.route('/')
def index():
	
	return render_template('index.html')

@app.route('/inputkey',methods=['GET','POST'])
def getKey():
	if request.method=="POST":
		keyword=request.form['keywords']

	client = pyorient.OrientDB("localhost", 2424) 
	session_id = client.connect( "root", "*" );
	client.db_open( "Project", "root","*")
	Callobj=Project(object)	

	rid_doc=[]
	
	rank=[]
	rid_doc,rank=Callobj.getRankRelation(keyword,client)

	real_rid=[]
	get_department=[]
	get_faculty=[]
	get_filename=[]
	get_title=[]
############################################
	##take doc and zip to template ###############
	##normal search with keyword  ##########
	######################################
	real_rid,get_department,get_faculty,get_filename=Callobj.getDoc1(rid_doc,rank,1,client)
	get_title=Callobj.get_title(real_rid,client)
	All_Detail=zip(get_faculty,get_department,get_filename,get_title)

	###########################################
	##  fine keyword each doc and match keyword 
	############################################
	hasword=[]
	hasword=Callobj.getHasword(real_rid,keyword,client)


	_r=[]
	_formatchdoc=[]
	_recommended=[]
	Check_rid=[]
		#################################################################
	## get rid before search afther new match dont same before doc ##
	#################################################################
	for i in real_rid:
		Check_rid.append(i)

	print("\n")
	for x in hasword:
		print("key recommended :",x)
		rid_doc,rank=Callobj.getRankRelation(x,client)
		_rid=Callobj.getDoc(rid_doc,rank,1,client)

		#############################################
		###check ketmatch dont same before search###
		##########################
		_r=Callobj.Keymatch(Check_rid,_rid)
		_formatchdoc.append(_r)

		###################################################
		# result match key and will going takedoc next step
		######################################

	print(_formatchdoc)	

	_recommended=Callobj.Doc_match(_formatchdoc)
	get_rec_department=[]
	get_rec_faculty=[]
	get_rec_filename=[]
	get_rec_title=[]
	
	get_rec_faculty,get_rec_department,get_rec_filename=Callobj.getrecommend(_recommended,client)
	get_rec_title=Callobj.get_title(_recommended,client)



	Recommendation=zip(get_rec_faculty,get_rec_department,get_rec_filename,get_rec_title)

	
	print(get_rec_faculty)	


	
	

	return render_template('index.html',Recommendation=Recommendation,All_Detail=All_Detail)

if __name__=="__main__":
	app.run(debug=True)