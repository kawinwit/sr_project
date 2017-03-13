
import pyorient	

class Project():
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(Project, self).__init__()
		self.arg = arg
		


	def getRankRelation(self,keyword,client):
		catch_out=[]
		compare_str=""
		comtf=""
		catch_ranktf=[]
		Search_rank ="select from hasword where term[0] like '%"
		Search_rank=Search_rank+keyword+"%" +"'"+   "order by tfidf desc"
		return_rank = client.command(Search_rank)
		cc=0
		for All_re in return_rank:
			compare_str=''.join(str(All_re.out))
	

			comtf=''.join(str(All_re.tfidf))
			if cc==0:
				catch_out.append(compare_str)
				catch_ranktf.append(comtf)
			else:
				if catch_out[cc-1]!=compare_str:
					catch_out.append(compare_str)
					catch_ranktf.append(comtf)
				else:
					cc=cc-1
			cc+=1					
	
	
		return catch_out,catch_ranktf		

	def getDoc1(self,catch_out,catch_ranktf,cc,client):
		Static_term="select @rid , department, faculty, filename from document where @rid="
		New=""
		Query_doc=[]
		Return_Doc=[]
		Document=[]


		get_department=[]
		get_faculty=[]
		get_filename=[]

		if cc==1:
			for e in catch_out:
				New=Static_term+e
				Query_doc.append(New)
		else:
				New=Static_term+catch_out[0]
				Query_doc.append(New)

		c=0
		#Keyword take Doc
		allRid=[]
		for e in Query_doc:
			Return_Doc = client.command(e)

			for d in Return_Doc:
				tostring=''.join(str(d.rid))
				allRid.append(tostring)


				get_department.append(d.department)
				get_faculty.append(d.faculty)
				get_filename.append(d.filename)

				print(c+1," : --Department : ",d.department, " "" --Faculty : ",d.faculty ,"  --Name document =",d.filename," Rank about keyword = : ",catch_ranktf[c])
			c+=1

		return allRid,get_department,get_faculty,get_filename
	
	def getDoc(self,catch_out,catch_ranktf,cc,client):
		Static_term="select @rid , department, faculty, filename from document where @rid="
		New=""
		Query_doc=[]
		Return_Doc=[]
		Document=[]

		get_department=[]
		get_faculty=[]
		get_filename=[]

		if cc==1:
			for e in catch_out:
				New=Static_term+e
				Query_doc.append(New)
		else:
				New=Static_term+catch_out[0]
				Query_doc.append(New)

		c=0
		#Keyword take Doc
		allRid=[]
		for e in Query_doc:
			Return_Doc = client.command(e)

			for d in Return_Doc:
				tostring=''.join(str(d.rid))
				allRid.append(tostring)

				get_department.append(d.department)
				get_faculty.append(d.faculty)
				get_filename.append(d.filename)
				print(c+1," : --Department : ",d.department, " "" --Faculty : ",d.faculty ,"  --Name document =",d.filename," Rank about keyword = : ",catch_ranktf[c])
				
			c+=1

		return allRid

	def getrecommend(self,rid,client):
		Static_term="select from document where @rid="
		New=""
		Query_doc=[]
		Return_Doc=[]

		get_department=[]
		get_faculty=[]
		get_filename=[]

		for e in rid:
			New=Static_term+e
			Query_doc.append(New)
	

		c=0
		#Keyword take Doc
		allRid=[]
		for e in Query_doc:
			Return_Doc = client.command(e)

			for d in Return_Doc:
				get_department.append(d.department)
				get_faculty.append(d.faculty)
				get_filename.append(d.filename)
				
			c+=1

		return get_faculty,get_department,get_filename				

	def getHasword(self,all_rid,_key,client):

		catch_sql=[]
		static_sql="select expand( out( hasword )) from document where @rid ="
		real_sql=""
		pick_sql=""
		rs_hasword=[]
		key=()

		for query in all_rid:
			real_sql=static_sql+query
			catch_sql.append(real_sql)

	##################
	####query all key#########
	##################
		for query in catch_sql:
			rs_termindex_all=client.command(query)
			for all_termindex in rs_termindex_all:
				try:
					if all_termindex.keyword!=_key:
						key=key+(all_termindex.keyword,)
				except AttributeError:
					pass
			rs_hasword.append(key)
			key=()

		#print("\n",rs_hasword)

		##################
	####   find match key  #########
	##################  ##########
		_r=[]
		for i in range(len(rs_hasword)):
			for l in range(len(rs_hasword[i])):
				_count_column=i
				NextColumn=_count_column+1
				
				# next obj in list
				while NextColumn<=len(rs_hasword)-1:
					for n in range(len(rs_hasword[NextColumn])):
						if rs_hasword[i][l]==rs_hasword[NextColumn][n]:
							_r.append(rs_hasword[i][l])
					NextColumn+=1

		
		_r.sort()
		"""print("\n",_r,"\n")
    ##################################
    ######################
		get in dex max
		##############################
		"""
		_re_hasword=()
		_has=[]
		_catch=''
		_catch_pop=[]
		
		## save hasword
		for i in _r:
			_re_hasword=_re_hasword+(i,)	


			
		for i in range(len(_r)):
			check=_r.pop()

			if _catch!=check:
				_has.append(_re_hasword.count(check))
				_catch_pop.append(check)
				_catch=check

		_has.reverse()
		_catch_pop.reverse()
		_catch_hasdoc=[]
		for x in _has:
			_catch_hasdoc.append(x)

		print(_catch_pop,"\n")
		print(_has)
		
		_c=[]
		_forCom=[]
		cc=0
		for i in range(len(_catch_pop)):
			_c.append(_has[i])
			_c.append(_catch_pop[i])
			_forCom.append(_c)
			_c=[]

		_forCom.sort()
		_forCom.reverse()
		print(_forCom)

		c_forCom=[]
		__c=[]
		"""
			Max 2 value and under max 2 value
		"""
		for i in range(len(_forCom)):
			if len(c_forCom)<3:
				c_forCom.append(_forCom[i][0])


		if len(c_forCom)==3:
			if c_forCom[0]==c_forCom[1]:
				c_forCom.pop(2)
			elif c_forCom[0]!=c_forCom[1] and c_forCom[1]> c_forCom[2]:
				c_forCom.pop(2)




		for x in range(len(c_forCom)):
			__c.append(_forCom[x][1])

		print(__c)	



		return __c

	def get_title(self,rid,client):
		static_sql="select expand( out( hasword )) from document where @rid ="
		catch_sql=[]

		real_sql=""
		pick_sql=""
		rs_hasword=[]
		key=[]

		for query in rid:
			real_sql=static_sql+query
			catch_sql.append(real_sql)

			##################
			###query all title of documnet #########
				##################
		for query in catch_sql:
			rs_termindex_all=client.command(query)
			for all_termindex in rs_termindex_all:
				try:
					rs_hasword.append(all_termindex.title)
				except AttributeError:
					pass
			
		
		return rs_hasword
	def Keymatch(self,_check,_rid):
		_recom=[]
		c=0
		#print(_check,_rid)
		for x in _rid:
			for y in _check:
				if x==y:
					c=c+1
			if c==0:
				_recom.append(x)
			else:	
				c=0		
		#print(_recom)
		return _recom



	def Doc_match(self,_doc):
	
		c01=[]
		_c=0
		if len(_doc)==2:
			for i in range(len(_doc)):
				for x in range(len(_doc[i])):
					_y=i+1
					while _y<=len(_doc)-1:
						for yy in range(len(_doc[_y])):
							if _doc[i][x]==_doc[_y][yy]:
								c01.append(_doc[i][x])
						_y+=1
						
		elif len(_doc)==3:
			for i in _doc[0]:
				for l in _doc[1]:
					if i==l:
						_c=c01.count(i)
						if _c==0:
							c01.append(i)
						_c=0

				for l in _doc[2]:		
					if i==l:
						_c=c01.count(i)
						if _c==0:
							c01.append(i)
						_c=0

		return c01			

##########################################################
################# Main first  ##################################
##########################################################


### get keyword from termindex

#keyword=Callobj.getTermindex(keyword)
#########################
##get ranking word in doc#######
#############################




##########################
##########################
## keymatch and max keyword to reccmommend and get 1 doc recomended##
#########################
##########################



