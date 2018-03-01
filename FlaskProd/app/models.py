# from app import db
#
# class Stwdaycount(db.Model):
#     __tablename__ = 'product_stw_daycount'
#     userid = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), primary_key=True)
#     schoolid = db.Column(db.BigInteger, primary_key=True)
#     schoolname = db.Column(db.String(200), primary_key=True)
#     classname = db.Column(db.String(200), primary_key=True)
#     classid = db.Column(db.Integer, primary_key=True)
#     bookname = db.Column(db.String(200), primary_key=True)
#     bookid = db.Column(db.String(200), primary_key=True)
#     hp = db.Column(db.Integer, primary_key=True)
#     credit = db.Column(db.Integer, primary_key=True)
#     countscore = db.Column(db.Float)
#     numhomework = db.Column(db.Integer)
#     numselfwork = db.Column(db.Integer)
#     topicnum = db.Column(db.Integer)
#     countright = db.Column(db.Integer)
#     rightlv = db.Column(db.Float)
#     counttime = db.Column(db.Integer)
#     datetime = db.Column(db.String(200), primary_key=True)
#
#     def __repr__(self):
#         return '<Stwdaycount %r>' % self.username