var apiDomain = 'http://api.chat.local/'
var apiVersion = 'chat/api/v1.0/';
var baseApi = apiDomain + apiVersion;
var chat = chat || {};

var chatForm = '#chat-input-form';
var chatInput = '#chat-input-form input[name=chat]';

// Initialized lastUpdated for checking for new chats.
chat.lastUpdated = chat.lastUpdated || null;

chat.api = function(urlExtra, callback){
    jQuery.getJSON(baseApi+urlExtra, callback);
    // Hack shortcut for api json
};

// Clear the input field
chat.clear = function(){
  $(chatForm).find('input[name=chat]').val('');
};

// initialize the chat area
chat.init = function(){
  $('.chat-output-list').remove();
  $( "<ul/>", {
    "class": "chat-output-list",
    html: ''
  }).appendTo( ".chat-output" );
};

chat.error = function(errorText){
  // Pop in the error element.
  var err = $(".chat-error").text(errorText).removeClass('hidden');
};

// Pull the chats since a point in time
chat.update = function(since){
  // Get chats since a certain point in time.
  chat.api('chats' + (since? '?since='+since : ''), function(data){
    chat.append(data); // Append the latest chats.
  });
  return new Date().getTime(); // Return updated latest
};

// Append any totally new chats
chat.append = function(data){
  console.log(data);
  // Loop through the chat data
  var chats = [];
  $.each( data.chats, function( key, val ) {
    chats.pushOut( "<li><strong id='chat-" + key + "' class='username'>" + val.username + "</strong><p>" + val.chat + "</p></li>" );
  });

  $('.chat-output-list').append($(chats.join('')));
};

chat.pushOut = function(author, pass, text){
  var nwChat = 
  jQuery.post(baseApi+'chats', function(){
    chat.clear(); // Clear upon success
    chat.update(chat.latest); // Update with newer chats
  }).fail(function(){
    chat.error('Sorry, there was a problem sending your chat message.');
  });
};

// test some of the chat functionality
chat.test = function(){
  chat.error('Simple test error!');
  chat.clear();
  //chat.update();
  var testChats = {
    'chats':[
        {
          'id': 3,
          'username':'William',
          'chat': 'I, William, am putting up another chat entirely.',
          'date_created': '2016-04-18 17:58:33.645138-04',
          'done': false
        },
        {
          'id': 4,
          'username':'William',
          'chat': 'Another fake chat sent from William here!',
          'date_created': '2016-04-19 17:58:33.645138-04',
          'done': false
        }
      ]
    };
  chat.append(testChats);
};

// Standard domload
jQuery(function($){
  chat.init();
  chat.latest = chat.latest || null;
  // Ideally we'd use websockets for the chat, but I'm going to poll for now
  (function poll() {
    chat.latest = chat.update(chat.latest);
    setTimeout(function(){
      // Poll for chat updates
      chat.latest = chat.update(chat.latest);
    }, 6000);
  })();
  $(chatForm).submit(function(e){
    // author, pass, text
    chat.pushOut('someAuthor', 'pass', $(chatInput).val());
    e.preventDefault();
  });
});