
$.ajaxSetup ({
    // Disable caching of AJAX responses */
    cache: false
});

$(document).ready(function() {
    //Display status 								   					  
    $("#data_resync_form").submit(function(){    
        setInterval(function() {
            var resyncMsgBoxDiv = document.getElementById('resync_progress_div');
            var btnDataResync = document.getElementById('btn_data_resync');
            var user = document.getElementById('athUN').value;
            var extension = '_stdout.txt';
            var file = user+extension;
            resyncMsgBoxDiv.hidden = false;
            btnDataResync.disabled = true;
            $.ajax({url: "static/stdout/"+file, dataType: "text", success: function(result){
                $("#MsgBox").text(result); 
                //$("#MsgBox").text($("#MsgBox").text() + result);                      
            }});
        },200);
        document.getElementById('alertBrClose').hidden = false
        document.getElementById('alertBrClose').innerHTML = 'The data Re-Sync has started. It will download any new data and skip the already downloaded data. To be able to monitor the progress, please <b>leave this page opened untill the task completes.</b>';
    });  
});
