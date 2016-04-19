var baseApi = 'http://api.chat.local/chat/api/v1.0/';
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

chat.error = function(errorText){
  // Add an error element 
  var err = $("<span class='error'/>").text(errorText);
  $(chatInput).closest('label').prepend(err);
  // Append a label up the tree.
};

// Pull the chats since a point in time
chat.update = function(last){
  // Get chats from a certain point in time.
  chat.api('chats/?from='+last, function(data){
    chat.append(data); // Append the latest chats.
  });
};

// Append any totally new chats
chat.append = function(data){
  // Loop through the chat data
  var chats = [];
  $.each( data, function( key, val ) {
    chats.push( "<dd id='chat-" + key + "'>" + val.username + "</dd><dt>" + val.chat + "</dt>" );
  });

  $('.chat-output-list').append($(chats.join('')));
};

// initialize the chat area
chat.init = function(){
  $( "<dl/>", {
    "class": "chat-output-list",
    html: ''
  }).appendTo( ".chat-output" );
};

// test some of the chat functionality
chat.test = function(){
  chat.error('test');
  chat.clear();
  chat.update();
  chat.init();
  var testChat = {
        'id': 3,
        'username':'William',
        'chat': 'I, William, am putting up another chat entirely.',
        'date_created': '2016-04-19 17:58:33.645138-04',
        'done': false
    };
  var testChats = {
    'chats':[testChat]
    };

  chat.append(testChats);
};

chat.push = function(author, pass, text){
  jQuery.getJSON(baseApi+chats, function(){
    chat.clear(); // Clear upon success
  }).fail(function(){
    chat.error('Sorry, there was a problem sending your chat message.');
  });
};

jQuery(function($){
  chat.init();
  chat.update();

});