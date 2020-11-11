
class websiteDetails:
    def __init__(self,name,rank):
        self.name=str(name)
        self.rank=int(rank)
        self.category=None
        self.reqcode=0
        self.req_count={"GET":0,"POST":0,"CONNECT":0,"DELETE":0,"PUT":0}
        self.requestDetails=[]
    
    def __str__(self):
        if(self.requestDetails!=[]):
            return [self.name,self.rank,self.category,self.reqcode,self.requestDetails]
        else:
            return [self.name,self.rank]

    def __repr__(self):
        if(self.requestDetails!=[]):
            return [self.name,self.rank,self.category,self.reqcode,self.requestDetails]
        else:
            return [self.name,self.rank]