
class websiteDetails:
    def __init__(self,name,rank):
        self.name=str(name)
        self.rank=int(rank)
        self.category=None
        self.reqcode=0
        self.req_count={"GET":0,"POST":0,"CONNECT":0,"DELETE":0,"PUT":0}
        self.requestDetails=[]