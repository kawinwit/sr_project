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
 ##################### ##################### ##################### ##
#################################################	
##### connect db  ##################### ##############
#################################################	 
#################################################	
	Callobj=Project(object)	
	Callobj.setclient()


#######	#################################################
	#######   directly search title by keyword ##############
	 ##################### ##################### ##################### #####################
#################################################	
	
	get_titlefirst,get_outtotakedoc=Callobj.Search_Title(keyword)
	#print("test get title : ",get_titlefirst)
	title_faculty,title_department,title_filename=Callobj.get_DocwithOut(get_outtotakedoc)
	#print("test tak doc",title_faculty,title_department,title_filename)
	directly_search=zip(get_titlefirst,title_faculty,title_department,title_filename)
	

 ##################### ##################### ##################### #####################
#################################################	 ##################### ##################### ##################### #####################

	rank=[]
	rid_doc,rank=Callobj.getRankRelation(keyword)

	real_rid=[]
	get_department=[]
	get_faculty=[]
	get_filename=[]
	get_title=[]
############################################
	##take doc and zip to template ###############
	##normal search with keyword  ##########
	######################################
	real_rid,get_department,get_faculty,get_filename=Callobj.getDoc1(rid_doc,rank,1)
	get_title=Callobj.get_title(real_rid)
	All_Detail=zip(get_faculty,get_department,get_filename,get_title)

	###########################################
	##  fine keyword each doc and match keyword 
	############################################
	hasword=[]
	hasword=Callobj.getHasword(real_rid,keyword)


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
		rid_doc,rank=Callobj.getRankRelation(x)
		_rid=Callobj.getDoc(rid_doc,rank,1)

		#############################################
		###check ketmatch dont same before search###
		##########################
		_r=Callobj.Keymatch(Check_rid,_rid)
		_formatchdoc.append(_r)

		###################################################
		# result match key and will going  takedoc next step
		######################################

	print("formatch doc",_formatchdoc)	

	_recommended=Callobj.Doc_match(_formatchdoc)

	print(" Rid Recommend= ",_recommended)

	get_rec_department=[]
	get_rec_faculty=[]
	get_rec_filename=[]
	get_rec_title=[]
	
	get_rec_faculty,get_rec_department,get_rec_filename=Callobj.getrecommend(_recommended)
	get_rec_title=Callobj.get_title(_recommended)



	Recommendation=zip(get_rec_faculty,get_rec_department,get_rec_filename,get_rec_title)
 

	return render_template('index.html',Recommendation=Recommendation,All_Detail=All_Detail,Directly=directly_search)

if __name__=="__main__":
	app.run(debug=True)