var base_api = '/chat/api/v1.0/';
var chat = chat || {};

chat.api = function(url_extra, callback){
    jQuery.getJSON(base_api+url_extra, callback);
    // Hack shortcut for api json
};

jQuery(function($){
    chat.api('chats', function(data){
      console.log(data);
      var chats = [];
      $.each( data, function( key, val ) {
        chats.push( "<li id='" + key + "'>" + val + "</li>" );
      });
     
      $( "<ul/>", {
        "class": "chat-output-list",
        html: chats.join( "" )
      }).appendTo( ".chat-output" );
    });
});