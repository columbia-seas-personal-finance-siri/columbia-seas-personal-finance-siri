
"use strict";

// Imports dependencies and set up http server
const request = require("request"),
  express = require("express"),
  body_parser = require("body-parser"),
  axios = require("axios").default,
  app = express().use(body_parser.json()); // creates express http server

// Sets server port and logs message on success
app.listen(process.env.PORT || 1337, () => console.log("webhook is listening"));

// Accepts POST requests at /webhook endpoint
app.post("/webhook", (req, res) => {
  

  // Default Example
  // sendAknowledgeMessage(req);

  // Movie integration
  showMovieIntegration(req, res);
});

// Accepts GET requests at the /webhook endpoint. You need this URL to setup webhook initially.
// info on verification request payload: https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests 
app.get("/webhook", (req, res) => {
  
  // Parse params from the webhook verification request
  let mode = req.query["hub.mode"];
  let token = req.query["hub.verify_token"];
  let challenge = req.query["hub.challenge"];

  // Check if a token and mode were sent
  if (mode && token) {
    // Check the mode and token sent are correct
    if (mode === "subscribe" && token === process.env.VERIFY_TOKEN) {
      // Respond with 200 OK and challenge token from the request
      console.log("WEBHOOK_VERIFIED");
      res.status(200).send(challenge);
    } else {
      // Responds with '403 Forbidden' if verify tokens do not match
      res.sendStatus(403);
    }
  }
});

function sendAknowledgeMessage(req) {
  let body = req.body;

  // Check the Incoming webhook message
  if (body.object) {
    if (
      body.entry &&
      body.entry[0].changes &&
      body.entry[0].changes[0] &&
      body.entry[0].changes[0].value.messages &&
      body.entry[0].changes[0].value.messages[0]
    ) {

      let phone_number_id =
      body.entry[0].changes[0].value.metadata.phone_number_id;
      let from = body.entry[0].changes[0].value.messages[0].from; // extract the phone number from the webhook payload
      let msg_body = body.entry[0].changes[0].value.messages[0].text.body; // extract the message text from the webhook payload
      
      axios({
        method: "POST", // Required, HTTP method, a string, e.g. POST, GET
        url:
          "https://graph.facebook.com/v15.0/" +
          phone_number_id +
          "/messages?access_token=" +
          process.env.ACCESS_TOKEN,
        data: {
          messaging_product: "whatsapp",
          to: from,
          text: { body: "Ack: " + msg_body },
        },
        headers: { "Content-Type": "application/json" },
      });
    }
  }
}

function getRecipientPhoneNumber(req) {
  return req.body.entry[0].changes[0].value.messages[0].from;
}


function showMovieIntegration(req, res) {
  let body = req.body;
   if (body.object) {
    if (
      body.entry &&
      body.entry[0].changes &&
      body.entry[0].changes[0] &&
      body.entry[0].changes[0].value.messages &&
      body.entry[0].changes[0].value.messages[0]) {
    let recipientPhoneNumber = getRecipientPhoneNumber(req); 

    var data = getTemplatedMessageInput(recipientPhoneNumber);

    sendMessage(data)
      .then(function (response) {
        console.log("message sent");
        return;
      })
      .catch(function (error) {
        console.log(error);
        return;
      });
        
      res.sendStatus(200);
    } else {
      res.sendStatus(404);
    }
   }
}

function isMessageValid(req) {
  let body = req.body;
  return body.object &&
      body.entry &&
      body.entry[0].changes &&
      body.entry[0].changes[0] &&
      body.entry[0].changes[0].value.messages &&
      body.entry[0].changes[0].value.messages[0]
    
}

function sendMessage(data) {
  
  var config = {
    method: 'post',
    url: `https://graph.facebook.com/${process.env.API_VERSION}/${process.env.BIZ_PHONE_NUMBER_ID}/messages`,
    headers: {
      'Authorization': `Bearer ${process.env.ACCESS_TOKEN}`,
      'Content-Type': 'application/json'
    },
    data: data
  };

  return axios(config)
}

function getTemplatedMessageInput(recipient) {
  return JSON.stringify({
    "messaging_product": "whatsapp",
    "to": recipient,
    "type": "template",
    "template": {
      "name": "thank_you_read_more",
      "language": {
        "code": "en_US"
      }
    }
  }
  );
}
