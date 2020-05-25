const expressSession = require('express-session');
const bodyParser     = require('body-parser');
const express        = require('express');
const multer         = require('multer');
const path           = require('path');
const spawn          = require('child_process').spawn;
const app            = express();

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname + '/public'));

app.use(expressSession({
    secret: "key",
    saveUninitialized: "false",
    resave: "false"
}));

const storage = multer.diskStorage({
    destination: './public/images',
    filename:  function(req, file, cb) {
        cb(null, file.originalname);
    }
})

const upload = multer({
    storage: storage,
    limit: {fileSize: 3000000},
    fileFilter: function(req, file, cb){
        checkFileType(file, cb);
    }
}).single('myFile'); // I have to add form name 

function checkFileType(file, cb){
    // Allowed ext
    const filetypes = /jpeg|jpg|png|gif/;
    // Check ext
    const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
    // Check mime
    const mimetype = filetypes.test(file.mimetype);
  
    if(mimetype && extname){
      return cb(null,true);
    } else {
      cb('Error: Images Only!');
    }
  }

//

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/views/front.html');
});

app.get('/index', (req, res) => {
    res.sendFile(__dirname + '/views/index.html');
});
let a;
app.post('/index',  (req, res) => {
    
    let uploading = new Promise ((resolve, reject) => {
        upload(req, res, err => {
            if(err) {
                res.sendFile(__dirname + '/views/index.html');
            } else {
                if(req.file === undefined) {
                    console.log('Undefined!');
                } else {
                    console.log('File uploaded');
                    a = req.file.originalname;
                    var dataToSend;
                    // spawn new child process to call the python script
                    const python = spawn('python', ['script.py', a ]);
                    // collect data from script
                    python.stdout.on('data', function (data) {
                    //console.log('Pipe data from python script ...');
                    dataToSend = data.toString();
                    });
                    // in close event we are sure that stream from child process is closed
                    python.on('close', (code) => {
                    //console.log(`child process close all stdio with code ${code}`);
                    // send data to browser
                    res.redirect('/result');
                    });
                }
            }
        });
    });
    uploading
    .then( a => {
            
    });
});

app.get('/result', (req, res) => {
    res.render('result.ejs',{fileName: a});
});

//
const PORT = 3000;
app.listen(PORT, (req, res) => {
    console.log(`Server Started at PORT: ${PORT}`);
});