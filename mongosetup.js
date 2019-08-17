// mongo -u admin -p asdasd00 --authenticationDatabase admin
use admin

db.createUser({
	user: "flasktester",
	pwd: "flasker00",
	roles: [{role: "readWrite", db: "flasktest"}]
})

use flasktest

db.createCollection('userinfo')
db.createCollection('groupinfo')
db.createCollection('messages')
db.createCollection('notebooks')
db.createCollection('steps')
db.createCollection('archive')
db.createCollection('fs.files')
db.createCollection('fs.chunks')
db.createCollection('news')
db.createCollection('tokens')

db.createCollection('samples')
db.createCollection('consumables')
db.createCollection('instruments')
db.createCollection('reviews')

db.createCollection('datatypes')
db.createCollection('scripts')

db.userinfo.insertOne({
	"name": "federif1",
	"password" : "sha256$EqeyZ54EPlTiz7IJ$eb1ec0c1f3e6c2d506463e2dc24509d626a2a1e2a045cbb7cde4073d33c794f9",
	"email": "filippo.federici@aalto.fi",
	"validated" : true,
	"created" : ISODate("2019-02-01T16:14:13.783Z"),
	"fullname" : "Filippo Federici Canova",
	"tel1" : "",
	"tel2" : "",
	"lastlogin" : ISODate("2019-07-18T06:39:32.656Z"),
	"hiddenmsg" : [ ],
	"grouprequests" : [ ],
	"isAdmin" : true
})
