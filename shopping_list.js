var express    = require('express');
var Webtask    = require('webtask-tools');
var bodyParser = require('body-parser');
var sha1 = require('sha-1');
var lodash = require('lodash');
var app = express();

// Using URL encoded parser as this makes it easier to test with the webtask.io runner
var urlencodedParser = bodyParser.urlencoded({ extended: false })
app.use(urlencodedParser);

app.get('/items', function (req, res) {
  req.webtaskContext.storage.get(function(err, data){
      if(err){
        errorResponse(res, 500, 'Internal server error');
      } else {
       data = data || []; 
       res.send({items: data});
       res.sendStatus(200);
      }
  });
});

app.post('/items', function (req, res) {
    var name = req.body.name;
    var quantity = req.body.quantity;
    if (!name) {
      errorResponse(res, 400, 'Name is missing');
    } else {
      var date = new Date();
      // Generating unique ids for the entries. Extremely unlikely to get duplicate ids
      var id = sha1(name + date.getTime());
      var entry = {id: id, name: name, date_added: date.toString()}
      // Quantity is an optional field. Only some entries have it set
      if (quantity) {
        entry.quantity = quantity;
      }
      req.webtaskContext.storage.get(function(readErr, data){
          if(readErr){
            console.error('Reading the data failed', readErr);
            errorResponse(res, 500, 'Internal server error');
          } else {
            data = data || []; 
            data.push(entry);
            req.webtaskContext.storage.set(data, function(writeErr) {
              if(writeErr) {
                console.error('Writing the data failed', writeErr);
                errorResponse(res, 500, 'Internal server error');
              } else {
                res.writeHead(200, { 'Content-Type': 'application/json'});
                res.end(JSON.stringify(entry));
              }
            });
          }
      });
    }
});

app.delete('/items/:itemId', function (req, res) {
  console.log("vlad");
  req.webtaskContext.storage.get(function(readErr, data){
    if(readErr){
      console.error('Reading from database failed', readErr);
      errorResponse(res, 500, 'Internal server error');
    } else {
      data = data || []; 
      var found = lodash.remove(data, (e) => e.id == req.params.itemId);
      if (found.length == 0) {
        errorResponse(res, 404, 'Id not found');
      } else {
        req.webtaskContext.storage.set(data, function(writeErr) {
          if(writeErr) {
            console.error('Writing to database failed', writeErr);
            errorResponse(res, 500, 'Internal server error');
          } else {
            res.sendStatus(200);
          }
        });
      }
    }
  });
});

module.exports = Webtask.fromExpress(app);

// Helper function that will make our error responses consistent
function errorResponse(res, httpStatus, errorMessage) {
      res.writeHead(httpStatus, { 'Content-Type': 'application/json'});
      res.end(JSON.stringify({error: errorMessage}));  
}
